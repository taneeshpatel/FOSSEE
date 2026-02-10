import React from 'react';
import api from '../api/axios';

/**
 * Summary component: displays stats and Download PDF button.
 */
function Summary({ summary, datasetId }) {
  const [pdfLoading, setPdfLoading] = React.useState(false);
  const [pdfError, setPdfError] = React.useState('');

  const handleDownloadPdf = async () => {
    if (!datasetId) return;
    setPdfError('');
    setPdfLoading(true);
    try {
      const res = await api.get(`/api/pdf/${datasetId}/`, {
        responseType: 'blob',
      });
      const url = URL.createObjectURL(res.data);
      const a = document.createElement('a');
      a.href = url;
      a.download = `report_${datasetId}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setPdfError('Failed to download PDF');
    } finally {
      setPdfLoading(false);
    }
  };

  if (!summary) {
    return (
      <section className="section">
        <h3>Summary</h3>
        <p style={{ color: '#b8b8b8' }}>No summary available. Upload a CSV or load from history.</p>
      </section>
    );
  }

  return (
    <section className="section">
      <h3>Summary</h3>
      <div className="summary-cards">
        <div className="summary-card">
          <span className="summary-label">Total Equipment Count</span>
          <span className="summary-value">{summary.total_count}</span>
        </div>
        <div className="summary-card">
          <span className="summary-label">Avg Flowrate</span>
          <span className="summary-value">{summary.avg_flowrate}</span>
        </div>
        <div className="summary-card">
          <span className="summary-label">Avg Pressure</span>
          <span className="summary-value">{summary.avg_pressure}</span>
        </div>
        <div className="summary-card">
          <span className="summary-label">Avg Temperature</span>
          <span className="summary-value">{summary.avg_temperature}</span>
        </div>
      </div>
      {datasetId && (
        <div style={{ marginTop: 16 }}>
          <button
            className="logout-btn"
            style={{ background: '#00d9ff', color: '#1a1a2e' }}
            onClick={handleDownloadPdf}
            disabled={pdfLoading}
          >
            {pdfLoading ? 'Downloading...' : 'Download PDF Report'}
          </button>
          {pdfError && <div className="auth-error" style={{ marginTop: 8 }}>{pdfError}</div>}
        </div>
      )}
    </section>
  );
}

export default Summary;
