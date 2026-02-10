import React from 'react';

/**
 * DataTable component: renders equipment data in a table.
 * Columns: Equipment Name, Type, Flowrate, Pressure, Temperature.
 */
function DataTable({ data }) {
  if (!data || data.length === 0) {
    return (
      <section className="section">
        <h3>Data Table</h3>
        <p style={{ color: '#b8b8b8' }}>No data loaded. Upload a CSV or load from history.</p>
      </section>
    );
  }

  return (
    <section className="section">
      <h3>Data Table</h3>
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr key={idx}>
                <td>{row['Equipment Name'] ?? row.equipment_name ?? '-'}</td>
                <td>{row['Type'] ?? row.type ?? '-'}</td>
                <td>{row['Flowrate'] ?? row.flowrate ?? '-'}</td>
                <td>{row['Pressure'] ?? row.pressure ?? '-'}</td>
                <td>{row['Temperature'] ?? row.temperature ?? '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default DataTable;
