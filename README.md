# Motion Tracking for Real-Time Feedback in Physiotherapy and Athletic Rehabilitation
## Overview

With global healthcare systems facing increasing pressure—especially in countries with large populations and limited access to specialised services such as physiotherapy, there is a growing need for scalable, affordable solutions. The COVID-19 pandemic further exposed vulnerabilities in healthcare accessibility. Meanwhile, advances in wearable technology and smart devices have demonstrated the potential for decentralised, self-managed health monitoring. The Individual Project software package has been developed to offer an affordable and intuitive platform for physiotherapy and rehabilitation from the comfort of ones home, without the need for direct supervision from a medical professional. 

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



## Known Issues/ Future Improvements:







  
