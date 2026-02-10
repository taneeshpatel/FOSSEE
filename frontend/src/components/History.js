import React, { useState, useEffect } from 'react';
import api from '../api/axios';

/**
 * History component: lists last 5 uploads with Load button.
 * On Load, fetches dataset and summary, updates parent via onLoadDataset.
 */
function History({ onLoadDataset }) {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchDatasets = async () => {
    setError('');
    setLoading(true);
    try {
      const res = await api.get('/api/datasets/');
      setDatasets(res.data || []);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  const handleLoad = async (datasetId) => {
    setError('');
    try {
      const [dataRes, summaryRes] = await Promise.all([
        api.get(`/api/datasets/${datasetId}/`),
        api.get(`/api/summary/${datasetId}/`),
      ]);
      const rawData = dataRes.data.raw_data || [];
      const summaryData = summaryRes.data;
      onLoadDataset(rawData, summaryData, datasetId);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load dataset');
    }
  };

  return (
    <section className="section">
      <h3>History</h3>
      {error && <div className="auth-error" style={{ marginBottom: 12 }}>{error}</div>}
      <button
        className="logout-btn"
        style={{ background: 'rgba(255,255,255,0.2)', marginBottom: 16 }}
        onClick={fetchDatasets}
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Refresh'}
      </button>
      {datasets.length === 0 ? (
        <p style={{ color: '#b8b8b8' }}>No uploads yet.</p>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>File Name</th>
                <th>Uploaded At</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {datasets.map((ds) => (
                <tr key={ds.id}>
                  <td>{ds.file_name}</td>
                  <td>{new Date(ds.uploaded_at).toLocaleString()}</td>
                  <td>
                    <button
                      className="logout-btn"
                      style={{ background: '#00d9ff', color: '#1a1a2e', padding: '6px 12px' }}
                      onClick={() => handleLoad(ds.id)}
                    >
                      Load
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default History;
