import React, { useState, useRef } from 'react';
import api from '../api/axios';

/**
 * Upload component: file input and upload button.
 * On success, fetches full dataset and summary, updates parent via onDataLoaded.
 */
function Upload({ onDataLoaded }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0];
    setFile(selected || null);
    setError('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a CSV file');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const uploadRes = await api.post('/api/upload/', formData);

      const { dataset_id, summary } = uploadRes.data;

      // Fetch full dataset and summary
      const [dataRes, summaryRes] = await Promise.all([
        api.get(`/api/datasets/${dataset_id}/`),
        api.get(`/api/summary/${dataset_id}/`),
      ]);

      const rawData = dataRes.data.raw_data || [];
      const summaryData = summaryRes.data;

      onDataLoaded(rawData, summaryData, dataset_id);
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      const msg = err.response?.data?.error
        || err.response?.data?.detail
        || err.message
        || 'Upload failed';
      setError(Array.isArray(msg) ? msg.join(', ') : String(msg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="section">
      <h3>Upload CSV</h3>
      {error && <div className="auth-error" style={{ marginBottom: 12 }}>{error}</div>}
      <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <button
          className="logout-btn"
          style={{ background: 'rgba(255,255,255,0.2)', color: '#e8e8e8' }}
          onClick={() => fileInputRef.current && fileInputRef.current.click()}
        >
          {file ? 'Change CSV File' : 'Select CSV File'}
        </button>
        <button
          className="logout-btn"
          style={{ background: '#00d9ff', color: '#1a1a2e' }}
          onClick={handleUpload}
          disabled={loading || !file}
        >
          {loading ? 'Submitting...' : 'Submit'}
        </button>
      </div>
      {file && <div style={{ marginTop: 8, color: '#b8b8b8' }}>Selected: {file.name}</div>}
    </section>
  );
}

export default Upload;
