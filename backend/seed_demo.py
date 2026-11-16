"""Insert optional synthetic demonstration records (safe to rerun)."""
from fastapi.testclient import TestClient
from main import app

SEEDS = [{'workspace': 'Acme Studio', 'title': 'Design dashboard', 'assignee': 'Alex', 'priority': 'High', 'status': 'In Progress', 'due_date': '2026-12-01'}, {'workspace': 'Acme Studio', 'title': 'Set up automated tests', 'assignee': 'Jordan', 'priority': 'Medium', 'status': 'Backlog', 'due_date': '2026-12-03'}]
client=TestClient(app)
if client.get('/api/items').json():
    print('Existing records found; skipping seed.')
else:
    for record in SEEDS:
        result=client.post('/api/items',json=record)
        result.raise_for_status()
    print('Added',len(SEEDS),'synthetic sample records.')
