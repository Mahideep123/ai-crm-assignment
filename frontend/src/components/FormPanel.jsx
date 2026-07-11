import React, { useState, useCallback } from 'react';
import { useSelector } from 'react-redux';
import { Search, Plus, Mic } from 'lucide-react';

// Tracks which fields just got updated so we can animate them
const useUpdatedFields = (formData) => {
  const [updatedKeys, setUpdatedKeys] = React.useState([]);
  const prevRef = React.useRef(formData);

  React.useEffect(() => {
    const changed = Object.keys(formData).filter(
      (k) => formData[k] !== prevRef.current[k] && formData[k]
    );
    if (changed.length) {
      setUpdatedKeys(changed);
      const t = setTimeout(() => setUpdatedKeys([]), 1900);
      prevRef.current = formData;
      return () => clearTimeout(t);
    }
    prevRef.current = formData;
  }, [formData]);

  return updatedKeys;
};

const FormPanel = () => {
  const formData = useSelector((s) => s.form);
  const updatedKeys = useUpdatedFields(formData);

  const cls = (field) => {
    let c = 'form-control';
    if (formData[field]) c += ' has-value';
    if (updatedKeys.includes(field)) c += ' just-updated';
    return c;
  };

  const sentiment = formData.sentiment?.toLowerCase() || '';

  return (
    <div className="panel form-panel">
      {/* Header */}
      <div className="panel-header">
        <h1 className="panel-title">Log HCP Interaction</h1>
        <p className="panel-subtitle">Interaction Details</p>
      </div>

      <div className="form-body">
        {/* ── Basic Info ── */}
        <p className="section-title">Interaction Details</p>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">HCP Name</label>
            <input
              className={cls('hcp_name')}
              type="text"
              placeholder="Search or select HCP..."
              value={formData.hcp_name}
              readOnly
            />
          </div>
          <div className="form-group">
            <label className="form-label">Interaction Type</label>
            <select className={`form-control form-select ${formData.interaction_type ? 'has-value' : ''} ${updatedKeys.includes('interaction_type') ? 'just-updated' : ''}`} value={formData.interaction_type} disabled>
              <option value="Meeting">Meeting</option>
              <option value="Call">Call</option>
              <option value="Email">Email</option>
              <option value="Conference">Conference</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Date</label>
            <input
              className={cls('date')}
              type="text"
              placeholder="MM/DD/YYYY"
              value={formData.date}
              readOnly
            />
          </div>
          <div className="form-group">
            <label className="form-label">Time</label>
            <input
              className={cls('time')}
              type="text"
              placeholder="HH:MM AM/PM"
              value={formData.time}
              readOnly
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Attendees</label>
            <input
              className={cls('attendees')}
              type="text"
              placeholder="Enter names or search..."
              value={formData.attendees}
              readOnly
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Topics Discussed</label>
            <textarea
              className={`${cls('topics')} form-textarea`}
              placeholder="Enter key discussion points..."
              value={formData.topics}
              readOnly
            />
            <div style={{ marginTop: '6px' }}>
              <span style={{ fontSize: '0.78rem', color: '#0f62fe', display:'flex', alignItems:'center', gap:'4px' }}>
                <Mic size={13} /> Summarize from Voice Note <span style={{color:'#a8a8a8'}}>(Requires Consent)</span>
              </span>
            </div>
          </div>
        </div>

        {/* ── Materials ── */}
        <p className="section-title">Materials Shared / Samples Distributed</p>

        <div style={{ marginBottom: '1rem' }}>
          <label className="form-label" style={{ marginBottom: '0.5rem', display: 'block' }}>Materials Shared</label>
          <div className={`materials-row ${updatedKeys.includes('materials') ? 'just-updated' : ''}`}>
            {formData.materials
              ? <span className="materials-value">{formData.materials}</span>
              : <span className="materials-empty">No materials added.</span>
            }
            <button className="btn-link"><Search size={13} /> Search/Add</button>
          </div>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label className="form-label" style={{ marginBottom: '0.5rem', display: 'block' }}>Samples Distributed</label>
          <div className={`materials-row ${updatedKeys.includes('samples') ? 'just-updated' : ''}`}>
            {formData.samples
              ? <span className="materials-value">{formData.samples}</span>
              : <span className="materials-empty">No samples added.</span>
            }
            <button className="btn-link"><Plus size={13} /> Add Sample</button>
          </div>
        </div>

        {/* ── Sentiment ── */}
        <p className="section-title">Observed / Inferred HCP Sentiment</p>

        <div className="sentiment-row" style={{ marginBottom: '1.5rem' }}>
          {['Positive', 'Neutral', 'Negative'].map((s) => {
            const key = s.toLowerCase();
            const activeClass =
              sentiment === key
                ? key === 'positive' ? 'active-positive'
                  : key === 'negative' ? 'active-negative'
                  : 'active-neutral'
                : '';
            const emoji = s === 'Positive' ? '😀' : s === 'Neutral' ? '😐' : '😞';
            return (
              <div key={s} className={`sentiment-option ${activeClass} ${updatedKeys.includes('sentiment') && sentiment === key ? 'just-updated' : ''}`}>
                {emoji} {s}
              </div>
            );
          })}
        </div>

        {/* ── Outcomes & Follow-up ── */}
        <p className="section-title">Outcomes & Follow-up</p>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Outcomes</label>
            <textarea
              className={`${cls('outcomes')} form-textarea`}
              placeholder="Key outcomes or agreements..."
              value={formData.outcomes}
              readOnly
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Follow-up Actions</label>
            <textarea
              className={`${cls('follow_up')} form-textarea`}
              placeholder="Suggested follow-up tasks..."
              value={formData.follow_up}
              readOnly
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FormPanel;
