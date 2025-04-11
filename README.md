# Motion Tracking for Real-Time Feedback in Physiotherapy and Athletic Rehabilitation
## Overview

Healthcare systems around the world are under growing pressure, especially in countries with large populations and limited access to specialised services like physiotherapy. The COVID-19 pandemic didn’t just strain these systems — it exposed major gaps in healthcare accessibility. Meanwhile, rapid advances in wearable technology and smart devices are proving that decentralised, self-managed health monitoring is not just possible, but practical. The Individual Project software package steps in to meet this need, offering an affordable, easy-to-use platform that lets people take charge of their physiotherapy and rehabilitation at home — no medical professional required.

The code found in this repository includes:
  1. Embedded Software for Motion Tracking Device
  2. Software for 3D Blender Environment
  3. Software for Custom GUI

The Embedded Software is written in C++ within the Arduino environment.
The Graphics User Interface program is split across two environments - Blender and VS Code. 
Both the Blender and Visual Studio Code is written in Python 3.10.

Arduino:
  1. Websocket setup - creates connection for clients (e.g. laptop) to connect to server/host (microcontroller on which the code is flashed)
  2. Data Communication with IMU via SPI
  3. Transmission of IMU Data via Wi-Fi

Blender:
  1. WebSocket setup for interfacing with the established websocket connection to the motion-tracking device via Wi-Fi
  2. IMU Data Processing code, implementing the equations described in the Final Report, i.e. equations (1) through (10) for 3D Transformations
  3. 3D shape rotation and camera rotation code

VS Code:
  1. WebSocket setup for interfacing with the established websocket connection to the motion-tracking device via Wi-Fi
  2. IMU Data Processing code for:
     - CSV data collection
     - Sensor drift and error measurement
     - Sensor accuracy measurement
     - ROM measurement
     - Smoothness measurement
  3. Code for GUI panels - Data Analysis Panel, Data Graphs, and Training and Loading ML Model Panel
  4. ML Model Code for Isolation Forest and LSTM Model

## Referencing

This work is described in the paper:

Sebastian Jadoenathmisier. 2025. "Motion Tracking for Real-Time Feedback in Physiotherapy and Athletic Rehabilitation". The University of Manchester. Link: 

## Installation

The platform installations required are as follows:
  - Arduino IDE (Most recent version)
  - Visual Studio Code (Most recent version)
  - Blender (version 4.2 used)

The library installations required are as follows:

Within Arduino:
  1. Adafruit_BNO08x
  2. WiFi
  3. WebSocketServer
  4. ArduinoJson
  5. math

Within Blender:
  1. mathutils
  2. asyncio
  3. websockets
  4. json
  5. math
  6. bpy
    
Within VS Code:
  1. PyQt5
  2. numpy
  3. tensorflow
  4. joblib
  5. pandas
  6. sklearn
  7. matplotlib

Installation within VS Code and Blender is as simple as typing into the terminal: pip install name_of_library

## Code Breakdown:

Aduino Environment:
  1. ESP32Code.cpp  =>  Encapsulates the entire code required for IMU data communication, WebSocket setup, and Wi-Fi communication
  
Blender Environment:
  1. BlenderCode.py  =>  Encapsulates the entire code required for the virtual environment GUI, including 3D transformation mathematics, 3D shape orientation, and camera orientation within the virtual environment

Visual Studio Code Environment:
  1. **main.py**
  2. **mathfunctions.py**  =>  Mathematical equations relating to data processing
  3. **WidgetWrapper.py**  =>  Style sheets and formatting of the GUI
  4. **WebSocketClientFile.py**  =>  Sets up client connection to the websocket, which connects to the motion tracking device  
  5. **RealTimeGraphs.py**  =>  Display incoming IMU data in real-time for live feedback
  6. **MetricsPanel.py**  =>  Menu for analysing previous physiotherapy sessions/ data, including basic statistical analysis (e.g. Range of Movement and Smoothness) and Isolation Forest and LSTM for anomaly detection and movement characterisation
  
  7. **DataCollectionPanel.py**  =>  Menu for collection of motion data for post-processed analysis or ML model training
  8. **CSVLoggers.py**  =>  When activated logs incoming IMU data, with the format specified through the interface
  9. **IsolationForest.py**  =>  ML Model for anomaly detection
  10. **LSTM.py**  =>  ML Model for movement characterisation 


## Future Improvements:

The 3D environment is currently implemented in Blender, which divides the GUI software package into 2 environments. To improve on this, the 3D virtual environment could be fully integrated and modified inside the same software package as the rest of the GUI. Combining the two would allow for interaction between the GUI panels. One good example of where this is useful is for live anomaly feedback correction. The Isolation Forest outputs could directly affect the way the 3D environment is displayed, to allow for feedback within the virtual environment, which isnt currently possible.






  
