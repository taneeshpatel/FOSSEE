import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const CHART_COLORS = [
  '#00d9ff',
  '#e94560',
  '#0f3460',
  '#533483',
  '#16a085',
  '#f39c12',
  '#9b59b6',
  '#1abc9c',
];

/**
 * Charts: per equipment type — Count, Avg Temperature, Avg Pressure.
 * Uses type_stats when available; falls back to type_distribution for count-only.
 */
function Charts({ summary }) {
  const typeStats = summary?.type_stats && Object.keys(summary.type_stats).length > 0
    ? summary.type_stats
    : null;
  const typeDist = summary?.type_distribution || {};
  const hasCounts = typeStats || (Object.keys(typeDist).length > 0);

  if (!summary || !hasCounts) {
    return (
      <section className="section">
        <h3>Charts</h3>
        <p style={{ color: '#b8b8b8' }}>No chart data. Upload a CSV or load from history.</p>
      </section>
    );
  }

  const labels = typeStats ? Object.keys(typeStats) : Object.keys(typeDist);
  const counts = typeStats
    ? labels.map((t) => typeStats[t].count)
    : labels.map((t) => typeDist[t]);
  const avgTemps = typeStats ? labels.map((t) => typeStats[t].avg_temperature) : null;
  const avgPressures = typeStats ? labels.map((t) => typeStats[t].avg_pressure) : null;

  const total = counts.reduce((a, b) => a + b, 0);
  const percentages = total ? counts.map((v) => Math.round((v / total) * 100)) : [];

  const barOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { labels: { color: '#e8e8e8' } },
    },
    scales: {
      x: {
        ticks: { color: '#b8b8b8' },
        grid: { color: 'rgba(255,255,255,0.1)' },
      },
      y: {
        ticks: { color: '#b8b8b8' },
        grid: { color: 'rgba(255,255,255,0.1)' },
      },
    },
  };

  const countBarData = {
    labels,
    datasets: [
      {
        label: 'Count',
        data: counts,
        backgroundColor: labels.map((_, i) => CHART_COLORS[i % CHART_COLORS.length]),
      },
    ],
  };

  const pieData = {
    labels,
    datasets: [
      {
        data: counts,
        backgroundColor: labels.map((_, i) => CHART_COLORS[i % CHART_COLORS.length]),
        borderColor: 'rgba(255,255,255,0.2)',
        borderWidth: 1,
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { labels: { color: '#e8e8e8' } },
      tooltip: {
        callbacks: {
          label: (ctx) => {
            const pct = percentages[ctx.dataIndex];
            return `${ctx.label}: ${ctx.raw} (${pct}%)`;
          },
        },
      },
    },
  };

  const tempBarData = avgTemps && {
    labels,
    datasets: [
      {
        label: 'Avg Temperature',
        data: avgTemps,
        backgroundColor: labels.map((_, i) => CHART_COLORS[i % CHART_COLORS.length]),
      },
    ],
  };

  const pressureBarData = avgPressures && {
    labels,
    datasets: [
      {
        label: 'Avg Pressure',
        data: avgPressures,
        backgroundColor: labels.map((_, i) => CHART_COLORS[i % CHART_COLORS.length]),
      },
    ],
  };

  return (
    <section className="section">
      <h3>Charts by equipment type</h3>
      <div className="charts-container">
        <div className="chart-wrapper">
          <h4 style={{ color: '#b8b8b8', marginBottom: 12 }}>Count by type</h4>
          <Bar data={countBarData} options={barOptions} />
        </div>
        <div className="chart-wrapper">
          <h4 style={{ color: '#b8b8b8', marginBottom: 12 }}>Share by type</h4>
          <Pie data={pieData} options={pieOptions} />
        </div>
        {tempBarData && (
          <div className="chart-wrapper">
            <h4 style={{ color: '#b8b8b8', marginBottom: 12 }}>Avg temperature by type</h4>
            <Bar data={tempBarData} options={barOptions} />
          </div>
        )}
        {pressureBarData && (
          <div className="chart-wrapper">
            <h4 style={{ color: '#b8b8b8', marginBottom: 12 }}>Avg pressure by type</h4>
            <Bar data={pressureBarData} options={barOptions} />
          </div>
        )}
      </div>
    </section>
  );
}

export default Charts;
