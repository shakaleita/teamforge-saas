"""TeamForge local portfolio API.

No authentication is implemented: do not deploy publicly without access controls.
"""
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

APP_TITLE = "TeamForge"
DB = Path(os.environ.get("APP_DB", str(Path(__file__).parent / "app.db")))
STATUSES = ("Backlog", "In Progress", "Review", "Done")
Priority = Literal["Low", "Medium", "High", "Urgent"]
Status = Literal["Backlog", "In Progress", "Review", "Done"]

app = FastAPI(title=APP_TITLE, version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

@contextmanager
def db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            workspace TEXT NOT NULL,
            title TEXT NOT NULL,
            assignee TEXT NOT NULL DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Backlog',
            due_date TEXT NOT NULL DEFAULT ''
        )""")
        con.execute("CREATE INDEX IF NOT EXISTS idx_tasks_workspace_status ON tasks (workspace, status)")

init_db()

with db() as con:
    con.execute("""CREATE TABLE IF NOT EXISTS task_activity (
        id INTEGER PRIMARY KEY, task_id INTEGER NOT NULL, workspace TEXT NOT NULL,
        action TEXT NOT NULL, detail TEXT NOT NULL, recorded_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    con.execute("CREATE INDEX IF NOT EXISTS idx_task_activity_workspace ON task_activity(workspace, id)")

class Task(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    workspace: str = Field(default="Acme Studio", min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    assignee: str = Field(default="", max_length=100)
    priority: Priority = "Medium"
    status: Status = "Backlog"
    due_date: str = Field(default="", max_length=30)

class TaskEdit(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    workspace: str | None = Field(default=None, min_length=1, max_length=100)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    assignee: str | None = Field(default=None, max_length=100)
    priority: Priority | None = None
    status: Status | None = None
    due_date: str | None = Field(default=None, max_length=30)


def row_or_404(con: sqlite3.Connection, item_id: int):
    found = con.execute("SELECT * FROM tasks WHERE id=?", (item_id,)).fetchone()
    if found is None:
        raise HTTPException(404, "Task not found")
    return dict(found)

@app.get("/api/health")
def health():
    return {"ok": True, "service": APP_TITLE}

@app.get("/api/items")
def list_items(
    workspace: str | None = None,
    status: Status | None = None,
    search: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    filters = []
    values = []
    if workspace is not None:
        filters.append("workspace = ?")
        values.append(workspace)
    if status is not None:
        filters.append("status = ?")
        values.append(status)
    if search:
        filters.append("(title LIKE ? OR assignee LIKE ?)")
        pattern = "%" + search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        # LIKE escaping below makes a literal search rather than arbitrary wildcard matching.
        filters[-1] = "(title LIKE ? ESCAPE '\\' OR assignee LIKE ? ESCAPE '\\')"
        values.extend([pattern, pattern])
    sql = "SELECT * FROM tasks" + (" WHERE " + " AND ".join(filters) if filters else "")
    with db() as con:
        return [dict(r) for r in con.execute(sql + " ORDER BY id DESC LIMIT ? OFFSET ?", (*values, limit, offset))]

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    with db() as con:
        return row_or_404(con, item_id)

@app.post("/api/items", status_code=201)
def create_item(item: Task):
    with db() as con:
        cursor = con.execute(
            "INSERT INTO tasks(workspace,title,assignee,priority,status,due_date) VALUES (?,?,?,?,?,?)",
            (item.workspace, item.title, item.assignee, item.priority, item.status, item.due_date),
        )
        result = row_or_404(con, cursor.lastrowid)
        con.execute("INSERT INTO task_activity(task_id,workspace,action,detail) VALUES(?,?,?,?)", (result["id"], item.workspace, "created", item.title))
        return result

@app.patch("/api/items/{item_id}")
def change_status(item_id: int, status: Status):
    """Backward-compatible endpoint used by the original React dashboard."""
    with db() as con:
        row_or_404(con, item_id)
        current = row_or_404(con, item_id)
        con.execute("UPDATE tasks SET status=? WHERE id=?", (status, item_id))
        con.execute("INSERT INTO task_activity(task_id,workspace,action,detail) VALUES(?,?,?,?)", (item_id,current["workspace"],"status_changed",f"{current['status']} → {status}"))
        return row_or_404(con, item_id)

@app.put("/api/items/{item_id}")
def edit_item(item_id: int, changes: TaskEdit):
    fields = changes.model_dump(exclude_unset=True)
    if not fields:
        raise HTTPException(422, "Provide at least one field")
    if any(value is None for value in fields.values()):
        raise HTTPException(422, "Fields cannot be null")
    with db() as con:
        row_or_404(con, item_id)
        assignments = ", ".join(f"{name}=?" for name in fields)
        con.execute(f"UPDATE tasks SET {assignments} WHERE id=?", (*fields.values(), item_id))
        updated = row_or_404(con, item_id)
        con.execute("INSERT INTO task_activity(task_id,workspace,action,detail) VALUES(?,?,?,?)", (item_id,updated["workspace"],"edited",", ".join(fields)))
        return updated

@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    with db() as con:
        row_or_404(con, item_id)
        existing = row_or_404(con, item_id)
        con.execute("DELETE FROM tasks WHERE id=?", (item_id,))
        con.execute("INSERT INTO task_activity(task_id,workspace,action,detail) VALUES(?,?,?,?)", (item_id,existing["workspace"],"deleted",existing["title"]))

@app.get("/api/summary")
def summary(workspace: str | None = None):
    query = "SELECT status AS label, COUNT(*) AS value FROM tasks"
    values = ()
    if workspace is not None:
        query += " WHERE workspace=?"
        values = (workspace,)
    query += " GROUP BY status ORDER BY status"
    with db() as con:
        return [dict(r) for r in con.execute(query, values)]


# v0.3: auditable task changes
from fastapi import Query as _Query
@app.get('/api/activity')
def activity(workspace: str | None = None, limit: int = _Query(25, ge=1, le=100)):
    with db() as con:
        if workspace is None:
            data = con.execute('SELECT * FROM task_activity ORDER BY id DESC LIMIT ?', (limit,))
        else:
            data = con.execute('SELECT * FROM task_activity WHERE workspace=? ORDER BY id DESC LIMIT ?', (workspace,limit))
        return [dict(r) for r in data]



# v0.5: authenticated owner session for demo deployment
# Project health metrics: completion, overdue tasks, and priority distribution.
@app.get('/api/insights')
def task_insights(workspace: str | None = None):
    filters = ' WHERE workspace=?' if workspace is not None else ''
    args = (workspace,) if workspace is not None else ()
    with db() as con:
        totals = con.execute("""SELECT COUNT(*) AS total,
          SUM(CASE WHEN status='Done' THEN 1 ELSE 0 END) AS completed,
          SUM(CASE WHEN status!='Done' AND date(due_date)<date('now') THEN 1 ELSE 0 END) AS overdue
          FROM tasks"""+filters, args).fetchone()
        priority = con.execute('SELECT priority,COUNT(*) AS tasks FROM tasks'+filters+
                               ' GROUP BY priority ORDER BY priority',args).fetchall()
    total = totals['total']
    return {'workspace':workspace,'total_tasks':total,'completed_tasks':totals['completed'] or 0,
            'overdue_tasks':totals['overdue'] or 0,
            'completion_percent':round(100*(totals['completed'] or 0)/total,1) if total else 0,
            'by_priority':[dict(row) for row in priority]}

from security import install_auth
install_auth(app,DB)

# v0.5: persistent task discussions and board aggregate model
with db() as con:
    con.executescript("""CREATE TABLE IF NOT EXISTS task_comments(
        id INTEGER PRIMARY KEY,task_id INTEGER NOT NULL,author TEXT NOT NULL,body TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE);
        CREATE INDEX IF NOT EXISTS idx_task_comments_task ON task_comments(task_id,id);""")

class Comment(BaseModel):
    model_config=ConfigDict(str_strip_whitespace=True)
    author:str=Field(min_length=1,max_length=80)
    body:str=Field(min_length=1,max_length=2000)

@app.get('/api/items/{item_id}/comments')
def task_comments(item_id:int):
    with db() as con:
        row_or_404(con,item_id)
        return [dict(r) for r in con.execute('SELECT * FROM task_comments WHERE task_id=? ORDER BY id',(item_id,))]

@app.post('/api/items/{item_id}/comments',status_code=201)
def add_task_comment(item_id:int,payload:Comment):
    with db() as con:
        task=row_or_404(con,item_id)
        cur=con.execute('INSERT INTO task_comments(task_id,author,body) VALUES(?,?,?)',(item_id,payload.author,payload.body))
        con.execute('INSERT INTO task_activity(task_id,workspace,action,detail) VALUES(?,?,?,?)',(item_id,task['workspace'],'commented',payload.author))
        return dict(con.execute('SELECT * FROM task_comments WHERE id=?',(cur.lastrowid,)).fetchone())

@app.get('/api/board')
def task_board(workspace:str|None=None):
    with db() as con:
        if workspace:
            records=[dict(x) for x in con.execute('SELECT * FROM tasks WHERE workspace=? ORDER BY id DESC',(workspace,))]
        else:
            records=[dict(x) for x in con.execute('SELECT * FROM tasks ORDER BY id DESC')]
    return {'workspace':workspace,'columns':[{'status':status,'count':sum(x['status']==status for x in records),
            'tasks':[x for x in records if x['status']==status]} for status in STATUSES]}
