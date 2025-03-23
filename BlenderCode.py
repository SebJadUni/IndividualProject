import bpy
import mathutils
import asyncio
import websockets
import json
import math

CAMERA_NAME = "Camera.001"  # The name of the camera object
HEAD_MODEL_NAME = "HeadModel"

websocket_url = "ws://192.168.1.22:81"  # ESP32 WebSocket Address

ws = None
head_data = None
initial_quaternion = None  # Stores the initial IMU quaternion
desired_start_orientation = None  # Stores the desired starting orientation as a quaternion


# Function to get head model object
def get_head_model():
    return bpy.data.objects.get(HEAD_MODEL_NAME)


#Function to update the head model's orientation using quaternion data
def update_head_model():
    global head_data
    
    if head_data is None:
        return
    
    head = get_head_model()
    
    if not head:
        print(f"Object '{HEAD_MODEL_NAME}' not found")
        return
    
    # Extract and scale the quaternion data
    q_real = head_data.get("real", 0) / 100.0
    q_i = head_data.get("i", 0) / 100.0
    q_j = head_data.get("j", 0) / 100.0
    q_k = head_data.get("k", 0) / 100.0

    # Create a Blender quaternion from the scaled values
    quaternion = mathutils.Quaternion((q_real, q_i, q_j, q_k))

    # Apply the quaternion to the head model
    head.rotation_mode = 'QUATERNION'
    head.rotation_quaternion = quaternion

    # Force Blender to update the scene
    head.update_tag()
    bpy.context.view_layer.update()    



# Function to get the camera object
def get_camera():
    return bpy.data.objects.get(CAMERA_NAME)

# Function to set the desired starting orientation as a quaternion
def set_desired_start_orientation(yaw=0.0, pitch=0.0, roll=0.0):
    """
    Convert desired starting yaw, pitch, roll (in degrees) to a quaternion.
    """
    global desired_start_orientation
    # Create a quaternion from Euler angles (convert degrees to radians)
    euler = mathutils.Euler(
        (math.radians(pitch), math.radians(roll), math.radians(yaw)), 'XYZ'
    )
    desired_start_orientation = euler.to_quaternion()

# Function to compute relative quaternion adjusted for desired starting orientation
def get_relative_quaternion(current_quaternion):
    """
    Calculate the relative quaternion based on the initial (baseline) quaternion,
    adjusted by the desired starting orientation.
    """
    global initial_quaternion, desired_start_orientation
    if initial_quaternion is None:
        # Set the initial IMU quaternion as the baseline
        initial_quaternion = current_quaternion
        print("Initial quaternion set as baseline:", initial_quaternion)

    # Calculate the relative quaternion
    relative_quaternion = initial_quaternion.inverted() @ current_quaternion

    # Adjust by the desired starting orientation
    if desired_start_orientation:
        return desired_start_orientation @ relative_quaternion
    return relative_quaternion

# Function to update the camera's orientation using quaternion data
def update_camera_orientation():
    global head_data
    if head_data is None:
        return

    camera = get_camera()
    if not camera:
        print(f"Camera '{CAMERA_NAME}' not found")
        return

    # Extract and scale the quaternion data
    q_real = head_data.get("real", 0) / 100.0
    q_i = head_data.get("i", 0) / 100.0
    q_j = head_data.get("j", 0) / 100.0
    q_k = head_data.get("k", 0) / 100.0

    # Create a Blender quaternion from the scaled values
    current_quaternion = mathutils.Quaternion((q_real, -q_i, q_k, q_j))

    # Get the relative quaternion adjusted for the desired starting orientation
    adjusted_quaternion = get_relative_quaternion(current_quaternion)

    # Apply the adjusted quaternion to the camera
    camera.rotation_mode = 'QUATERNION'
    camera.rotation_quaternion = adjusted_quaternion

    # Force Blender to update the scene
    camera.update_tag()
    bpy.context.view_layer.update()



# Asynchronous function to receive data from the ESP32 WebSocket
async def receive_data():
    global head_data, ws
    async with websockets.connect(websocket_url) as websocket:
        ws = websocket
        while True:
            try:
                data = await websocket.recv()
                head_data = json.loads(data)
                print("Received data:", head_data)

            except json.JSONDecodeError:
                print("Failed to decode JSON")
            except websockets.exceptions.ConnectionClosedError:
                print("Connection to ESP32 was closed")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

# Function to start the WebSocket connection
def start_websocket():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_data())

# Function to periodically update Blender
def update_blender_scene():
    update_camera_orientation()
    update_head_model()
    return 0.05  # Repeat every 50 milliseconds

# Start the WebSocket connection in a separate thread
import threading
threading.Thread(target=start_websocket, daemon=True).start()

# Set the desired starting orientation
set_desired_start_orientation(yaw=0.0, pitch=90.0, roll=0.0)  # Example: Look 90° to the right initially

# Start the Blender timer to update the scene
bpy.app.timers.register(update_blender_scene)
