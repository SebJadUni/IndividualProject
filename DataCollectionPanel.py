#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout  # For GUI layout and widget container
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

import os 
import time  # For timing calculations (velocity, logging intervals)
import csv

# from WebSocketClient import WebSocketClient  # Import the WebSocket client
from CSVLoggers import CSVLogger, CSVLoggerML
from mathfunctions import quaternion_to_euler

from IsolationForest import AnomalyDetector


# from PyQt5.QtWebSockets import QWebSocket  # WebSocket client for real-time communication

websocket_url = "ws://192.168.1.22:81"  # URL of the WebSocket Server hosted by the ESP32

master_csv_path = "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Master_CSV/"

file_directory = "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Formal_Design/"    # Preset file directory to store CSV logs


# Parameter Constants
static_time_const = 10                  # In Minutes
static_sampling_interval_const = 0.4    # Sampling Interval
orientation_time_const = 15             # In Seconds
ML_time_const = 10                      # In Minutes

green_button_style = """
    QPushButton {
        background-color: #444444;
        color: green;
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


#---------------------------------------------------------------------------------------------
# Class - Test Panel Container
#---------------------------------------------------------------------------------------------

class TestPanel(QWidget):
    def __init__(self, websocket_client, angle_graph=None, velocity_graph=None):
        super().__init__()
        self.websocket_client = websocket_client

        self.ML_button_style = """"""

        self.ML_button_text = "Load a Real-Time ML Model"

        # NEW ***********************************************
        self.anomaly_detector = AnomalyDetector()
        # NEW ***********************************************

        # Connect signals from WebSocketClient to UI functions
        self.websocket_client.update_signal.connect(self.update_graph)  # Connect the signal to handle incoming data

        self.angle_graph = angle_graph              # Reference to the angle graph widget
        self.velocity_graph = velocity_graph        # Reference to the graph widget
        self.csv_logger = None                      # Reference to the CSV logger        
        
        # Initialize previous values and time for velocity calculation
        self.prev_pitch = self.prev_roll = self.prev_yaw = None
        self.prev_time = None        
        self.logging_active = False

        # Variables for controlling CSV sampling rate
        self.csv_sampling_interval = 1.0  # Time in seconds between CSV writes
        self.last_csv_write_time = None   # Timestamp of the last CSV write

        # self.csv_logger = None
        self.timer = None

        self.static_remaining_time = static_time_const
        self.orientation_remaining_time = orientation_time_const
        self.ML_remaining_time = ML_time_const

        self.phase = 0
        self.counter = 0

        # Track connection status
        self.connected = False

        # Initialise "connect to ESP UI"
        self.panel_layout()

        # # Listen for WebSocket events
        self.websocket_client.connected_signal.connect(self.on_connected)
        self.websocket_client.disconnected_signal.connect(self.on_disconnected)        

    #---------------------------------------------------------------------------------------------
    # Functions - Panel Layouts
    #---------------------------------------------------------------------------------------------

    def panel_layout(self):
        self.setWindowTitle("IMU Test Panel")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.layout.addStretch()
        
        # Create all required widgets
        self.connect_button = QPushButton("Connect to ESP")
        # self.connect_button.setStyleSheet(button_style)
        self.connect_button.clicked.connect(self.connect_to_esp)

        self.static_test_button = QPushButton("Static Test")
        # self.static_test_button.setStyleSheet(button_style)
        self.static_test_button.clicked.connect(self.show_static_test_menu)
        
        self.orientation_test_button = QPushButton("Orientation Test")
        # self.orientation_test_button.setStyleSheet(button_style)
        self.orientation_test_button.clicked.connect(self.show_orientation_test_menu)

        self.real_time_ML_button = QPushButton("Load Real-Time ML Model")
        # self.combined_test_button.setStyleSheet(button_style)
        self.real_time_ML_button.clicked.connect(self.load_real_time_ML_model)

        self.ML_button = QPushButton("ML Data Gathering")
        # self.ML_button.setStyleSheet(button_style)
        self.ML_button.clicked.connect(self.ML_menu)

        self.done_button = QPushButton("Done")
        # self.done_button.setStyleSheet(button_style)
        self.done_button.clicked.connect(self.start_static_test)

        self.cancel_button = QPushButton("Cancel")
        # self.cancel_button.setStyleSheet(button_style)
        self.cancel_button.clicked.connect(self.return_to_main_menu)

        self.done_button_orientation = QPushButton("Done")
        # self.done_button.setStyleSheet(button_style)
        self.done_button_orientation.clicked.connect(self.start_orientation_test)

        self.cancel_button_orientation = QPushButton("Cancel")   
        # self.cancel_button.setStyleSheet(button_style)
        self.cancel_button_orientation.clicked.connect(self.return_to_main_menu)

        # self.done_button_combined = QPushButton("Done")
        # self.done_button_combined.clicked.connect(self.start_combined_test)

        # self.cancel_button_combined = QPushButton("Cancel")
        # self.cancel_button_combined.clicked.connect(self.return_to_main_menu)

        self.done_button_ML = QPushButton("Done")
        self.done_button_ML.clicked.connect(self.ML_data_gathering)

        self.cancel_button_ML = QPushButton("Cancel")
        self.cancel_button_ML.clicked.connect(self.return_to_main_menu)

        self.instruction_label = QLabel("")

        self.timer_label = QLabel("")

        self.init_connect_menu()

    def remove_all_widgits(self):
        self.layout.removeWidget(self.connect_button)
        self.connect_button.hide()

        self.layout.removeWidget(self.static_test_button)
        self.static_test_button.hide()

        self.layout.removeWidget(self.orientation_test_button)
        self.orientation_test_button.hide()

        self.layout.removeWidget(self.real_time_ML_button)
        self.real_time_ML_button.hide()

        self.layout.removeWidget(self.ML_button)
        self.ML_button.hide()

        self.layout.removeWidget(self.done_button)
        self.done_button.hide()

        self.layout.removeWidget(self.cancel_button)
        self.cancel_button.hide()

        self.layout.removeWidget(self.done_button_orientation)
        self.done_button_orientation.hide()

        self.layout.removeWidget(self.cancel_button_orientation)
        self.cancel_button_orientation.hide()

        self.layout.removeWidget(self.instruction_label)
        self.instruction_label.hide()

        while self.layout.count():  # Loop through all widgets in layout
            item = self.layout.takeAt(0)  # Take the first item
            if item.widget():
                item.widget().setParent(None)  # Properly remove the widget        

    def init_connect_menu(self):
        
        self.remove_all_widgits()

        """Initial screen to prompt connection to ESP32"""

        self.layout.addStretch()  # Push everything down

        # Instruction Label
        self.instruction_label.setText("Please connect to the ESP before proceeding.")
        self.instruction_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)        

        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.connect_button)
        self.connect_button.setVisible(True)

        self.layout.addStretch()  # Push everything up slightly

        self.setLayout(self.layout)

    def init_main_menu(self):       
        
        self.remove_all_widgits()

        self.layout.addStretch()  # Push everything down

        self.instruction_label.setText("Select a test to run")
        self.instruction_label.setStyleSheet("font-size: 16px; color: green;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing

        # Static Test Button
        
        self.layout.addWidget(self.static_test_button)
        self.static_test_button.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing

        # Orientation Test Button

        self.layout.addWidget(self.orientation_test_button)
        self.orientation_test_button.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing

        # Real-Time ML Button
  
        self.layout.addWidget(self.real_time_ML_button)
        self.real_time_ML_button.setStyleSheet(self.ML_button_style)
        self.real_time_ML_button.setText(self.ML_button_text)
        self.real_time_ML_button.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing

        # ML Test Button
  
        self.layout.addWidget(self.ML_button)        
        self.ML_button.setVisible(True)

        self.layout.addStretch()  # Push everything down

        self.setLayout(self.layout)

    #---------------------------------------------------------------------------------------------
    # Functions - Static Test 
    #---------------------------------------------------------------------------------------------

    def show_static_test_menu(self):

        self.remove_all_widgits()

        self.layout.addStretch()  # Push everything up slightly

        self.instruction_label.setText("Position the device in a static position")
        self.instruction_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing
        
        self.layout.addWidget(self.done_button)
        self.done_button.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.cancel_button)
        self.cancel_button.setVisible(True)

        self.layout.addStretch()  # Push everything up slightly

    def start_static_test(self):

        self.remove_all_widgits()

        file_path = self.ask_for_file()
        if not file_path:
            return

        self.csv_logger = CSVLogger(file_path)
        self.set_csv_logger(self.csv_logger)
        self.start_logging(sampling_interval=static_sampling_interval_const)

        self.instruction_label.setText("The test is running...")
        self.instruction_label.setStyleSheet("font-size: 16px; color: orange;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)

        self.layout.addWidget(self.cancel_button)
        self.cancel_button.setVisible(True)

        self.start_timer()

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(60000)
        self.update_timer()

    def update_timer(self):

        # self.remove_all_widgits()

        if self.static_remaining_time > 0:
            self.static_remaining_time -= 1

            self.instruction_label.setText(f"Time Remaining: {self.static_remaining_time} minutes")
            self.instruction_label.setStyleSheet("font-size: 16px; color: orange;")
            self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
            self.instruction_label.setVisible(True)

        else:
            self.timer.stop()
            self.complete_test()

    def complete_test(self):
        self.stop_logging()
        QMessageBox.information(self, "Test Completed", "The Static Test has completed.")
        
        self.return_to_main_menu()

    #---------------------------------------------------------------------------------------------
    # Functions - Orientation Test
    #---------------------------------------------------------------------------------------------

    def show_orientation_test_menu(self):
        
        self.remove_all_widgits()

        self.layout.addStretch()  # Push everything up slightly

        self.instruction_label.setText("Position the device in a static position<br>pitch(0), roll(0), yaw(0)")
        self.instruction_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)
        
        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.done_button_orientation)
        self.done_button_orientation.setVisible(True)
       
        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.cancel_button_orientation)
        self.cancel_button_orientation.setVisible(True)

        self.layout.addStretch()  # Push everything up slightly

    def start_orientation_test(self):

        self.remove_all_widgits()

        file_path = self.ask_for_file()
        if not file_path:
            return

        self.csv_logger = CSVLogger(file_path)
        self.set_csv_logger(self.csv_logger)
        self.start_logging(sampling_interval=0.10)

        self.instruction_label.setText("Logging data for phase 1... (15 seconds)")
        self.instruction_label.setStyleSheet("font-size: 16px; color: orange;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)
        
        self.layout.addWidget(self.cancel_button_orientation)
        self.cancel_button_orientation.setVisible(True)

        self.phase = 0
        self.start_timer_orientation()

    def start_timer_orientation(self):
        self.orientation_remaining_time = orientation_time_const
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_orientation)
        self.timer.start(1000)
        self.update_timer_orientation()

    def update_timer_orientation(self):
        if self.orientation_remaining_time > 0:
            self.orientation_remaining_time -= 1
            self.instruction_label.setText(f"Time Remaining: {self.orientation_remaining_time} seconds<br>Rotate the device {self.phase} degrees")
            self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
            self.instruction_label.setVisible(True)
        else:
            self.timer.stop()
            if self.phase == 0:
                self.phase = 45
                self.start_timer_orientation()
            elif self.phase == 45:
                self.phase = 90
                self.start_timer_orientation()
            elif self.phase == 90:
                self.phase = 0
                self.complete_orientation_test()           

    def complete_orientation_test(self):
        # self.websocket_client.stop_logging()
        QMessageBox.information(self, "Test Completed", "The Orientation Test has completed.")
        self.return_to_main_menu()        


    #---------------------------------------------------------------------------------------------
    # Functions - ML Data Collection
    #---------------------------------------------------------------------------------------------

    def load_real_time_ML_model(self):
        
        load_ML_Model, _ = QFileDialog.getOpenFileName(self, "Select Joblib Model File", master_csv_path, "Joblib Files (*.joblib);;All Files (*)")
        if load_ML_Model:
            loaded_message = self.anomaly_detector.load(load_ML_Model)
            QMessageBox.information(None, "Success", loaded_message) 

            self.ML_button_style = green_button_style 
            self.ML_button_text = "Model Loaded"

        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid ML Model file.")     


        self.init_main_menu()     

    def ML_menu(self):

        self.remove_all_widgits()

        self.layout.addStretch()  # Push everything up slightly

        self.instruction_label.setText("Mount the module onto the head")
        self.instruction_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.done_button_ML)
        self.done_button_ML.setVisible(True)

        self.layout.addSpacing(30)  # Adjust vertical spacing
        
        self.layout.addWidget(self.cancel_button_ML)
        self.cancel_button_ML.setVisible(True)

        self.layout.addStretch()  # Push everything up slightly

    def ML_data_gathering(self):

        file_path = self.ask_for_file()
        if not file_path:
            return

        self.csv_logger = CSVLoggerML(file_path)
        self.set_csv_logger(self.csv_logger)
        self.start_logging(sampling_interval=0.10)

        self.phase = 0
        self.start_timer_ML()

    def start_timer_ML(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_ML)
        self.timer.start(60000)
        self.update_timer_ML()

    def update_timer_ML(self):

        self.remove_all_widgits()

        self.instruction_label.setText("Logging data...")
        self.instruction_label.setStyleSheet("font-size: 16px; color: green;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)

        self.layout.addWidget(self.cancel_button_ML)
        self.cancel_button_ML.setVisible(True)

        if self.ML_remaining_time > 0:
            self.ML_remaining_time -= 1
            self.timer_label.setText(f"Time Remaining: {self.ML_remaining_time} minutes")
            self.timer_label.setStyleSheet("font-size: 16px; color: green;")
            self.layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
            self.timer_label.setVisible(True)            
        else:
            self.timer.stop()
            self.complete_ML()

    def complete_ML(self):
        self.stop_logging()
        QMessageBox.information(self, "Logging Data has Finished.")
        self.return_to_main_menu()


    #---------------------------------------------------------------------------------------------
    # Function - Utilities
    #---------------------------------------------------------------------------------------------

    def return_to_main_menu(self):
        """Reset the panel to its main menu by hiding and showing relevant widgets."""

        # Stop Logging any Data
        self.stop_logging()

        # Stop any running timers
        if self.timer:
            self.timer.stop()
            self.timer = None

        # Reset state variables
        self.static_remaining_time = static_time_const
        self.orientation_remaining_time = orientation_time_const
        self.phase = 0
        self.counter = 0

        self.remove_all_widgits()

        self.init_main_menu()

    def ask_for_file(self):
        while True:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Test Log File", file_directory, "CSV Files (*.csv)")
            if not file_name:
                QMessageBox.warning(self, "No File Selected", "Please select a valid file name.")
                return None
            if os.path.exists(file_name):
                QMessageBox.warning(self, "File Exists", "The file name already exists. Please choose a new name.")
            else:
                return file_name

    def connect_to_esp(self):
        """Attempts to connect to the ESP."""

        if self.connected:
            self.init_main_menu()


        self.instruction_label.setText("Connecting...")
        self.instruction_label.setStyleSheet("font-size: 16px; color: orange;")

         # Call WebSocketClient’s connect function
        self.websocket_client.connect()


        # Start a timeout timer (e.g., 5 seconds)
        self.connection_timer = QTimer()
        self.connection_timer.setSingleShot(True)
        self.connection_timer.timeout.connect(self.handle_connection_timeout)
        self.connection_timer.start(5000)  # 5 seconds timeout        

    def handle_connection_timeout(self):
        """Called if the connection attempt times out."""
        if not self.connected:  # If still not connected, return to menu
            QMessageBox.warning(self, "Connection Failed", "Failed to connect to ESP. Please try again.")
            self.remove_all_widgits()
            self.init_connect_menu()

    def on_connected(self):
        """Handles successful connection and switches to the main menu."""
        self.connection_timer.stop()  # Stop the timeout check
        self.connected = True
        QMessageBox.information(self, "Connection Successful", "Connected to ESP!")

        self.init_main_menu()

    def on_disconnected(self):
        """Handles disconnection and returns to the connection menu."""
        print("WebSocket Disconnected - Triggering UI update")
        self.connected = False

        if self.websocket_client.last_received_time != None:
            QMessageBox.warning(self, "Connection Lost", "ESP disconnected! Please reconnect.")

        self.websocket_client.last_received_time = None       #######
        
        # Stop Logging any Data
        self.stop_logging()

        # Stop any running timers
        if self.timer:
            self.timer.stop()
            self.timer = None

        # Reset state variables
        self.static_remaining_time = static_time_const
        self.orientation_remaining_time = orientation_time_const
        self.phase = 0
        self.counter = 0


        self.remove_all_widgits()

        self.init_connect_menu()  

    def update_graph(self, data):
        """Update the graph with new data."""
        # Extract quaternion components (real, i, j, k) from the received JSON data
        w = data.get("real", 0.0) / 100.0
        x = data.get("i", 0.0) / 100.0
        y = data.get("j", 0.0) / 100.0
        z = data.get("k", 0.0) / 100.0

        # Convert quaternion to Euler angles
        pitch, roll, yaw = quaternion_to_euler(w, x, y, z)

        # Calculate angular velocity
        current_time = time.time()
        pitch_velocity, roll_velocity, yaw_velocity = self.calculate_velocity(pitch, roll, yaw, current_time)


        # Real-time anomaly detection ... INSERT BELOW

        anomaly_detected = self.anomaly_detector.detect_anomaly(pitch, roll, yaw, pitch_velocity, roll_velocity, yaw_velocity)


        # ... Real-Time anomaly detection INSERT ABOVE


        # Update the graph widget with the new data
        self.angle_graph.update_data(pitch, roll, yaw, anomaly=anomaly_detected)

        # Update the velocity graph
        self.velocity_graph.update_data(pitch_velocity, roll_velocity, yaw_velocity)  

        # Log data to the CSV file if logging is active and interval has passed
        if self.logging_active and self.csv_logger:
            if self.last_csv_write_time is None or (current_time - self.last_csv_write_time >= self.csv_sampling_interval):
                self.csv_logger.log_data(current_time, pitch, roll, yaw, pitch_velocity, roll_velocity, yaw_velocity)
                self.last_csv_write_time = current_time           

    def calculate_velocity(self, pitch, roll, yaw, current_time):
        """Calculate angular velocity (degrees/second) for pitch, roll, and yaw."""
        if self.prev_time is None:
            # Initialize previous values on first call
            self.prev_pitch, self.prev_roll, self.prev_yaw = pitch, roll, yaw
            self.prev_time = current_time
            return 0.0, 0.0, 0.0

        # Calculate time difference
        dt = current_time - self.prev_time

        if dt <= 0:  # Avoid division by zero or negative time
            return 0.0, 0.0, 0.0

        # Calculate angular velocity
        pitch_velocity = (pitch - self.prev_pitch) / dt
        roll_velocity = (roll - self.prev_roll) / dt
        yaw_velocity = (yaw - self.prev_yaw) / dt

        # Update previous values
        self.prev_pitch, self.prev_roll, self.prev_yaw = pitch, roll, yaw
        self.prev_time = current_time

        return pitch_velocity, roll_velocity, yaw_velocity
    
    def set_csv_logger(self, csv_logger):
        """Attach a CSV logger for the test."""
        self.csv_logger = csv_logger

    def start_logging(self, sampling_interval=1.0):
        """Activate logging."""
        self.logging_active = True
        self.csv_sampling_interval = sampling_interval
        self.last_csv_write_time = time.time()        

    def stop_logging(self):
        """Deactivate logging."""
        self.logging_active = False
