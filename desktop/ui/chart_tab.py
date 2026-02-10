"""
Chart tab: Matplotlib Bar and Pie charts for type_distribution.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartTab(QWidget):
    """Matplotlib charts: Bar and Pie for type_distribution."""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        self.fig = Figure(figsize=(12, 10))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self._draw_placeholder()

    def _draw_placeholder(self):
        """Show placeholder when no data."""
        self.fig.clear()
        self.fig.patch.set_facecolor("#0b1020")
        ax = self.fig.add_subplot(111)
        ax.set_facecolor("#0b1020")
        ax.text(0.5, 0.5, 'No chart data. Upload a CSV or load from history.',
                ha='center', va='center', fontsize=12, transform=ax.transAxes)
        ax.texts[0].set_color("#b8b8b8")
        ax.axis('off')
        self.canvas.draw()

    def update_charts(self, summary):
        """
        Update charts: count, avg temperature, avg pressure per equipment type.
        Uses type_stats when available; otherwise type_distribution for count only.
        """
        self.fig.clear()
        self.fig.patch.set_facecolor("#0b1020")

        type_stats = summary.get('type_stats') or {}
        type_dist = summary.get('type_distribution') or {}
        if type_stats:
            labels = list(type_stats.keys())
            counts = [type_stats[t]['count'] for t in labels]
            avg_temps = [type_stats[t]['avg_temperature'] for t in labels]
            avg_pressures = [type_stats[t]['avg_pressure'] for t in labels]
        elif type_dist:
            labels = list(type_dist.keys())
            counts = list(type_dist.values())
            avg_temps = None
            avg_pressures = None
        else:
            self._draw_placeholder()
            return

        palette = [
            "#00d9ff", "#e94560", "#16a085", "#f39c12",
            "#9b59b6", "#1abc9c", "#533483", "#0f3460",
        ]
        colors = [palette[i % len(palette)] for i in range(len(labels))]

        def style_ax(ax):
            ax.set_facecolor("#0b1020")
            ax.tick_params(axis='x', rotation=45)
            ax.tick_params(colors="#b8b8b8")
            ax.spines['bottom'].set_color("#334155")
            ax.spines['left'].set_color("#334155")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(color="#ffffff", alpha=0.08)

        n_plots = 4 if (avg_temps is not None and avg_pressures is not None) else 2
        ax1 = self.fig.add_subplot(2, 2, 1)
        ax2 = self.fig.add_subplot(2, 2, 2)
        ax1.set_facecolor("#0b1020")
        ax2.set_facecolor("#0b1020")

        ax1.bar(labels, counts, color=colors)
        ax1.set_xlabel('Type', color="#b8b8b8")
        ax1.set_ylabel('Count', color="#b8b8b8")
        ax1.set_title('Count by type', color="#00d9ff")
        style_ax(ax1)

        wedges, texts, autotexts = ax2.pie(
            counts,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
        )
        # Make pie labels and percentages readable on dark background
        for txt in list(texts) + list(autotexts):
            txt.set_color("#ffffff")
        ax2.set_title('Share by type', color="#00d9ff")

        if avg_temps is not None and avg_pressures is not None:
            ax3 = self.fig.add_subplot(2, 2, 3)
            ax4 = self.fig.add_subplot(2, 2, 4)
            ax3.set_facecolor("#0b1020")
            ax4.set_facecolor("#0b1020")

            ax3.bar(labels, avg_temps, color=colors)
            ax3.set_xlabel('Type', color="#b8b8b8")
            ax3.set_ylabel('Avg Temperature', color="#b8b8b8")
            ax3.set_title('Avg temperature by type', color="#00d9ff")
            style_ax(ax3)

            ax4.bar(labels, avg_pressures, color=colors)
            ax4.set_xlabel('Type', color="#b8b8b8")
            ax4.set_ylabel('Avg Pressure', color="#b8b8b8")
            ax4.set_title('Avg pressure by type', color="#00d9ff")
            style_ax(ax4)

        self.fig.tight_layout()
        self.canvas.draw()
