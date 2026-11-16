import React, {useEffect, useState} from 'react';

const CONFIG = {
  "title": "Task activity feed",
  "description": "Follow the lifecycle of task creation, changes and deletion within a workspace.",
  "endpoint": "/api/activity",
  "auto": true,
  "fields": [
    [
      "workspace",
      "Workspace (optional)",
      "text"
    ],
    [
      "limit",
      "Maximum events",
      "number"
    ]
  ]
};
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function describe(key) {
  return key.replaceAll('_',' ').replace(/\b\w/g, c => c.toUpperCase());
}
function createPath(pattern, fields, allowedQuery) {
  const path = pattern.replace(/\{(\w+)\}/g, (_, key) => {
    if (!String(fields[key] ?? '').trim()) throw new Error(`Please provide ${describe(key)}`);
    return encodeURIComponent(fields[key]);
  });
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(fields)) {
    if (allowedQuery.includes(key) && String(value ?? '').trim()) params.set(key, String(value));
  }
  return path + (params.size ? `?${params}` : '');
}
function DataCard({item}) {
  const pairs = Object.entries(item).filter(([key])=>key !== 'body').slice(0, 9);
  return <article className="insight-card"><dl>
    {pairs.map(([key,value])=><React.Fragment key={key}><dt>{describe(key)}</dt><dd>{value === null ? '—' : typeof value === 'object' ? JSON.stringify(value) : String(value)}</dd></React.Fragment>)}
  </dl></article>;
}
function Result({data}) {
  if (data === null) return null;
  if (Array.isArray(data)) return <div className="insight-results">{data.length ? data.slice(0,30).map((item,i)=><DataCard key={item.id??i} item={item}/>) : <p className="insight-empty">No matching records yet.</p>}</div>;
  return <div className="insight-results"><DataCard item={data}/></div>;
}
function FieldSet({fields, values, update}) {
  return fields.map(([key,label,type])=><label key={key} className="insight-field">{label}
    {type==='textarea' ? <textarea rows="3" value={values[key]||''} onChange={e=>update(key,e.target.value)} /> :
     <input type={type} value={values[key]??''} onChange={e=>update(key,e.target.value)} />}
  </label>);
}
export default function ProjectExtras({request,refresh}) {
  const [filters,setFilters]=useState({});
  const [actionFields,setActionFields]=useState({});
  const [data,setData]=useState(null);
  const [result,setResult]=useState(null);
  const [status,setStatus]=useState('');
  const [loading,setLoading]=useState(false);
  const update=(setter)=>(key,value)=>setter(previous=>({...previous,[key]:value}));
  async function load(e){
    e?.preventDefault(); setLoading(true);setStatus('');
    try {
      const path=createPath(CONFIG.endpoint,filters,CONFIG.fields.map(([key])=>key));
      setData(await request(path));
    } catch(err) {setStatus(`Unable to load: ${err.message}`);} finally {setLoading(false);}
  }
  async function perform(e) {
    e.preventDefault(); setLoading(true);setStatus('');
    try {
      const action=CONFIG.action;
      const body=Object.fromEntries((action.body||[]).map(key=>[key,actionFields[key]]));
      const url=createPath(action.endpoint,actionFields,action.method==='GET'?action.fields.map(([key])=>key):[]);
      const options=action.method==='GET'?{}:{method:action.method,...(action.body.length?{body:JSON.stringify(body)}:{})};
      const response=await request(url,options);
      setResult(response || {status:'Completed'});setStatus('Operation completed.');
      await refresh();
      if (CONFIG.auto) await load();
    } catch(err) {setStatus(`Action failed: ${err.message}`);} finally {setLoading(false);}
  }
  useEffect(()=>{if(CONFIG.auto){load();}},[]);
  return <section className="panel enhancements" id="insights" aria-label="Advanced project tools">
    <div className="panelhead"><div><span className="eyebrow">ADVANCED TOOLS / VERSION 0.3</span><h2>{CONFIG.title}</h2><p className="insight-description">{CONFIG.description}</p></div><span className="chip">Live API</span></div>
    <form className="insight-form" onSubmit={load}>
      <div className="insight-inputs"><FieldSet fields={CONFIG.fields} values={filters} update={update(setFilters)}/></div>
      <button className="secondary" type="submit" disabled={loading}>{loading?'Loading…':'View report'}</button>
      {CONFIG.export&&<a className="insight-export" href={API+CONFIG.export} download>Download CSV</a>}
    </form>
    <Result data={data}/>
    {CONFIG.action&&<div className="insight-action"><h3>{CONFIG.action.title}</h3><form onSubmit={perform} className="insight-form"><div className="insight-inputs"><FieldSet fields={CONFIG.action.fields} values={actionFields} update={update(setActionFields)}/></div><button className="secondary" disabled={loading} type="submit">{loading?'Working…':'Run action'}</button></form><Result data={result}/></div>}
    {status&&<p role="status" className="insight-status">{status}</p>}
  </section>;
}
