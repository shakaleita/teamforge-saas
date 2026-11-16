import AuthGate from './AuthGate.jsx';
import ProjectExtras from './ProjectExtras.jsx';
import React, {useEffect,useState,useCallback} from 'react';
import {createRoot} from 'react-dom/client';
import './styles.css';
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const meta = {"id": 1, "title": "TeamForge", "description": "Multi-workspace project & task management", "createTitle": "Create new task", "listTitle": "Tasks"};
const fields = [["workspace", "Workspace", "text", "Acme Studio"], ["title", "Task title", "text", "Build dashboard"], ["assignee", "Assignee", "text", "Alex"], ["priority", "Priority", "select", "Medium|Low|Medium|High|Urgent"], ["status", "Status", "select", "Backlog|Backlog|In Progress|Review|Done"], ["due_date", "Due date", "date", ""]];
const defaults = Object.fromEntries(fields.map(([key,,type,initial])=>[key,type==='select'?initial.split('|')[1]:initial]));
const request = async(path,options={})=>{
 const r=await fetch(API+path,{...options,headers:{'Content-Type':'application/json',...(options.headers||{})}});
 if(r.status===204)return null;
 let data=await r.json().catch(()=>({detail:'Unexpected server response'}));
 if(!r.ok)throw new Error(typeof data.detail==='string'?data.detail:JSON.stringify(data.detail||data));
 return data;
};
function App(){
 const [items,setItems]=useState([]),[metrics,setMetrics]=useState([]),[form,setForm]=useState(defaults),[notice,setNotice]=useState(''),[busy,setBusy]=useState(false),[filter,setFilter]=useState('');
 const [extra,setExtra]=useState([]),[search,setSearch]=useState(''),[selected,setSelected]=useState(null),[room,setRoom]=useState('general');
 const refresh=useCallback(async()=>{
   try {
    const q=meta.id===7?'?room='+encodeURIComponent(room):'';
    const [a,b]=await Promise.all([request('/api/items'+q),request('/api/summary')]);setItems(a);setMetrics(b);
    if(meta.id===6)setExtra(await request('/api/enrolments'));
    if(meta.id===9)setExtra(await request('/api/history'));
   } catch(e){setNotice('Connection: '+e.message)}
 },[room]);
 useEffect(()=>{refresh()},[refresh]);
 useEffect(()=>{
   if(meta.id!==7)return;
   const url=API.replace(/^http/,'ws')+'/ws/'+encodeURIComponent(room);
   const ws=new WebSocket(url); ws.onmessage=()=>refresh();
   return()=>ws.close();
 },[room,refresh]);
 async function mutate(path,options){setBusy(true);try{const x=await request(path,options);setNotice('Saved successfully');await refresh();return x}catch(e){setNotice('Error: '+e.message);return null}finally{setBusy(false)}}
 const create=async e=>{e.preventDefault();const data=Object.fromEntries(fields.map(([key,,type])=>[key,type==='number'?Number(form[key]):form[key]]));let result=await mutate('/api/items',{method:'POST',body:JSON.stringify(data)});if(result)setForm(defaults)};
 const action=async item=>{
  if(meta.id===1){const next=prompt('Set status: Backlog, In Progress, Review, Done',item.status);if(next)await mutate('/api/items/'+item.id+'?status='+encodeURIComponent(next),{method:'PATCH'});}
  if(meta.id===2){const amount=Number(prompt('Quantity to purchase',1));if(amount>0)await mutate('/api/checkout',{method:'POST',body:JSON.stringify({product_id:item.id,quantity:amount})});}
  if(meta.id===3){if(confirm('Cancel this appointment?'))await mutate('/api/items/'+item.id,{method:'PATCH'});}
  if(meta.id===4){const next=prompt('Set stage: Lead, Qualified, Proposal, Negotiation, Won, Lost',item.stage);if(next)await mutate('/api/items/'+item.id+'?stage='+encodeURIComponent(next),{method:'PATCH'});}
  if(meta.id===6){const student=prompt('Student name','Alex Example');if(student)await mutate('/api/enrol',{method:'POST',body:JSON.stringify({course_id:item.id,student})});}
  if(meta.id===9){await mutate('/api/check/'+item.id,{method:'POST'});}
  if(meta.id===10){await mutate('/api/items/'+item.id,{method:'PATCH'});}
 };
 async function searchDocs(e){e.preventDefault();try{setExtra(await request('/api/search?q='+encodeURIComponent(search)))}catch(e){setNotice(e.message)}}
 async function importCSV(e){const file=e.target.files?.[0];if(!file)return;setBusy(true);try{const data=new FormData();data.append('file',file);const r=await fetch(API+'/api/import',{method:'POST',body:data});const result=await r.json();if(!r.ok)throw Error(result.detail||'Upload failed');setNotice(`Imported ${result.imported} records`);await refresh()}catch(e){setNotice(e.message)}finally{setBusy(false);e.target.value=''}}
 async function updatePage(){if(!selected)return;await mutate('/api/items/'+selected.id,{method:'PUT',body:JSON.stringify(selected)});setSelected(null)}
 const actionLabel={1:'Move status',2:'Checkout',3:'Cancel',4:'Change stage',6:'Enrol student',9:'Run check',10:'Toggle publish'}[meta.id];
 const displayFields=fields.map(x=>x[0]).filter(k=>!(k==='body'&&meta.id===5));
 return <div className="shell"><aside className="sidebar"><div className="brand"><span className="brandicon">◈</span><div><b>{meta.title}</b><small>PORTFOLIO / DEMO</small></div></div><nav><a className="active" href="#overview">▦ <span>Overview</span></a><a href="#create">＋ <span>Create new</span></a><a href="#records">▤ <span>Records</span></a><a href="#insights">◈ <span>Advanced tools</span></a><a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">↗ <span>API documentation</span></a></nav><div className="foot">Open-source portfolio starter<br/>FastAPI · React · SQLite</div></aside><main><header><div><span className="eyebrow">WORKSPACE / OVERVIEW</span><h1>{meta.title}</h1><p>{meta.description}</p></div><div className="status"><span className="dot"/> Live local demo</div></header><section className="metrics" id="overview">{metrics.length?metrics.map((m,i)=><article key={i} className="stat"><span>{m.label}</span><strong>{typeof m.value==='number'?m.value.toLocaleString():m.value}</strong><small>Current dataset</small></article>):<article className="stat"><span>Getting started</span><strong>0</strong><small>Create the first record below</small></article>}<article className="stat accent"><span>Current records</span><strong>{items.length}</strong><small>Persisted in local SQLite</small></article></section>
 <ProjectExtras request={request} refresh={refresh}/><div className="columns"><section className="panel" id="create"><div className="panelhead"><div><span className="eyebrow">NEW ENTRY</span><h2>{meta.createTitle}</h2></div><span className="chip">CRUD</span></div><form onSubmit={create}>{fields.map(([key,label,type,initial])=><label key={key}>{label}{type==='textarea'?<textarea value={form[key]||''} onChange={e=>setForm({...form,[key]:e.target.value})} rows="3"/>:type==='select'?<select value={form[key]||''} onChange={e=>setForm({...form,[key]:e.target.value})}>{initial.split('|').slice(1).map(v=><option key={v}>{v}</option>)}</select>:<input required={['title','name','company','patient','doctor','body','url','slug'].includes(key)} type={type} step={type==='number'?'any':undefined} value={form[key]||''} onChange={e=>setForm({...form,[key]:e.target.value})}/>}</label>)}<button disabled={busy} className="primary">{busy?'Working…':'＋ Create record'}</button></form>
 {meta.id===5&&<div className="feature"><h3>Document retrieval</h3><form onSubmit={searchDocs} className="inline"><input placeholder="Search indexed documents" value={search} onChange={e=>setSearch(e.target.value)}/><button>Search</button></form>{extra.map(x=><div className="result" key={x.id}><b>{x.title}</b><p>{x.snippet}</p><small>Source: {x.source||'Local document'}</small></div>)}</div>}
 {meta.id===7&&<div className="feature"><h3>Chat room</h3><input value={room} onChange={e=>setRoom(e.target.value||'general')}/><small>Open this app in two browser tabs to test real-time updates.</small></div>}
 {meta.id===8&&<div className="feature"><h3>CSV import</h3><p>Headers: date, region, product, revenue, units</p><input aria-label="CSV file" type="file" accept=".csv,text/csv" onChange={importCSV}/></div>}
 {meta.id===6&&<div className="feature"><h3>Enrolments</h3>{extra.map(x=><div className="result" key={x.id}>{x.student} · {x.title} <b>{x.completed}/{x.lessons}</b><button onClick={()=>mutate('/api/enrolments/'+x.id,{method:'PATCH'})}>Complete lesson</button></div>)}</div>}
 {meta.id===9&&<div className="feature"><h3>Recent checks</h3>{extra.slice(0,8).map(x=><div className="result" key={x.id}>{x.name} · {x.latency_ms} ms · {x.ok?'Healthy':'Unhealthy'}</div>)}</div>}
 </section><section className="panel records" id="records"><div className="panelhead"><div><span className="eyebrow">DATABASE / COLLECTION</span><h2>{meta.listTitle}</h2></div><span className="chip">{items.length} entries</span></div><div className="search"><input placeholder="Filter visible entries..." value={filter} onChange={e=>setFilter(e.target.value)}/><button onClick={refresh} aria-label="Refresh">↻</button></div><div className="recordlist">{items.filter(x=>JSON.stringify(x).toLowerCase().includes(filter.toLowerCase())).map(item=><div className="record" key={item.id}><div className="rec-top"><b>{item.title||item.name||item.company||item.patient||item.author||item.region||item.slug||item.id}</b><span className="chip">#{item.id}</span></div><dl>{displayFields.slice(0,6).map(k=><React.Fragment key={k}><dt>{k.replaceAll('_',' ')}</dt><dd>{String(item[k]??'—').slice(0,100)}</dd></React.Fragment>)}</dl>{actionLabel&&<button className="secondary" disabled={busy} onClick={()=>action(item)}>{actionLabel} →</button>}{meta.id===10&&<button className="secondary" onClick={()=>setSelected({...item})}>Edit revision</button>}</div>)}{items.length===0&&<div className="empty">No records yet. Use the form to create your first entry.</div>}</div></section></div>{selected&&meta.id===10&&<div className="modal" role="dialog"><div className="modalbox"><h2>New revision: {selected.slug}</h2><label>Title<input value={selected.title} onChange={e=>setSelected({...selected,title:e.target.value})}/></label><label>Body<textarea rows="6" value={selected.body} onChange={e=>setSelected({...selected,body:e.target.value})}/></label><button className="primary" onClick={updatePage}>Save revision</button><button className="secondary" onClick={()=>setSelected(null)}>Close</button></div></div>}{notice&&<div className="toast" role="status" onClick={()=>setNotice('')}>{notice} ✕</div>}<footer>Owner-only portfolio MVP · Use synthetic data only</footer></main></div>
}
createRoot(document.getElementById('root')).render(<AuthGate><App/></AuthGate>);
