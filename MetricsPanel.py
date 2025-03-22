#---------------------------------------------------------------------------------------------
# Libraries - Core Functionality
#---------------------------------------------------------------------------------------------
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QMessageBox, QMainWindow

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 

from IsolationForest import AnomalyDetector

from LSTM import MovementClassifier
from tensorflow.keras.layers import LSTM, Dropout
from tabulate import tabulate  # Pretty table formatting


file_directory = "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Formal_Design/"    # Preset file directory to store CSV logs

master_csv_path = "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Master_CSV/"

file_path_ML_Model = "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Master_CSV/" 

green_button_style = """
    QPushButton {
        background-color: green; /* Makes the button fully green */
        color: white; /* Changes the text color for better visibility */
        border: 2px solid darkgreen; /* Gives a darker green border */
        border-radius: 5px;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #32CD32; /* Lighter green on hover */
        border: 2px solid #228B22;
    }
    QPushButton:pressed {
        background-color: #006400; /* Darker green when pressed */
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

ML_model_loaded = 0

#---------------------------------------------------------------------------------------------
# Class - Metrics Panel
#---------------------------------------------------------------------------------------------

class PlotWindow(QMainWindow):
    """Popup window for displaying the graph."""
    def __init__(self, df, anomalies, movement_regions, label_encoder=None):
        super().__init__()
        self.setWindowTitle("IMU Data Plot")
        self.setGeometry(1130, 550, 800, 450)       # Size of the popup
        self.label_encoder = label_encoder  # Store label encoder


        # Create a figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        # Layout for the plot
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        # Plot the data
        self.plot_graph(df, anomalies, movement_regions)

# ORIGINAL
#     def plot_graph(self, df, anomalies=None, movement_regions=None):
#         """Plots the IMU data."""
#         self.ax.clear()  # Clear previous plots
#         self.ax.plot(df.index, df["Pitch (°)"], label="Pitch", color="r")
#         self.ax.plot(df.index, df["Roll (°)"], label="Roll", color="g")
#         self.ax.plot(df.index, df["Yaw (°)"], label="Yaw", color="b")

        
#         if self.label_encoder:
#             # Decode movement labels using LabelEncoder (convert numbers back to movement names)
#             movement_labels = {i: label for i, label in enumerate(self.label_encoder.classes_)}  
#         else:
#             movement_labels = {i: f"Movement {i}" for i in range(4)}  # Default labels


#         movement_colors = {0: "yellow", 1: "cyan", 2: "magenta", 3: "red"}  # Example: Nod, Roll, Tilt, Stationary

#         # Highlight movement regions
#         if movement_regions:
#             seen_labels = set()

#             for start, end, label in movement_regions:
#                 print(f"Start: {start}, End: {end}, Label: {label}, Type: {type(label)}")  # Debugging print


#                 if isinstance(label, (list, set)):  # Convert set/list to single integer
#                     label = list(label)[0]

#                 movement_name = movement_labels.get(label, f"Unknown {label}")
#                 color = movement_colors[label % len(movement_colors)]  # Safe color selection
                
#                 if label not in seen_labels:  
#                     self.ax.axvspan(start, end, color=color, alpha=0.3, label=movement_name)  
#                     seen_labels.add(label)  # Prevent duplicates
#                 else:
#                     self.ax.axvspan(start, end, color=color, alpha=0.3)


#         if anomalies:
#             # Highlight anomalies in Pitch, Roll, and Yaw
#             self.ax.scatter(anomalies, df.loc[anomalies, "Pitch (°)"], color='red', s=100, label="Anomalies - Pitch", edgecolor='black')
#             self.ax.scatter(anomalies, df.loc[anomalies, "Roll (°)"], color='green', s=100, label="Anomalies - Roll", edgecolor='black')
#             self.ax.scatter(anomalies, df.loc[anomalies, "Yaw (°)"], color='blue', s=100, label="Anomalies - Yaw", edgecolor='black')


#    #         # Legends
#     #         imu_legend = self.ax.legend(loc="center left", bbox_to_anchor=(1.04, 0.9), fontsize=14, title="IMU Data", title_fontsize=14)
#     #         jerk_legend = ax2.legend(loc="center left", bbox_to_anchor=(1.04, 0.7), fontsize=14, title="Jerk Analysis", title_fontsize=14)

#     #         self.ax.add_artist(imu_legend)  # Prevents overwriting the first legend

#     #         self.ax.set_title("Post-Processed IMU Data with Jerk Analysis", fontsize=22)

#     #         # Get the figure from the canvas
#     #         fig = self.canvas.figure  

#     #         # Adjust layout to shift the plot left and make room for the legend
#     #         fig.subplots_adjust(left=0.05, right=0.8)  # Reduces right space for legend

#         self.ax.legend(loc="center left", bbox_to_anchor=(1.04, 0.85), fontsize=14, title="Legend", title_fontsize=14)
#         self.ax.set_xlabel("Time (s)", fontsize=22)
#         self.ax.set_ylabel("Angle (°)", fontsize=22)
#         self.ax.set_title("Post-Processed IMU Data Graph with Anomaly Detection", fontsize=22)
#         # self.ax.legend()

#         self.ax.tick_params(axis='both', labelsize=20)  # Adjust the font size here (e.g., 16)

#         # Get the figure from the canvas
#         fig = self.canvas.figure  

#         # Adjust layout to shift the plot left and make room for the legend
#         fig.subplots_adjust(left=0.07, right=0.8)  # Reduces right space for legend

#         self.canvas.draw()  # Refresh the plot        


    # def plot_graph(self, df, anomalies=None, movement_regions=None):
    #     """Plots the IMU data with max/min values highlighted."""
    #     self.ax.clear()  # Clear previous plots
    #     self.ax.plot(df.index, df["Pitch (°)"], label="Pitch", color="r")
    #     self.ax.plot(df.index, df["Roll (°)"], label="Roll", color="g")
    #     self.ax.plot(df.index, df["Yaw (°)"], label="Yaw", color="b")

    #     # Compute max and min values for Pitch, Roll, and Yaw
    #     metrics = {}
    #     for col in ["Pitch (°)", "Roll (°)", "Yaw (°)"]:
    #         max_val = df[col].max()
    #         min_val = df[col].min()
    #         max_idx = df[col].idxmax()
    #         min_idx = df[col].idxmin()
    #         metrics[col] = {"max": (max_idx, max_val), "min": (min_idx, min_val)}

    #     # Highlight max/min values on the graph
    #     for col, color in zip(["Pitch (°)", "Roll (°)", "Yaw (°)"], ["r", "g", "b"]):
    #         max_idx, max_val = metrics[col]["max"]
    #         min_idx, min_val = metrics[col]["min"]

    #         self.ax.scatter(max_idx, max_val, color=color, s=100, marker="v", edgecolor="black", label=f"Max {col}: {max_val:.2f}")
    #         self.ax.scatter(min_idx, min_val, color=color, s=100, marker="^", edgecolor="black", label=f"Min {col}: {min_val:.2f}")

    #         # Annotate max value above the marker
    #         self.ax.text(max_idx, max_val + 3, f"{max_val:.2f}", fontsize=11, ha="center", va="bottom", color=color)

    #         # Annotate min value below the marker
    #         self.ax.text(min_idx, min_val - 3, f"{min_val:.2f}", fontsize=11, ha="center", va="top", color=color)

    #     # If movement regions exist, highlight them
    #     if movement_regions:
    #         movement_colors = {0: "yellow", 1: "cyan", 2: "magenta", 3: "red"}
    #         seen_labels = set()
    #         for start, end, label in movement_regions:
    #             movement_name = self.label_encoder.classes_[label] if self.label_encoder else f"Movement {label}"
    #             color = movement_colors[label % len(movement_colors)]
    #             if label not in seen_labels:
    #                 self.ax.axvspan(start, end, color=color, alpha=0.3, label=movement_name)
    #                 seen_labels.add(label)
    #             else:
    #                 self.ax.axvspan(start, end, color=color, alpha=0.3)

    #     # If anomalies exist, highlight them
    #     if anomalies:
    #         self.ax.scatter(anomalies, df.loc[anomalies, "Pitch (°)"], color="red", s=100, label="Anomalies - Pitch", edgecolor="black")
    #         self.ax.scatter(anomalies, df.loc[anomalies, "Roll (°)"], color="green", s=100, label="Anomalies - Roll", edgecolor="black")
    #         self.ax.scatter(anomalies, df.loc[anomalies, "Yaw (°)"], color="blue", s=100, label="Anomalies - Yaw", edgecolor="black")

    #     self.ax.legend(loc="upper right", fontsize=10)
    #     self.ax.set_xlabel("Time", fontsize=12)
    #     self.ax.set_ylabel("Angle (°)", fontsize=12)
    #     self.ax.set_title("Post-Processed IMU Data Graph", fontsize=14)

    #     self.canvas.draw()  # Refresh the plot

    # def plot_graph(self, df, anomalies=None, movement_regions=None):
    #     """Plots the IMU data with separate legends for movement regions and min/max values."""
    #     self.ax.clear()  # Clear previous plots
    #     imu_lines = []  # Store handles for the IMU + movement legend
    #     min_max_lines = []  # Store handles for the min/max legend

    #     # Plot IMU Data
    #     imu_lines.append(self.ax.plot(df.index, df["Pitch (°)"], label="Pitch", color="r")[0])
    #     imu_lines.append(self.ax.plot(df.index, df["Roll (°)"], label="Roll", color="g")[0])
    #     imu_lines.append(self.ax.plot(df.index, df["Yaw (°)"], label="Yaw", color="b")[0])

    #     # Compute max and min values for Pitch, Roll, and Yaw
    #     metrics = {}
    #     for col in ["Pitch (°)", "Roll (°)", "Yaw (°)"]:
    #         max_val = df[col].max()
    #         min_val = df[col].min()
    #         max_idx = df[col].idxmax()
    #         min_idx = df[col].idxmin()
    #         metrics[col] = {"max": (max_idx, max_val), "min": (min_idx, min_val)}

    #     # Highlight max/min values on the graph
    #     for col, color in zip(["Pitch (°)", "Roll (°)", "Yaw (°)"], ["r", "g", "b"]):
    #         max_idx, max_val = metrics[col]["max"]
    #         min_idx, min_val = metrics[col]["min"]

    #         # Plot max and min markers and store them separately
    #         min_max_lines.append(self.ax.scatter(max_idx, max_val, color=color, s=100, marker="^", edgecolor="black", label=f"Max {col}: {max_val:.2f}"))
    #         min_max_lines.append(self.ax.scatter(min_idx, min_val, color=color, s=100, marker="v", edgecolor="black", label=f"Min {col}: {min_val:.2f}"))

    #         # Annotate max value above the marker
    #         self.ax.text(max_idx, max_val + 2, f"{max_val:.2f}", fontsize=10, ha="center", va="bottom", color=color)

    #         # Annotate min value below the marker
    #         self.ax.text(min_idx, min_val - 2, f"{min_val:.2f}", fontsize=10, ha="center", va="top", color=color)

    #     # If movement regions exist, highlight them
    #     if movement_regions:
    #         movement_colors = {0: "yellow", 1: "cyan", 2: "magenta", 3: "red"}
    #         seen_labels = set()
    #         for start, end, label in movement_regions:
    #             # Decode movement labels using LabelEncoder if available
    #             movement_name = self.label_encoder.classes_[label] if self.label_encoder else f"Movement {label}"
    #             color = movement_colors[label % len(movement_colors)]

    #             # Only add unique movement labels to the legend
    #             if movement_name not in seen_labels:
    #                 patch = self.ax.axvspan(start, end, color=color, alpha=0.3, label=movement_name)
    #                 imu_lines.append(patch)  # Add to the IMU legend
    #                 seen_labels.add(movement_name)
    #             else:
    #                 self.ax.axvspan(start, end, color=color, alpha=0.3)

    #     # If anomalies exist, highlight them
    #     if anomalies:
    #         min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Pitch (°)"], color="red", s=100, label="Anomalies - Pitch", edgecolor="black"))
    #         min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Roll (°)"], color="green", s=100, label="Anomalies - Roll", edgecolor="black"))
    #         min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Yaw (°)"], color="blue", s=100, label="Anomalies - Yaw", edgecolor="black"))

    #     # Create separate legends
    #     imu_legend = self.ax.legend(handles=imu_lines, loc="upper left", fontsize=10, title="IMU Data & Movements")
    #     self.ax.add_artist(imu_legend)  # Add first legend manually

    #     min_max_legend = self.ax.legend(handles=min_max_lines, loc="upper right", fontsize=10, title="Min/Max Values")

    #     self.ax.set_xlabel("Time", fontsize=12)
    #     self.ax.set_ylabel("Angle (°)", fontsize=12)
    #     self.ax.set_title("Post-Processed IMU Data Graph", fontsize=14)

    #     self.canvas.draw()  # Refresh the plot


    # def plot_graph(self, df, anomalies=None, movement_regions=None):
    #     """Plots the IMU data with separate legends for movement regions and min/max values, positioning the legend outside the graph."""
    #     self.ax.clear()  # Clear previous plots
    #     imu_lines = []  # Store handles for the IMU + movement legend
    #     min_max_lines = []  # Store handles for the min/max legend

    #     # Plot IMU Data
    #     imu_lines.append(self.ax.plot(df.index, df["Pitch (°)"], label="Pitch", color="r")[0])
    #     imu_lines.append(self.ax.plot(df.index, df["Roll (°)"], label="Roll", color="g")[0])
    #     imu_lines.append(self.ax.plot(df.index, df["Yaw (°)"], label="Yaw", color="b")[0])

    #     # Compute max and min values for Pitch, Roll, and Yaw
    #     metrics = {}
    #     for col in ["Pitch (°)", "Roll (°)", "Yaw (°)"]:
    #         max_val = df[col].max()
    #         min_val = df[col].min()
    #         max_idx = df[col].idxmax()
    #         min_idx = df[col].idxmin()
    #         metrics[col] = {"max": (max_idx, max_val), "min": (min_idx, min_val)}

    #     # Highlight max/min values on the graph
    #     for col, color in zip(["Pitch (°)", "Roll (°)", "Yaw (°)"], ["r", "g", "b"]):
    #         max_idx, max_val = metrics[col]["max"]
    #         min_idx, min_val = metrics[col]["min"]

    #         # Plot max and min markers and store them separately
    #         min_max_lines.append(self.ax.scatter(max_idx, max_val, color=color, s=100, marker="v", edgecolor="black", label=f"Max {col}: {max_val:.2f}"))
    #         min_max_lines.append(self.ax.scatter(min_idx, min_val, color=color, s=100, marker="^", edgecolor="black", label=f"Min {col}: {min_val:.2f}"))

    #         # Annotate max value above the marker
    #         self.ax.text(max_idx, max_val + 2, f"{max_val:.2f}", fontsize=10, ha="center", va="bottom", color=color)

    #         # Annotate min value below the marker
    #         self.ax.text(min_idx, min_val - 3, f"{min_val:.2f}", fontsize=10, ha="center", va="top", color=color)

    #     # If movement regions exist, highlight them
    #     if movement_regions:
    #         movement_colors = {0: "yellow", 1: "cyan", 2: "magenta", 3: "red"}
    #         seen_labels = set()
    #         for start, end, label in movement_regions:
    #             # Decode movement labels using LabelEncoder if available
    #             movement_name = self.label_encoder.classes_[label] if self.label_encoder else f"Movement {label}"
    #             color = movement_colors[label % len(movement_colors)]

    #             # Only add unique movement labels to the legend
    #             if movement_name not in seen_labels:
    #                 patch = self.ax.axvspan(start, end, color=color, alpha=0.3, label=movement_name)
    #                 imu_lines.append(patch)  # Add to the IMU legend
    #                 seen_labels.add(movement_name)
    #             else:
    #                 self.ax.axvspan(start, end, color=color, alpha=0.3)

    #     # If anomalies exist, highlight them
    #     if anomalies:
    #         min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Pitch (°)"], color="red", s=100, label="Anomalies - Pitch", edgecolor="black"))
    #         min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Roll (°)"], color="green", s=100, label="Anomalies - Roll", edgecolor="black"))
    #         min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Yaw (°)"], color="blue", s=100, label="Anomalies - Yaw", edgecolor="black"))

    #     # Adjust figure size to create space for the legend on the right
    #     self.figure.subplots_adjust(right=0.75)  # Shrink plot to make space for legends

    #     # Create separate legends and position them outside the graph
    #     imu_legend = self.ax.legend(handles=imu_lines, loc="center left", bbox_to_anchor=(1.02, 0.9), fontsize=10, title="IMU Data & Movements")
    #     min_max_legend = self.ax.legend(handles=min_max_lines, loc="upper left", bbox_to_anchor=(1.02, 0.75), fontsize=10, title="Min/Max Values")

    #     # Add the first legend manually (so it does not get overwritten)
    #     self.ax.add_artist(imu_legend)

    #     self.ax.set_xlabel("Time", fontsize=12)
    #     self.ax.set_ylabel("Angle (°)", fontsize=12)
    #     self.ax.set_title("Post-Processed IMU Data Graph", fontsize=14)

    #     self.canvas.draw()  # Refresh the plot

#MIN/MAX ROM
    def plot_graph(self, df, anomalies=None, movement_regions=None):
        """Plots the IMU data with separate legends for movement regions and min/max values, ensuring full region coverage."""
        self.ax.clear()  # Clear previous plots
        imu_lines = []  # Store handles for the IMU + movement legend
        min_max_lines = []  # Store handles for the min/max legend

        # Plot IMU Data
        imu_lines.append(self.ax.plot(df.index, df["Pitch (°)"], label="Pitch", color="r")[0])
        imu_lines.append(self.ax.plot(df.index, df["Roll (°)"], label="Roll", color="g")[0])
        imu_lines.append(self.ax.plot(df.index, df["Yaw (°)"], label="Yaw", color="b")[0])

        # Compute max and min values for Pitch, Roll, and Yaw
        metrics = {}
        for col in ["Pitch (°)", "Roll (°)", "Yaw (°)"]:
            max_val = df[col].max()
            min_val = df[col].min()
            max_idx = df[col].idxmax()
            min_idx = df[col].idxmin()
            metrics[col] = {"max": (max_idx, max_val), "min": (min_idx, min_val)}

        # Highlight max/min values on the graph
        for col, color in zip(["Pitch (°)", "Roll (°)", "Yaw (°)"], ["r", "g", "b"]):
            max_idx, max_val = metrics[col]["max"]
            min_idx, min_val = metrics[col]["min"]

            # Plot max and min markers and store them separately
            min_max_lines.append(self.ax.scatter(max_idx, max_val, color=color, s=100, marker="v", edgecolor="black", label=f"Max {col}: {max_val:.2f}°"))
            min_max_lines.append(self.ax.scatter(min_idx, min_val, color=color, s=100, marker="^", edgecolor="black", label=f"Min {col}: {min_val:.2f}°"))

            # Annotate max value above the marker
            self.ax.text(max_idx, max_val + 2, f"{max_val:.2f}", fontsize=14, ha="center", va="bottom", color=color)

            # Annotate min value below the marker
            self.ax.text(min_idx, min_val - 3, f"{min_val:.2f}", fontsize=14, ha="center", va="top", color=color)

        # Ensure all data points have a movement region
        if movement_regions:
            movement_colors = {0: "yellow", 1: "cyan", 2: "magenta", 3: "red"}
            seen_labels = set()
            new_movement_regions = []

            current_start = 0
            current_label = movement_regions[0][2]  # Start with the first label

            for start, end, label in movement_regions:
                new_movement_regions.append((current_start, end, label))
                current_start = end
                current_label = label

            # Ensure the last region extends to the end of the dataset
            if new_movement_regions[-1][1] < len(df):
                last_start, _, last_label = new_movement_regions[-1]
                new_movement_regions[-1] = (last_start, len(df), last_label)

            # Plot movement regions
            for start, end, label in new_movement_regions:
                movement_name = self.label_encoder.classes_[label] if self.label_encoder else f"Movement {label}"
                color = movement_colors[label % len(movement_colors)]

                if movement_name not in seen_labels:
                    patch = self.ax.axvspan(start, end, color=color, alpha=0.3, label=movement_name)
                    imu_lines.append(patch)  # Add to the IMU legend
                    seen_labels.add(movement_name)
                else:
                    self.ax.axvspan(start, end, color=color, alpha=0.3)

        # If anomalies exist, highlight them
        if anomalies:
            min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Pitch (°)"], color="red", s=100, label="Anomalies - Pitch", edgecolor="black"))
            min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Roll (°)"], color="green", s=100, label="Anomalies - Roll", edgecolor="black"))
            min_max_lines.append(self.ax.scatter(anomalies, df.loc[anomalies, "Yaw (°)"], color="blue", s=100, label="Anomalies - Yaw", edgecolor="black"))

        # Adjust figure size to create space for the legend on the right
        self.figure.subplots_adjust(right=0.75)  # Shrink plot to make space for legends

        # Create separate legends and position them outside the graph
        imu_legend = self.ax.legend(handles=imu_lines, loc="center left", bbox_to_anchor=(1.02, 0.86), fontsize=16, title="IMU Data Legend", title_fontsize = 16)
        min_max_legend = self.ax.legend(handles=min_max_lines, loc="upper left", bbox_to_anchor=(1.02, 0.70), fontsize=16, title="Min/Max Values", title_fontsize = 16)

        # Add the first legend manually (so it does not get overwritten)
        self.ax.add_artist(imu_legend)

        self.ax.set_xlabel("Time (s)", fontsize=22)
        self.ax.set_ylabel("Angle (°)", fontsize=22)
        self.ax.set_title("Post-Processed IMU Data with ROM", fontsize=22)

        self.ax.tick_params(axis='both', labelsize=20)  # Adjust the font size here (e.g., 16)

        # Get the figure from the canvas
        fig = self.canvas.figure  

        # Adjust layout to shift the plot left and make room for the legend
        fig.subplots_adjust(left=0.07, right=0.8)  # Reduces right space for legend
    
        self.canvas.draw()  # Refresh the plot


    # Accuracy Test
    # def plot_graph(self, df, anomalies=None, movement_regions=None):
    #     """Plots the IMU data and highlights stationary regions with horizontal lines."""
    #     self.ax.clear()  # Clear previous plots
    #     imu_lines = []  # Store handles for IMU data
    #     min_max_lines = []  # Store handles for min/max legend

    #     # Plot IMU Data
    #     imu_lines.append(self.ax.plot(df.index, df["Pitch (°)"], label="Pitch", color="r")[0])
    #     imu_lines.append(self.ax.plot(df.index, df["Roll (°)"], label="Roll", color="g")[0])
    #     imu_lines.append(self.ax.plot(df.index, df["Yaw (°)"], label="Yaw", color="b")[0])

    #     # Detect and plot stationary regions
    #     def detect_stationary_regions(angle_series, threshold=3, min_duration=10):
    #         """Detects stationary regions where angle remains within a threshold for a minimum duration."""
    #         stationary_regions = []
    #         start_idx = None

    #         for i in range(1, len(angle_series)):
    #             if abs(angle_series[i] - angle_series[i - 1]) < threshold:
    #                 if start_idx is None:
    #                     start_idx = i - 1  # Mark start of stationary region
    #             else:
    #                 if start_idx is not None and (i - start_idx) >= min_duration:
    #                     mean_value = np.mean(angle_series[start_idx:i])
    #                     stationary_regions.append((start_idx, i, mean_value))
    #                 start_idx = None  # Reset

    #         if start_idx is not None and (len(angle_series) - start_idx) >= min_duration:
    #             mean_value = np.mean(angle_series[start_idx:])
    #             stationary_regions.append((start_idx, len(angle_series), mean_value))

    #         return stationary_regions

    #     # Find and plot stationary lines for Pitch, Roll, and Yaw
    #     for angle_col, color in zip(["Pitch (°)", "Roll (°)", "Yaw (°)"], ["r", "g", "b"]):
    #         stationary_regions = detect_stationary_regions(df[angle_col])

    #         for start, end, mean_value in stationary_regions:
    #             self.ax.hlines(y=mean_value, xmin=start, xmax=end, colors=color, linestyles="dotted", linewidth=2, alpha=0.6)
    #             self.ax.text((start + end) / 2, mean_value - 22, f"{mean_value:.2f}°", fontsize=8, ha="center", va="bottom", color=color)

    #     # Label axes
    #     self.ax.set_xlabel("Time (s)", fontsize=14)
    #     self.ax.set_ylabel("Angle (°)", fontsize=14)

    #     # Create legend
    #     imu_legend = self.ax.legend(handles=imu_lines, loc="upper right", fontsize=11, title="Legend", title_fontsize=11)
    # #     imu_legend = self.ax.legend(handles=imu_lines, loc="center left", bbox_to_anchor=(1.02, 0.9), fontsize=10, title="IMU Data & Movements")

    #     self.ax.add_artist(imu_legend)

    #     self.ax.set_title("Post-Processed IMU Data Graph", fontsize=14)
    #     self.canvas.draw()  # Refresh the plot

# # JERK ANALYSIS
#     def plot_graph(self, df, anomalies=None, movement_regions=None):
#             """Plots the IMU data with jerk analysis using Pitch, Roll, and Yaw directly."""
#             self.ax.clear()  # Clear previous plots

#             # Compute jerk from position instead of velocity
#             df["Pitch Velocity"] = df["Pitch (°)"].diff()
#             df["Roll Velocity"] = df["Roll (°)"].diff()
#             df["Yaw Velocity"] = df["Yaw (°)"].diff()

#             df["Pitch Acceleration"] = df["Pitch Velocity"].diff()
#             df["Roll Acceleration"] = df["Roll Velocity"].diff()
#             df["Yaw Acceleration"] = df["Yaw Velocity"].diff()

#             # df["Pitch Jerk Abs"] = df["Pitch Acceleration"].diff().abs().rolling(window=2).mean()
#             # df["Roll Jerk Abs"] = df["Roll Acceleration"].diff().abs().rolling(window=2).mean()
#             # df["Yaw Jerk Abs"] = df["Yaw Acceleration"].diff().abs().rolling(window=2).mean()

#             df["Pitch Jerk Abs"] = df["Pitch Acceleration"].diff().abs()
#             df["Roll Jerk Abs"] = df["Roll Acceleration"].diff().abs()
#             df["Yaw Jerk Abs"] = df["Yaw Acceleration"].diff().abs()       

#             # Create a secondary y-axis for jerk values
#             ax2 = self.ax.twinx()

#             # Plot IMU Data (Pitch, Roll, Yaw)
#             self.ax.plot(df.index, df["Pitch (°)"], label="Pitch", color="r")
#             self.ax.plot(df.index, df["Roll (°)"], label="Roll", color="g")
#             self.ax.plot(df.index, df["Yaw (°)"], label="Yaw", color="b")

#             # Plot Jerk on Secondary Axis
#             ax2.plot(df.index, df["Pitch Jerk Abs"], label="Pitch Jerk", color="r", linestyle="dashed", alpha=0.7)
#             ax2.plot(df.index, df["Roll Jerk Abs"], label="Roll Jerk", color="g", linestyle="dashed", alpha=0.7)
#             ax2.plot(df.index, df["Yaw Jerk Abs"], label="Yaw Jerk", color="b", linestyle="dashed", alpha=0.7)

#             ax2.axhline(y=20, color="orange", linestyle="--", linewidth=2, alpha=0.5, label="Jerk Benchmark")

#             ax2.set_ylim(0, 100)  # Jerk axis always from 0 to 300°/s³

#             # Label axes
#             self.ax.set_xlabel("Time (s)", fontsize=22)
#             self.ax.set_ylabel("Angle (°)", fontsize=22)
#             ax2.set_ylabel("Jerk (°/s³)", fontsize=22, color="gray")

#             # Legends
#             imu_legend = self.ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.94), fontsize=16, title="IMU Data", title_fontsize=16)
#             jerk_legend = ax2.legend(loc="center left", bbox_to_anchor=(1.05, 0.72), fontsize=16, title="Jerk Analysis", title_fontsize=16)

#             self.ax.add_artist(imu_legend)  # Prevents overwriting the first legend

#             self.ax.set_title("Post-Processed IMU Data with Jerk Analysis", fontsize=22)

#             self.ax.tick_params(axis='both', labelsize=20)  # Adjust the font size here (e.g., 16)
#             ax2.tick_params(axis='y', labelsize=20)          # For secondary y-axis (jerk)

#             # Get the figure from the canvas
#             fig = self.canvas.figure  

#             # Adjust layout to shift the plot left and make room for the legend
#             fig.subplots_adjust(left=0.07, right=0.8)  # Reduces right space for legend

#             self.canvas.draw()  # Refresh the plot

#---------------------------------------------------------------

class MetricsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.Load_button_style = button_style

        self.Load_button_text = "Load ML Model"

        self.anomaly_detector = AnomalyDetector()

        self.motion_characteriser = MovementClassifier(input_shape=(10,6), num_classes=4)

        self.panel_layout()

    def panel_layout(self):    
        self.setWindowTitle("Statistics and ML odel")
        self.setGeometry(720, 300, 400, 300)

        self.layout = QVBoxLayout()

        self.layout.addStretch()

        # Creat all required widgets

        self.calculate_metrics_button = QPushButton("Select CSV file for Analysis")
        self.calculate_metrics_button.setStyleSheet(button_style)
        self.calculate_metrics_button.clicked.connect(self.select_csv_file)

        self.train_ML_button = QPushButton("Train ML Model")
        self.train_ML_button.setStyleSheet(button_style)
        self.train_ML_button.clicked.connect(self.ML_Model_Selection_Menu_Train)

        self.load_ML_button = QPushButton(self.Load_button_text)
        self.load_ML_button.setStyleSheet(self.Load_button_style)
        self.load_ML_button.clicked.connect(self.ML_Model_Selection_Menu_Load)

        self.add_data_button = QPushButton("Add Data to Master")
        self.add_data_button.setStyleSheet(button_style)
        self.add_data_button.clicked.connect(self.append_new_data_to_master)        

        self.back_button = QPushButton("Return to Menu")
        self.back_button.setStyleSheet(button_style)
        self.back_button.clicked.connect(self.init_menu)

        self.isolation_forest_train_button = QPushButton("Train Isolation Forest")
        self.isolation_forest_train_button.setStyleSheet(button_style)
        self.isolation_forest_train_button.clicked.connect(self.select_csv_file_training_IF)  

        self.LSTM_train_button = QPushButton("Train LSTM")
        self.LSTM_train_button.setStyleSheet(button_style)
        self.LSTM_train_button.clicked.connect(self.select_csv_file_training_LSTM)

        self.isolation_forest_load_button = QPushButton("Load Isolation Forest")
        self.isolation_forest_load_button.setStyleSheet(button_style)
        self.isolation_forest_load_button.clicked.connect(self.load_ML_Model_IF)  

        self.LSTM_load_button = QPushButton("Load LSTM")
        self.LSTM_load_button.setStyleSheet(button_style)
        self.LSTM_load_button.clicked.connect(self.load_ML_Model_LSTM)        

        # Insturction Label
        self.instruction_label = QLabel("")

        # Display Metrics Area
        self.metrics_label = QLabel("")

        self.init_menu()
    
    def remove_all_widgits(self):
        self.layout.removeWidget(self.calculate_metrics_button)
        self.calculate_metrics_button.hide()

        self.layout.removeWidget(self.train_ML_button)
        self.train_ML_button.hide()

        self.layout.removeWidget(self.instruction_label)
        self.instruction_label.hide()

        self.layout.removeWidget(self.metrics_label)
        self.metrics_label.hide()        

        while self.layout.count():  # Loop through all widgets in layout
            item = self.layout.takeAt(0)  # Take the first item
            if item.widget():
                item.widget().setParent(None)  # Properly remove the widget  

    def init_menu(self):

        self.remove_all_widgits()

        self.layout.addStretch()

        # Instruction Label
        self.instruction_label.setText("Calculate Metrics or Train ML Model")
        self.instruction_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)        

        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.calculate_metrics_button)
        self.calculate_metrics_button.setVisible(True)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.train_ML_button)
        self.train_ML_button.setVisible(True)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.load_ML_button)
        self.load_ML_button.setStyleSheet(self.Load_button_style)
        self.load_ML_button.setText(self.Load_button_text)        
        self.load_ML_button.setVisible(True)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.add_data_button)
        self.add_data_button.setVisible(True)        

        self.layout.addStretch()  # Push everything up slightly

        self.setLayout(self.layout)

    def ML_Model_Selection_Menu_Train(self):

        self.remove_all_widgits()

        self.layout.addStretch()

        # Instruction Label
        self.instruction_label.setText("Select ML Model For Training")
        self.instruction_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)        

        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.isolation_forest_train_button)
        self.isolation_forest_train_button.setVisible(True)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.LSTM_train_button)
        self.LSTM_train_button.setVisible(True)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.back_button)
        self.back_button.setVisible(True)     

        self.layout.addStretch() 

    def ML_Model_Selection_Menu_Load(self):

        self.remove_all_widgits()

        self.layout.addStretch()

        # Instruction Label
        self.instruction_label.setText("Select ML Model For Training")
        self.instruction_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.instruction_label.setVisible(True)        

        self.layout.addSpacing(30)  # Adjust vertical spacing

        self.layout.addWidget(self.isolation_forest_load_button)
        self.isolation_forest_load_button.setVisible(True)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.LSTM_load_button)
        self.LSTM_load_button.setVisible(True)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.back_button)
        self.back_button.setVisible(True)     

        self.layout.addStretch() 

# Statisitical Analysis Functions ------------------------>
    def select_csv_file(self):
        """Open a file dialog to select a CSV file and calculate metrics."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", file_directory, "CSV Files (*.csv)")
        if file_path:
            metrics = self.calculate_metrics(file_path)

            if metrics == -1:
                self.init_menu()

            self.display_metrics(metrics)
            self.show_plot(file_path)
        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid CSV file.") 
            self.init_menu()    

    def calculate_metrics(self, file_path):

        self.remove_all_widgits()

        """Calculate metrics from the selected CSV file."""
        try:
            df = pd.read_csv(file_path, encoding="latin1")

            # Ensure the required columns are present
            required_columns = ["Pitch (°)", "Roll (°)", "Yaw (°)"]
            if not all(col in df.columns for col in required_columns):
                # raise ValueError("The selected file does not have the required columns.")    
                QMessageBox.critical(self, "Error", "The selected file does not have the required columns")
                return -1

            metrics = {
                "Pitch": {
                    "Mean": df["Pitch (°)"].mean(),
                    # "Standard Deviation": df["Pitch (°)"].std(),
                    "Total Drift": df["Pitch (°)"].iloc[-1] - df["Pitch (°)"].iloc[0],
                    "Range": df["Pitch (°)"].max() - df["Pitch (°)"].min(),  # NEW - Measures spread
                    "RMS Error": np.sqrt(np.mean((df["Pitch (°)"] - df["Pitch (°)"].mean())**2))  # RMS deviation from mean
                },
                "Roll": {
                    "Mean": df["Roll (°)"].mean(),
                    # "Standard Deviation": df["Roll (°)"].std(),
                    "Total Drift": df["Roll (°)"].iloc[-1] - df["Roll (°)"].iloc[0],
                    "Range": df["Roll (°)"].max() - df["Roll (°)"].min(),  # NEW
                    "RMS Error": np.sqrt(np.mean((df["Roll (°)"] - df["Roll (°)"].mean())**2))  # RMS deviation from mean
                },
                "Yaw": {
                    "Mean": df["Yaw (°)"].mean(),
                    # "Standard Deviation": df["Yaw (°)"].std(),
                    "Total Drift": df["Yaw (°)"].iloc[-1] - df["Yaw (°)"].iloc[0],
                    "Range": df["Yaw (°)"].max() - df["Yaw (°)"].min(),  # NEW
                    "RMS Error": np.sqrt(np.mean((df["Yaw (°)"] - df["Yaw (°)"].mean())**2))  # RMS deviation from mean
                }
            }
            return metrics
        

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate metrics: {str(e)}")
            return {}

    def display_metrics(self, metrics):
        """Display the calculated metrics in the panel."""
        if not metrics:
            self.metrics_label.setText("No metrics available.")
            return

        # metrics_text = "Calculated Metrics:\n"
        metrics_text = ""

        for key, value in metrics.items():
            metrics_text += f"\n{key}:\n"
            for metric, result in value.items():
                metrics_text += f"  {metric}: {result:.2f}\n"

        self.metrics_label.setStyleSheet("font-size: 16px; color: white;")
        self.metrics_label.setText(metrics_text)
        
        self.layout.addWidget(self.metrics_label)
        self.metrics_label.setVisible(True)

        self.layout.addSpacing(0)  # Adjust vertical spacing

        self.layout.addWidget(self.back_button)
        self.back_button.setVisible(True)

# Working and Proven
    def show_plot(self, file_path):

        # Add functionality here to select plotting output based on which ML model is loaded 
        #----------------------------------------------------------------------------------#

        """Open the plot in a new popup window."""
        df = pd.read_csv(file_path, encoding="latin1")

        # Ensure required columns exist
        if not all(col in df.columns for col in ["Pitch (°)", "Roll (°)", "Yaw (°)", "Pitch Velocity (°/s)", "Roll Velocity (°/s)", "Yaw Velocity (°/s)"]):
            QMessageBox.warning(self, "Invalid File", "The selected file must contain Pitch, Roll, and Yaw columns.")
            return
        
        if ML_model_loaded == 1:
        
            # Detect anomalies in the data
            anomalies = []
            for index, row in df.iterrows():
                pitch = row["Pitch (°)"]
                roll = row["Roll (°)"]
                yaw = row["Yaw (°)"]
                pitch_v = row["Pitch Velocity (°/s)"]
                roll_v = row["Roll Velocity (°/s)"]
                yaw_v = row["Yaw Velocity (°/s)"]

                if self.anomaly_detector.detect_anomaly(pitch, roll, yaw, pitch_v, roll_v, yaw_v):
                    anomalies.append(index)


            self.plot_window = PlotWindow(df, anomalies, movement_regions=None, label_encoder=None)
            self.plot_window.show()  # Display the new window    

        elif ML_model_loaded == 2:
    
            # Prepare data for LSTM model
            feature_cols = ["Pitch (°)", "Roll (°)", "Yaw (°)", "Pitch Velocity (°/s)", "Roll Velocity (°/s)", "Yaw Velocity (°/s)"]
            X = df[feature_cols].values  # Extract relevant features

            # Reshape data for LSTM model (samples, time_steps, features)
            time_steps = 10
            num_samples = X.shape[0] - time_steps + 1  # Ensure we have complete windows
            X_windows = np.array([X[i:i + time_steps] for i in range(num_samples)])

            # Get predictions from the LSTM model
            predicted_labels = self.motion_characteriser.predict(X_windows)    
            # predicted_labels = list(map(int, self.motion_characteriser.predict(X_windows)))  # Ensure labels are integers


            # Find movement regions
            movement_regions = []
            current_start = 0
            current_label = predicted_labels[0]

            for i in range(1, len(predicted_labels)):
                if predicted_labels[i] != current_label:
                    movement_regions.append((current_start, i, current_label))  # (start, end, movement_type)
                    current_start = i
                    current_label = predicted_labels[i]

            # Append the last detected region
            movement_regions.append((current_start, len(predicted_labels), current_label))   

            self.plot_window = PlotWindow(df, anomalies=None, movement_regions=movement_regions,  label_encoder=self.motion_characteriser.label_encoder)

            self.plot_window.show()  # Display the new window     

        else:
            self.plot_window = PlotWindow(df, None, None, None)
            self.plot_window.show()  # Display the new window               


    # def show_plot(self, file_path):

    #     # Add functionality here to select plotting output based on which ML model is loaded 
    #     #----------------------------------------------------------------------------------#

    #     """Open the plot in a new popup window."""
    #     df = pd.read_csv(file_path, encoding="latin1")

    #     # Ensure required columns exist
    #     if not all(col in df.columns for col in ["Pitch (°)", "Roll (°)", "Yaw (°)", "Pitch Velocity (°/s)", "Roll Velocity (°/s)", "Yaw Velocity (°/s)"]):
    #         QMessageBox.warning(self, "Invalid File", "The selected file must contain Pitch, Roll, and Yaw columns.")
    #         return
        
    #     if ML_model_loaded == 1:
        
    #         # Detect anomalies in the data
    #         anomalies = []
    #         for index, row in df.iterrows():
    #             pitch = row["Pitch (°)"]
    #             roll = row["Roll (°)"]
    #             yaw = row["Yaw (°)"]
    #             pitch_v = row["Pitch Velocity (°/s)"]
    #             roll_v = row["Roll Velocity (°/s)"]
    #             yaw_v = row["Yaw Velocity (°/s)"]

    #             if self.anomaly_detector.detect_anomaly(pitch, roll, yaw, pitch_v, roll_v, yaw_v):
    #                 anomalies.append(index)


    #         self.plot_window = PlotWindow(df, anomalies, movement_regions=None, label_encoder=None)
    #         self.plot_window.show()  # Display the new window    

    #     elif ML_model_loaded == 2:
    
    #         # Prepare data for LSTM model
    #         feature_cols = ["Pitch (°)", "Roll (°)", "Yaw (°)", "Pitch Velocity (°/s)", "Roll Velocity (°/s)", "Yaw Velocity (°/s)"]
    #         X = df[feature_cols].values  # Extract relevant features

    #         # Reshape data for LSTM model (samples, time_steps, features)
    #         time_steps = 10
    #         num_samples = X.shape[0] - time_steps + 1  # Ensure we have complete windows
    #         X_windows = np.array([X[i:i + time_steps] for i in range(num_samples)])

    #         # Get predictions from the LSTM model
    #         predicted_labels = self.motion_characteriser.predict(X_windows)    
    #         # predicted_labels = list(map(int, self.motion_characteriser.predict(X_windows)))  # Ensure labels are integers


    #         # Find movement regions
    #         movement_regions = []
    #         current_start = 0
    #         current_label = predicted_labels[0]

    #         for i in range(1, len(predicted_labels)):
    #             if predicted_labels[i] != current_label:
    #                 movement_regions.append((current_start, i, current_label))  # (start, end, movement_type)
    #                 current_start = i
    #                 current_label = predicted_labels[i]

    #         # Append the last detected region
    #         movement_regions.append((current_start, len(predicted_labels), current_label))   

    #         self.plot_window = PlotWindow(df, anomalies=None, movement_regions=movement_regions,  label_encoder=self.motion_characteriser.label_encoder)

    #         self.plot_window.show()  # Display the new window     

    #     else:
    #         self.plot_window = PlotWindow(df, None, None, None)
    #         self.plot_window.show()  # Display the new window               



# Statisitical Analysis Functions ------------------------<


# Machine Learning Functions Isolation Forest
    def select_csv_file_training_IF(self):
        """Open a file dialog to select a CSV file"""
        file_path_ML, _ = QFileDialog.getOpenFileName(self, "Select CSV File for Training", master_csv_path, "CSV Files (*.csv)")
        if file_path_ML:
            self.train_ML_IF(file_path_ML)
        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid CSV file.")     

    def train_ML_IF(self, file_path_ML):
        # display "training model message with pulsating heart"

        complete_message = self.anomaly_detector.train(file_path_ML)
        QMessageBox.warning(self, "Completion of ML Training", complete_message)

        # Prompt user to specify the file path for saving the model
        file_path_ML_Model, _ = QFileDialog.getSaveFileName(self, "Save Model As", "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Master_CSV/model.joblib", "Joblib Files (*.joblib);;All Files (*)")
        if file_path_ML_Model:
            # Save trained model
            saved_message = self.anomaly_detector.save(file_path_ML_Model)
            QMessageBox.warning(self, "Model saved", saved_message)
        else:
            QMessageBox.warning(self, "No File Selected", "Please specify a valid file name to save the model.")

    def load_ML_Model_IF(self):
        
        global ML_model_loaded

        load_ML_Model, _ = QFileDialog.getOpenFileName(self, "Select Joblib Model File", master_csv_path, "Joblib Files (*.joblib);;All Files (*)")
        if load_ML_Model:
            loaded_message = self.anomaly_detector.load(load_ML_Model)
            QMessageBox.information(None, "Success", loaded_message)              

            self.Load_button_style = green_button_style 
            self.Load_button_text = "IF Model Loaded"            

            ML_model_loaded = 1

        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid Master CSV file.")     

        self.init_menu()


# Machine Learning Functions LSTM
    def select_csv_file_training_LSTM(self):

        self.train_ML_LSTM()
    
    def train_ML_LSTM(self):
        # display "training model message with pulsating heart"

        file_path_ML_Master, _ = QFileDialog.getOpenFileName(self, "Select CSV Master File", master_csv_path, "CSV Files (*.csv)")
        if file_path_ML_Master:
            
            history = self.motion_characteriser.train(file_path_ML_Master)  # Get the History object

            # # Extract final accuracy and loss from history
            # final_accuracy = history.history['accuracy'][-1] if 'accuracy' in history.history else None
            # final_loss = history.history['loss'][-1] if 'loss' in history.history else None

            #NEW----------------------------------------------------------------------------------------------

        # Extract training performance
            final_accuracy = history.history.get('accuracy', [None])[-1]
            final_loss = history.history.get('loss', [None])[-1]
            val_accuracy = history.history.get('val_accuracy', [None])[-1]
            val_loss = history.history.get('val_loss', [None])[-1]

            # Get model details
            model = self.motion_characteriser.model
            optimizer = model.optimizer.__class__.__name__
            loss_function = model.loss

            num_layers = len(model.layers)
            trainable_params = model.count_params()
            input_shape = model.input_shape
            num_classes = model.output_shape[-1]

            # Get dataset details
            X_train, X_val, y_train, y_val, _ = self.motion_characteriser.load_and_preprocess_data(file_path_ML_Master)
            num_train_samples = X_train.shape[0]
            num_val_samples = X_val.shape[0]

            # Get LSTM Layer Details
            lstm_units = [layer.units for layer in model.layers if isinstance(layer, LSTM)]
            dropout_rates = [layer.rate for layer in model.layers if isinstance(layer, Dropout)]

            # Create table data
            data = [
                ["Final Training Accuracy", f"{final_accuracy:.4f}"],
                ["Final Training Loss", f"{final_loss:.4f}"],
                ["Validation Accuracy", f"{val_accuracy:.4f}"],
                ["Validation Loss", f"{val_loss:.4f}"],
                ["Optimizer", optimizer],
                ["Loss Function", loss_function],
                ["Number of Layers", num_layers],
                ["Trainable Parameters", trainable_params],
                ["Input Shape", input_shape],
                ["Number of Movement Classes", num_classes],
                ["Training Samples", num_train_samples],
                ["Validation Samples", num_val_samples],
                ["LSTM Layer Units", ', '.join(map(str, lstm_units))],
                ["Dropout Rates", ', '.join(map(str, dropout_rates))]
            ]

            # Print table
            print("\n" + tabulate(data, headers=["Parameter", "Value"], tablefmt="fancy_grid"))

            #NEW----------------------------------------------------------------------------------------------



            # Create a summary message
            if final_accuracy is not None and final_loss is not None:
                complete_message = f"Training Complete ✅\nFinal Accuracy: {final_accuracy:.4f}\nFinal Loss: {final_loss:.4f}"
            else:
                complete_message = "Training Complete ✅ (Accuracy/Loss Not Available)"

            QMessageBox.warning(None, "Completion of ML Training", complete_message)

        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid Master CSV file.")

    def load_ML_Model_LSTM(self):
        
        global ML_model_loaded

        load_ML_Model, _ = QFileDialog.getOpenFileName(self, "Select LSTM Model File", master_csv_path, "HDF5 Files (*.h5);;All Files (*)")
        if load_ML_Model:
            loaded_message = self.motion_characteriser.load_model(load_ML_Model)
            QMessageBox.information(None, "Success", loaded_message)              

            self.Load_button_style = green_button_style 
            self.Load_button_text = "LSTM Model Loaded"   

            ML_model_loaded = 2

        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid Master CSV file.")     

        self.init_menu()


# CSV Data Handling Functions

    def append_new_data_to_master(self):

        file_path_training_set, _ = QFileDialog.getOpenFileName(self, "Select CSV File for Training", file_directory, "CSV Files (*.csv)")
        if file_path_training_set:


            file_path_master, _ = QFileDialog.getOpenFileName(self, "Select CSV Master File to Append Data to", master_csv_path, "CSV Files (*.csv)")
            if file_path_master:
                self.append_to_master_csv(file_path_training_set, file_path_master)
            else:
                QMessageBox.warning(self, "No File Selected", "Please select a valid CSV file.") 

        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid CSV file.")  
 
    def append_to_master_csv(self, file_path_training_set, file_path_master):
        try:
            # Read the new CSV file, skipping the first row (header)
            with open(file_path_training_set, 'r') as f1:
                # Skip the first line (header)
                f1.readline()  # Read and ignore the header line
                new_data = f1.read()

            # Check if master CSV file exists
            try:
                # Open master CSV in append mode
                with open(file_path_master, 'a') as f2:
                    # f2.write('\n')  # Ensure there's a newline before appending new data
                    f2.write(new_data)  # Append new data
            except FileNotFoundError:
                # If master CSV doesn't exist, create it and write the new data
                with open(master_csv_path, 'w') as f2:
                    f2.write(new_data)

            QMessageBox.information(None, "Success", "Data appended to master CSV successfully.")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to append data: {str(e)}")



