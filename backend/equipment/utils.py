"""
Utility functions for CSV parsing, summary computation, and PDF generation.
"""
import io
from typing import Dict, Any

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']


def parse_csv(uploaded_file) -> pd.DataFrame:
    """
    Parse uploaded CSV file using Pandas.
    - Strips column whitespace
    - Drops empty rows
    - Validates required columns exist
    Raises ValueError if columns are missing.
    """
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    return df


def compute_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute summary statistics from the DataFrame.
    Returns dict with total_count, avg_flowrate, avg_pressure, avg_temperature,
    type_distribution (count per type), and type_stats (per-type count, avg_temperature, avg_pressure).
    """
    total_count = float(len(df))
    avg_flowrate = round(df['Flowrate'].mean(), 2) if total_count > 0 else 0.0
    avg_pressure = round(df['Pressure'].mean(), 2) if total_count > 0 else 0.0
    avg_temperature = round(df['Temperature'].mean(), 2) if total_count > 0 else 0.0
    type_distribution = df['Type'].value_counts().to_dict()

    # Per-type stats: count, avg_temperature, avg_pressure for each equipment type
    type_stats = {}
    for eq_type in df['Type'].dropna().unique():
        sub = df[df['Type'] == eq_type]
        type_stats[str(eq_type)] = {
            'count': int(len(sub)),
            'avg_temperature': round(sub['Temperature'].mean(), 2),
            'avg_pressure': round(sub['Pressure'].mean(), 2),
        }

    return {
        'total_count': total_count,
        'avg_flowrate': avg_flowrate,
        'avg_pressure': avg_pressure,
        'avg_temperature': avg_temperature,
        'type_distribution': type_distribution,
        'type_stats': type_stats,
    }


def compute_type_stats_from_raw_data(raw_data: list) -> Dict[str, Dict[str, Any]]:
    """
    Compute type_stats (count, avg_temperature, avg_pressure per type) from
    raw_data list of dicts. Used for older datasets that don't have type_stats saved.
    """
    if not raw_data:
        return {}
    df = pd.DataFrame(raw_data)
    # Normalize column names (could be 'Temperature' or 'Pressure' from CSV)
    col_map = {c: c.strip() for c in df.columns}
    df = df.rename(columns=col_map)
    for col in ['Type', 'Temperature', 'Pressure']:
        if col not in df.columns:
            return {}
    type_stats = {}
    for eq_type in df['Type'].dropna().unique():
        sub = df[df['Type'] == eq_type]
        type_stats[str(eq_type)] = {
            'count': int(len(sub)),
            'avg_temperature': round(float(sub['Temperature'].mean()), 2),
            'avg_pressure': round(float(sub['Pressure'].mean()), 2),
        }
    return type_stats


def generate_pdf(dataset, summary) -> io.BytesIO:
    """
    Generate a PDF report using ReportLab.
    Includes title, file name, upload date, summary stats, and type distribution table.
    Returns a BytesIO buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
    )

    elements = []
    elements.append(Paragraph("Chemical Equipment Parameter Report", title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>File Name:</b> {dataset.file_name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
    elements.append(Paragraph(f"Total Equipment Count: {summary.total_count}", styles['Normal']))
    elements.append(Paragraph(f"Average Flowrate: {summary.avg_flowrate}", styles['Normal']))
    elements.append(Paragraph(f"Average Pressure: {summary.avg_pressure}", styles['Normal']))
    elements.append(Paragraph(f"Average Temperature: {summary.avg_temperature}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Per equipment type (Count, Avg Temp, Avg Pressure)</b>", styles['Heading2']))
    type_stats = getattr(summary, 'type_stats', None) or {}
    if type_stats:
        type_data = [['Type', 'Count', 'Avg Temperature', 'Avg Pressure']]
        for t, s in type_stats.items():
            type_data.append([str(t), str(s.get('count', '')), str(s.get('avg_temperature', '')), str(s.get('avg_pressure', ''))])
    else:
        type_data = [['Type', 'Count']]
        for t, c in summary.type_distribution.items():
            type_data.append([str(t), str(c)])
    table = Table(type_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
