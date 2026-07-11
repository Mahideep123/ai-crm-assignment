import React, { useState, useRef, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Send, Bot } from 'lucide-react';
import axios from 'axios';
import { logInteraction, editInteraction } from '../store/formSlice';

const API_URL = 'http://localhost:8000/api/chat';

// Keeps only user/assistant messages for history (no system bubbles)
const toApiHistory = (msgs) =>
  msgs
    .filter((m) => m.role === 'user' || m.role === 'assistant')
    .map((m) => ({ role: m.role, content: m.content }));

const ChatPanel = () => {
  const dispatch = useDispatch();
  const [messages, setMessages] = useState([
    {
      id: 'intro',
      role: 'assistant',
      content:
        'Log interaction details here (e.g., "Met Dr. Smith, discussed Prodo-X efficacy, positive sentiment, shared brochure") or ask for help.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addMsg = (msg) =>
    setMessages((prev) => [...prev, { id: Date.now() + Math.random(), ...msg }]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    // Add user bubble
    addMsg({ role: 'user', content: text });
    setInput('');
    setLoading(true);

    try {
      const history = toApiHistory(messages);
      const res = await axios.post(API_URL, { message: text, history });
      const { response, form_updates, action_type } = res.data;

      // Show AI text response
      if (response) addMsg({ role: 'assistant', content: response });

      // Dispatch to Redux if form was updated
      if (form_updates && Object.keys(form_updates).length > 0) {
        if (action_type === 'edit') {
          dispatch(editInteraction(form_updates));
          addMsg({
            role: 'system-edit',
            content: '✏️ Form updated — specific fields have been corrected.',
          });
        } else {
          // "log" or default
          dispatch(logInteraction(form_updates));
          addMsg({
            role: 'system-success',
            content: '✅ Interaction logged! The form on the left has been automatically populated.',
          });
        }
      }
    } catch (err) {
      console.error(err);
      const msg =
        err?.response?.data?.detail ||
        'Could not reach the backend. Make sure the FastAPI server is running on port 8000.';
      addMsg({ role: 'assistant', content: `⚠️ Error: ${msg}` });
    } finally {
      setLoading(false);
    }
  };

  const onKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="panel chat-panel">
      {/* Header */}
      <div className="panel-header">
        <div className="chat-header-inner">
          <div className="chat-header-icon">
            <Bot size={16} />
          </div>
          <div>
            <h2 className="panel-title panel-title-chat">AI Assistant</h2>
            <p className="panel-subtitle">Log interaction details here via chat</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((msg) => {
          if (msg.role === 'system-success') {
            return (
              <div key={msg.id} className="bubble-wrap assistant">
                <div className="bubble system-success">{msg.content}</div>
              </div>
            );
          }
          if (msg.role === 'system-edit') {
            return (
              <div key={msg.id} className="bubble-wrap assistant">
                <div className="bubble system-edit">{msg.content}</div>
              </div>
            );
          }
          return (
            <div key={msg.id} className={`bubble-wrap ${msg.role}`}>
              <div className={`bubble ${msg.role}`}>{msg.content}</div>
            </div>
          );
        })}

        {loading && (
          <div className="bubble-wrap assistant">
            <div className="typing-dots">
              <span /><span /><span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="chat-input-area">
        <input
          className="chat-input"
          placeholder="Describe interaction..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKey}
          disabled={loading}
        />
        <button
          className="send-btn"
          onClick={handleSend}
          disabled={loading || !input.trim()}
          title="Send"
        >
          <Send size={17} />
        </button>
      </div>
    </div>
  );
};

export default ChatPanel;
