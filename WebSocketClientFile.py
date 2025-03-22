#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
import json  # To parse incoming WebSocket messages
from PyQt5.QtCore import pyqtSignal, QObject, QUrl, QTimer  # PyQt core features (signals, objects, URL handling)
from PyQt5.QtWebSockets import QWebSocket  # WebSocket client for real-time communication
from PyQt5.QtNetwork import QAbstractSocket
import time  # For timing calculations (velocity, logging intervals)

websocket_url = "ws://192.168.1.22:81"  # URL of the WebSocket Server hosted by the ESP32

#---------------------------------------------------------------------------------------------
# Class - WebSocket Client
#---------------------------------------------------------------------------------------------

class WebSocketClient(QObject):
    update_signal = pyqtSignal(dict)  # Signal for new data
    connected_signal = pyqtSignal()
    disconnected_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Initialize WebSocket and connect it to the server
        self.websocket = QWebSocket()
        self.websocket.textMessageReceived.connect(self.on_message)     # Triggered when data is received
        self.websocket.connected.connect(self.on_connected)
        self.websocket.disconnected.connect(self.on_disconnected)

        # #METHOD1 TIMEOUT
        # self.ping_timer = QTimer()
        # self.ping_timer.timeout.connect(self.check_connection)
        # self.ping_timer.start(5000)  # Check every 5 seconds

        #METHOD2 TIMEOUT
        self.last_received_time = None  # Track last received message time
        self.timeout_timer = QTimer()
        self.timeout_timer.timeout.connect(self.check_timeout)
        self.timeout_timer.start(5000)  # Check every 5 seconds

        self.connect()

    # def check_connection(self):
    #     """Periodically sends a ping to detect ESP disconnection."""
    #     if self.websocket.state() == QAbstractSocket.ConnectedState:
    #         self.websocket.ping()
    #     else:
    #         print("WebSocket appears disconnected, triggering on_disconnected()")
    #         self.on_disconnected()

    def check_timeout(self):
        """Detects if no messages have been received for too long."""
        if self.last_received_time is None:
            return  # Skip if no messages received yet

        if time.time() - self.last_received_time > 10:  # 10 sec timeout
            print("ESP32 unresponsive - triggering disconnect")
            self.on_disconnected()

    def connect(self):
        """Opens the WebSocket connection if not already connected"""
        if self.websocket.state() == QAbstractSocket.ConnectedState:
            return
        
        self.websocket.disconnected.connect(self.on_disconnected)   # NEW ADDITION CHECK IF WORKS 

        print("Attempting to connect to WebSocket...")
        self.websocket.open(QUrl(websocket_url))

    def on_connected(self):
        """Handles successful connection"""
        print("WebSocket Connected")
        self.connected_signal.emit()

    def on_disconnected(self):
        """Handles ESP disconnection"""
        print("WebSocket Disconnected")
        # self.last_received_time = None                          # Remove cyclic warning message
        self.disconnected_signal.emit()

    def on_message(self, message):
        """Handle incoming WebSocket messages."""
        self.last_received_time = time.time()  # Update last message time

        try:
            # Parse incoming JSON message
            data = json.loads(message)
            print("Received data:", data)  # Log the received data for debugging
            self.update_signal.emit(data)  # Emit the signal to update the graph
        except json.JSONDecodeError:
            print("Failed to decode JSON")  # Log an error if JSON parsing fails

          
