#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
import math

#---------------------------------------------------------------------------------------------
# Function - Quaternion to Euler Conversion
#---------------------------------------------------------------------------------------------

def quaternion_to_euler(w, x, y, z):
    """Convert quaternion to Euler angles (yaw, pitch, roll)."""

    # Yaw (Z-axis rotation)
    yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

    # Roll (Y-axis rotation)
    sinp = 2.0 * (w * y - z * x)

    roll = math.asin(sinp) if abs(sinp) <= 1 else math.copysign(math.pi / 2, sinp)
    # Pitch (X-axis rotation)

    pitch = math.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
    # Convert radians to degrees

    return math.degrees(pitch), math.degrees(roll), math.degrees(yaw)
