#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
import sys

from PyQt5.QtWidgets import QApplication

from MetricsPanel import MetricsPanel
from WidgetWrapper import CustomWindow
from DataCollectionPanel import TestPanel
from RealTimeGraphs import GraphContainer
from WebSocketClientFile import WebSocketClient

# WebSocket configuration
websocket_url = "ws://192.168.1.22:81"  # URL of the WebSocket Server hosted by the ESP32
file_directory = "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Formal_Design/"    # Preset file directory to store CSV logs

# GUI Styles

button_style = """
    QPushButton {
        background-color: #444444;
        color: white;
        border: 2px solid #555555;
        border-radius: 5px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #555555;
        border: 2px solid #888888;
    }
    QPushButton:pressed {
        background-color: #222222;
    }
"""

style_sheet_style = """
    QPushButton {
        background-color: #444444;
        color: white;
        border: 2px solid #555555;
        border-radius: 5px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #555555;
        border: 2px solid #888888;
    }
    QPushButton:pressed {
        background-color: #222222;
    }
    QLabel {
        color: white;
    }
    QWidget {
        background-color: black;
    }
"""


#---------------------------------------------------------------------------------------------
# Function - Main
#---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create a PyQt application

    app.setStyleSheet(style_sheet_style)

    # Create the angle graph container
    angle_graph_window = GraphContainer(title="Real-Time Graph: Pitch, Roll, Yaw", y_label="Euler Angle (°)")
    angle_graph_window_wrapped = CustomWindow(angle_graph_window, title="")

    # Create the velocity graph container
    velocity_graph_window = GraphContainer(title="Real-Time Graph: Angular Velocity", y_label="Velocity (°/s)")
    velocity_graph_window_wrapped = CustomWindow(velocity_graph_window, title="")

    # Create the WebSocket client and pass the graph containers to it
    websocket_client = WebSocketClient()

    # Create the test panel and pass the WebSocket client
    test_panel = TestPanel(websocket_client, angle_graph_window, velocity_graph_window)
    test_panel_wrapped = CustomWindow(test_panel, title="Real-Time Processing Panel")

    # Create the metrics panel and pass the WebSocket client
    metrics_panel = MetricsPanel()
    metrics_panel_wrapped = CustomWindow(metrics_panel, title="Post-Processing and Analysis Panel")

    # Show the graph windows
    angle_graph_window_wrapped.setGeometry(1120, 0, 800, 500)
    velocity_graph_window_wrapped.setGeometry(1120, 500, 800, 500)
    test_panel_wrapped.setGeometry(720, 0, 400, 500)
    metrics_panel_wrapped.setGeometry(720, 500, 400, 500)

    angle_graph_window_wrapped.show()
    velocity_graph_window_wrapped.show()
    test_panel_wrapped.show()
    metrics_panel_wrapped.show()

    sys.exit(app.exec_())  # Run the application event loop
