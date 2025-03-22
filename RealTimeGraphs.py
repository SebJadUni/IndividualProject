#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
from collections import deque  # For buffering last 100 data points
from PyQt5.QtWidgets import QWidget, QVBoxLayout  # For GUI layout and widget container
import pyqtgraph as pg  # For real-time plotting
from pyqtgraph import ScatterPlotItem               # NEW*******************************
from PyQt5.QtGui import QFont, QPen
#---------------------------------------------------------------------------------------------
# Class - Graph Container
#---------------------------------------------------------------------------------------------

class GraphContainer(QWidget):
    """Encapsulates the real-time graph functionality as an independent UI component."""

    def __init__(self, title="Real-Time IMU Data", y_label="Unknown_Data"):
        super().__init__()

        # Buffers to store the last 100 data points for each parameter
        self.yaw_buffer = deque([0.0] * 100, maxlen=100)
        self.pitch_buffer = deque([0.0] * 100, maxlen=100)
        self.roll_buffer = deque([0.0] * 100, maxlen=100)

        #NEW ****************************************************************
        # self.anomaly_buffer = deque([0.0] * 100, maxlen=100)
        self.anomaly_buffer_dot = deque([0.0] * 100, maxlen=100)

        #NEW ****************************************************************


        # Create a PyQtGraph widget for plotting real-time data
        # self.plot_widget = pg.PlotWidget(title=title)
        # self.plot_widget.setBackground('white')  # Set the graph background to black
        # self.plot_widget.setLabel('left', y_label, color='black')  # Y-axis label
        # self.plot_widget.setLabel('bottom', 'Data Points', color='black')  # X-axis label
        # self.plot_widget.addLegend(labelTextColor='black')  # Add a legend with white text

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('white')  # White background
        self.plot_widget.setTitle(title, color='black', size="10pt")  # Title in black

        # Axis labels

        label_font = QFont("Arial", 20)
        label_font.setBold(True)

        self.plot_widget.setLabel('left', y_label, **{'color': 'black', 'font': label_font})
        self.plot_widget.setLabel('bottom', 'Data Points', **{'color': 'black', 'font': label_font})

        # Axis tick labels
        self.plot_widget.getAxis('left').setTextPen('black')
        self.plot_widget.getAxis('bottom').setTextPen('black')

        # Legend text colour (PyQtGraph doesn't always respect labelTextColor, so ignore it)
        legend = self.plot_widget.addLegend(labelTextColor='black')

        # Thicker pens for pitch, roll, and yaw
        pitch_pen = pg.mkPen(color='r', width=2)
        roll_pen = pg.mkPen(color='g', width=2)
        yaw_pen = pg.mkPen(color='b', width=2)

        self.pitch_curve = self.plot_widget.plot(pen=pitch_pen, name="Pitch")
        self.roll_curve = self.plot_widget.plot(pen=roll_pen, name="Roll")
        self.yaw_curve = self.plot_widget.plot(pen=yaw_pen, name="Yaw")

        # # Plot curves for yaw, pitch, and roll
        # self.pitch_curve = self.plot_widget.plot(pen='r', name="Pitch", width=10)     # Red line for pitch
        # self.roll_curve = self.plot_widget.plot(pen='g', name="Roll", width=10)       # Green line for roll
        # self.yaw_curve = self.plot_widget.plot(pen='b', name="Yaw", width=10)         # Blue line for yaw
        # # self.anomaly_curve = self.plot_widget.plot(pen='y', name="Anomalies")         # Yellow line for anomalies


        #NEW ****************************************************************
        self.anomaly_scatter = ScatterPlotItem(size=8, pen=pg.mkPen(None), brush=pg.mkBrush('orange'), symbol='t1')
        self.plot_widget.addItem(self.anomaly_scatter)
        #NEW ****************************************************************


        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Set the background color of the widget (the container) to black
        self.setStyleSheet("background-color: black;")        

    def update_data(self, pitch, roll, yaw, anomaly=False):
        """Update the graph with new pitch, roll, and yaw data."""
        # Append new values to the circular buffers
        self.pitch_buffer.append(pitch)
        self.roll_buffer.append(roll)
        self.yaw_buffer.append(yaw)

        # Update the line plots with the new buffer data
        self.pitch_curve.setData(list(self.pitch_buffer))
        self.roll_curve.setData(list(self.roll_buffer))
        self.yaw_curve.setData(list(self.yaw_buffer))

        #NEW ****************************************************************

        if anomaly:
            self.anomaly_buffer_dot.append(-200)  # Only store pitch values
            print("ANOMALY DETECTED")
        else:
            self.anomaly_buffer_dot.append(None)  # Maintain buffer size

        # Generate indices dynamically
        x_vals = list(range(len(self.anomaly_buffer_dot)))  # Use indices as x-values
        y_vals = list(self.anomaly_buffer_dot)  # Use buffer values as y-values

        # Pass both x and y to setData
        self.anomaly_scatter.setData(x=x_vals, y=y_vals)        

        # Update the anomaly scatter plot

        # if anomaly:
        #     anomaly_value = 50
        # else:
        #     anomaly_value = 0


        # self.anomaly_buffer.append(anomaly_value)
        # self.anomaly_curve.setData(list(self.anomaly_buffer))

        #NEW ****************************************************************
