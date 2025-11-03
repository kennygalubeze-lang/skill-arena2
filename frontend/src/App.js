
import React, {useEffect, useState} from 'react';
import axios from 'axios';
export default function App(){ 
  const [health, setHealth] = useState(null);
  const [lounges, setLounges] = useState([]);
  const [support, setSupport] = useState({});
  useEffect(()=>{ 
    axios.get('/api/health').then(r=>setHealth(r.data)).catch(()=>{});
    axios.get('/api/lounges').then(r=>setLounges(r.data)).catch(()=>{});
    axios.get('/api/support').then(r=>setSupport(r.data)).catch(()=>{});
  },[]);
  return (<div className='app'>
    <header className='header'><h1>🎮 SkillArena</h1><p>Skill-based competitive gaming</p></header>
    <main>
      {health && <div className='card'>Server: <strong>{'{'}health.app{'}'}</strong></div>}
      <section><h2>Lounges</h2><ul>{'{'}lounges.map(l=>(<li key={'{'}l.id{'}'}><strong>{'{'}l.name{'}'}</strong> — Entry: {'{'}l.min_entry{'}'} {'{'}l.currency{'}'}</li>)){'}'}</ul></section>
      <section><h2>Support</h2><p>WhatsApp: {'{'}support.whatsapp{'}'}</p><p>Call: {'{'}support.call{'}'}</p><p>Email: {'{'}support.email{'}'}</p></section>
    </main>
    <footer>Support: WhatsApp +2347011695248 | Call +2347053070533 | Email kennygalubeze@gmail.com</footer>
  </div>); }
