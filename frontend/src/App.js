import React, { useState, useEffect } from 'react';
import api from './api/axios';
import Login from './components/Login';
import Register from './components/Register';
import Upload from './components/Upload';
import DataTable from './components/DataTable';
import Charts from './components/Charts';
import Summary from './components/Summary';
import History from './components/History';

/**
 * Main App component.
 * Manages authentication state and shared data (currentData, currentSummary).
 */
function App() {
  useEffect(() => {
    api.get('/api/auth/csrf/').catch(() => {});
  }, []);

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [currentData, setCurrentData] = useState([]);
  const [currentSummary, setCurrentSummary] = useState(null);
  const [currentDatasetId, setCurrentDatasetId] = useState(null);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    setShowRegister(false);
  };

  const handleLogout = async () => {
    try {
      await api.post('/api/auth/logout/');
    } catch (err) {
      console.error('Logout error:', err);
    }
    setIsLoggedIn(false);
    setCurrentData([]);
    setCurrentSummary(null);
    setCurrentDatasetId(null);
  };

  const handleDataLoaded = (data, summary, datasetId) => {
    setCurrentData(data || []);
    setCurrentSummary(summary || null);
    setCurrentDatasetId(datasetId || null);
  };

  if (!isLoggedIn) {
    if (showRegister) {
      return (
        <Register
          onLoginSuccess={handleLoginSuccess}
          onSwitchToLogin={() => setShowRegister(false)}
        />
      );
    }
    return (
      <Login
        onLoginSuccess={handleLoginSuccess}
        onSwitchToRegister={() => setShowRegister(true)}
      />
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Chemical Equipment Parameter Visualizer</h1>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <main className="main-content">
        <Upload onDataLoaded={handleDataLoaded} />
        <Summary
          summary={currentSummary}
          datasetId={currentDatasetId}
        />
        <DataTable data={currentData} />
        <Charts summary={currentSummary} />
        <History onLoadDataset={handleDataLoaded} />
      </main>
    </div>
  );
}

export default App;
