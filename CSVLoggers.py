#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
import os
import csv

#---------------------------------------------------------------------------------------------
# Class - CSVLogger - Normal
#---------------------------------------------------------------------------------------------

class CSVLogger:
    def __init__(self, filepath):
        self.filepath = filepath

        #Ensure the directory exists
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory) # Create directories if they do not exist

        # Open the file in write mode and initialise the CSV writer
        with open(self.filepath, mode="w", newline="") as file:
            self.writer = csv.writer(file)
            # Write the header row
            self.writer.writerow(["Timestamp", "Pitch (°)", "Roll (°)", "Yaw (°)", 
                                  "Pitch Velocity (°/s)", "Roll Velocity (°/s)", "Yaw Velocity (°/s)"])
            

    def log_data(self, timestamp, pitch, roll, yaw, pitch_velocity, roll_velocity, yaw_velocity):
        """Log a new row of data to the CSV file."""
        with open(self.filepath, mode="a", newline="") as file:
            self.writer = csv.writer(file)
            self.writer.writerow([timestamp, pitch, roll, yaw, pitch_velocity, roll_velocity, yaw_velocity])            

#---------------------------------------------------------------------------------------------
# Class - CSVLoggerML - ML Sliding Window
#---------------------------------------------------------------------------------------------

class CSVLoggerML:
    def __init__(self, filepath, window_size=10):
        self.filepath = filepath
        self.window_size = window_size
        self.buffer = []

        #Ensure the directory exists
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory) # Create directories if they do not exist

        # Open the file in write mode and initialise the CSV writer
        with open(self.filepath, mode="w", newline="") as file:
            self.writer = csv.writer(file)
            # Write the header row
            headers = ["Timestamp"]
            for i in range(self.window_size):
                headers += [f"Pitch_{i+1}", f"Roll_{i+1}", f"Yaw_{i+1}",
                            f"Pitch Velocity_{i+1}", f"Roll Velocity_{i+1}", f"Yaw Velocity_{i+1}"]            
            headers.append("Label")
            self.writer.writerow(headers)

    def log_data(self, timestamp, pitch, roll, yaw, pitch_velocity, roll_velocity, yaw_velocity, label=None):
        """Add a new sensor reading and write a window to CSV when full."""
        # Append data to the buffer
        self.buffer.append([pitch, roll, yaw, pitch_velocity, roll_velocity, yaw_velocity])
        
        # When the buffer reaches window size, write to CSV
        if len(self.buffer) == self.window_size:
            # Start the row with the timestamp (from the first sample in the window)
            row = [timestamp]
            
            # Flatten the buffer and write to the CSV file
            for sample in self.buffer:
                row.extend(sample)
            
            # flattened_window = [item for sublist in self.buffer for item in sublist]
            # if label is not None:
            #     flattened_window.append(label)  # Append label if it's supervised data
                    
        
        with open(self.filepath, mode="a", newline="") as file:
            self.writer = csv.writer(file)
            self.writer.writerow(row)   

        # After writing, remove oldest data point for the sliding window                     
        self.buffer.pop(0)
