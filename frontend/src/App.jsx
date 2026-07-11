import React from 'react';
import FormPanel from './components/FormPanel';
import ChatPanel from './components/ChatPanel';
import './index.css';

function App() {
  return (
    <div className="app-wrapper">
      {/* Top navigation bar */}
      <header className="app-topbar">
        <span className="topbar-logo">🏥 LifeScience CRM</span>
        <div className="topbar-breadcrumb">
          <span>›</span> HCP Module <span>›</span> Log Interaction
        </div>
      </header>

      {/* Main split-screen body */}
      <main className="app-body">
        <FormPanel />
        <ChatPanel />
      </main>
    </div>
  );
}

export default App;
