# IndividualProject
The code provided in the "IndividualProject" repository contains all code required for recreating the Graphics User Interface of the Individual Project. The Graphics User Interface is programmed in two environments - Blender and VS Code. View the README for more information.

Title: 
Individual Project - Motion Tracking for Real-Time Feedback in Physiotherapy and Athletic Rehabilitation


Introduction:
The Graphics User Interface program is split across two environments - Blender and VS Code. 
Both the Blender and Visual Studio Code is written in Python 3.10.

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


User Installation Instructions:
The platform installations required are as follows:
  - Blender (version 4.2 used)
  - Visual Studio Code (Most recent version)

The library installations required are as follows:
  - Within Blender:
    1. mathutils
    2. asyncio
    3. websockets
    4. json
    5. math
    6. bpy
  - Within VS Code:
    1. PyQt5
    2. numpy
    3. tensorflow
    4. joblib
    5. pandas
    6. sklearn
    7. matplotlib

  Installation within VS Code is as simple as typing into the terminal: pip install name_of_library


Further Technical Details:



Known Issues/ Future Improvements:




  
