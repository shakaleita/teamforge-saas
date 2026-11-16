import React,{useEffect,useState} from 'react';
import './auth.css';
const API=import.meta.env.VITE_API_URL || 'http://localhost:8000';
export default function AuthGate({children}){
 const [state,setState]=useState('loading'),[setup,setSetup]=useState(false),[enabled,setEnabled]=useState(false);
 const [username,setUsername]=useState(''),[password,setPassword]=useState(''),[token,setToken]=useState('');
 const [error,setError]=useState(''),[busy,setBusy]=useState(false),[who,setWho]=useState('');
 const [securityOpen,setSecurityOpen]=useState(false),[currentSecret,setCurrentSecret]=useState(''),[nextSecret,setNextSecret]=useState('');
 const [securityError,setSecurityError]=useState(''),[securityNotice,setSecurityNotice]=useState('');
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
 async function changePassword(e){e.preventDefault();setBusy(true);setSecurityError('');
  try{
   const r=await fetch(API+'/api/auth/change-password',{method:'POST',credentials:'include',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({current_password:currentSecret,new_password:nextSecret})});
   const data=await r.json().catch(()=>({}));
   if(!r.ok)throw Error(data.detail||'Password change failed');
   setCurrentSecret('');setNextSecret('');setSecurityOpen(false);setState('login');
   setSecurityNotice('Password changed. All sessions were revoked. Sign in with your new password.');
  }catch(e){setSecurityError(e.message)}finally{setBusy(false)}
 }
 async function logout(){setBusy(true);setSecurityError('');
  try{const r=await fetch(API+'/api/auth/logout',{method:'POST',credentials:'include'});
   if(!r.ok)throw Error('Could not revoke this session');
   setState('login');setWho('');setPassword('');setSecurityOpen(false);
   setCurrentSecret('');setNextSecret('');
  }catch(e){setSecurityOpen(true);setSecurityError(e.message)}
  finally{setBusy(false)}
 }
 if(state==='loading')return <div className="auth-page">Connecting to the local workspace…</div>;
 if(state==='ready')return <div className="auth-shell">{children}
  <div className="auth-user">Signed in as <b>{who}</b>
   <button type="button" disabled={busy} onClick={()=>{setSecurityOpen(v=>!v);setSecurityError('')}}>Account security</button>
   <button type="button" disabled={busy} onClick={logout}>Sign out</button>
  </div>
  {securityOpen&&<section className="auth-security" aria-label="Account security">
   <h2>Protect your account</h2>
   <p>Changing your password signs out every device, including this one.</p>
   <form onSubmit={changePassword}>
    <label>Current password<input type="password" required autoComplete="current-password"
     value={currentSecret} onChange={e=>setCurrentSecret(e.target.value)}/></label>
    <label>New password<input type="password" required minLength={12} maxLength={128}
     autoComplete="new-password" value={nextSecret} onChange={e=>setNextSecret(e.target.value)}/></label>
    {securityError&&<p role="alert" className="auth-error">{securityError}</p>}
    <div className="auth-security-actions">
     <button type="submit" disabled={busy}>{busy?'Updating…':'Change password'}</button>
     <button type="button" onClick={()=>{setSecurityOpen(false);setCurrentSecret('');setNextSecret('')}}>Close</button>
    </div>
   </form>
  </section>}
 </div>;
 return <div className="auth-page"><form className="auth-panel" onSubmit={send}>
  <div className="auth-emblem">◇</div><small>CONTROLLED DEMO ACCESS</small><h1>{setup?'Secure owner setup':'Welcome back'}</h1>
  <p>{setup?'Enter your one-time server setup token to create the first owner account.':'Sign in to your local portfolio workspace.'}</p>
  <label>Username<input required autoComplete="username" minLength={3} value={username} onChange={e=>setUsername(e.target.value)}/></label>
  <label>Password<input type="password" required minLength={10} autoComplete={setup?'new-password':'current-password'} value={password} onChange={e=>setPassword(e.target.value)}/></label>
  {setup&&<label>One-time setup token<input required type="password" autoComplete="off" value={token} onChange={e=>setToken(e.target.value)} placeholder="OWNER_SETUP_TOKEN"/></label>}
  {setup&&!enabled&&<p role="alert">Owner setup is disabled until the server administrator configures OWNER_SETUP_TOKEN.</p>}
  {error&&<p role="alert" className="auth-error">{error}</p>}
  {securityNotice&&<p role="status">{securityNotice}</p>}
  <button disabled={busy||(setup&&!enabled)}>{busy?'Working…':setup?'Create owner account':'Sign in'}</button>
  <small>Local demonstration · synthetic data only</small>
 </form></div>
}
