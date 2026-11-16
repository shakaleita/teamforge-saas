import React,{useEffect,useState} from 'react';
import './auth.css';
const API=import.meta.env.VITE_API_URL || 'http://localhost:8000';
export default function AuthGate({children}){
 const [state,setState]=useState('loading'),[setup,setSetup]=useState(false),[enabled,setEnabled]=useState(false);
 const [username,setUsername]=useState(''),[password,setPassword]=useState(''),[token,setToken]=useState('');
 const [error,setError]=useState(''),[busy,setBusy]=useState(false),[who,setWho]=useState('');
 useEffect(()=>{let alive=true;(async()=>{try{
  const me=await fetch(API+'/api/auth/me',{credentials:'include'});
  if(me.ok){const u=await me.json();if(alive){setWho(u.username);setState('ready')}return}
  const r=await fetch(API+'/api/auth/setup');if(!r.ok)throw Error('Authentication API unavailable');
  const d=await r.json();if(alive){setSetup(d.needs_setup);setEnabled(d.bootstrap_enabled);setState('login')}
 }catch(e){if(alive){setError(e.message);setState('login')}}})();return()=>{alive=false}},[]);
 async function send(e){e.preventDefault();setBusy(true);setError('');
  try{if(setup){const r=await fetch(API+'/api/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'include',body:JSON.stringify({username,password,setup_token:token})});const j=await r.json();if(!r.ok)throw Error(j.detail||'Setup failed');setSetup(false);setToken('')}
   const r=await fetch(API+'/api/auth/login',{method:'POST',credentials:'include',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});
   const j=await r.json();if(!r.ok)throw Error(j.detail||'Login failed');setWho(j.username);setPassword('');setState('ready')
  }catch(e){setError(e.message)}finally{setBusy(false)}
 }
 async function logout(){await fetch(API+'/api/auth/logout',{method:'POST',credentials:'include'}).catch(()=>{});setState('login');setPassword('')}
 if(state==='loading')return <div className="auth-page">Connecting to the local workspace…</div>;
 if(state==='ready')return <div className="auth-shell">{children}<div className="auth-user">Signed in as {who} <button onClick={logout}>Sign out</button></div></div>;
 return <div className="auth-page"><form className="auth-panel" onSubmit={send}>
  <div className="auth-emblem">◇</div><small>CONTROLLED DEMO ACCESS</small><h1>{setup?'Secure owner setup':'Welcome back'}</h1>
  <p>{setup?'Enter your one-time server setup token to create the first owner account.':'Sign in to your local portfolio workspace.'}</p>
  <label>Username<input required autoComplete="username" minLength={3} value={username} onChange={e=>setUsername(e.target.value)}/></label>
  <label>Password<input type="password" required minLength={10} autoComplete={setup?'new-password':'current-password'} value={password} onChange={e=>setPassword(e.target.value)}/></label>
  {setup&&<label>One-time setup token<input required type="password" autoComplete="off" value={token} onChange={e=>setToken(e.target.value)} placeholder="OWNER_SETUP_TOKEN"/></label>}
  {setup&&!enabled&&<p role="alert">Owner setup is disabled until the server administrator configures OWNER_SETUP_TOKEN.</p>}
  {error&&<p role="alert" className="auth-error">{error}</p>}
  <button disabled={busy||(setup&&!enabled)}>{busy?'Working…':setup?'Create owner account':'Sign in'}</button>
  <small>Local demonstration · synthetic data only</small>
 </form></div>
}
