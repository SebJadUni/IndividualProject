import pandas as pd
import numpy as np
import collections
from sklearn.ensemble import IsolationForest
import joblib

class AnomalyDetector:
    def __init__(self, window_size=5):
        self.model = None
        self.model_trained = False
        self.window_size = window_size
        self.imu_window = collections.deque(maxlen=self.window_size)


    def train(self, file_path):
        """Train Isolation Forest using a CSV dataset."""
        training_file = pd.read_csv(file_path)
        training_data = training_file.iloc[:, 1:-1].values  # Exclude timestamp & label

        # Train model
        self.model = IsolationForest(random_state=42)
        self.model.fit(training_data)

        self.model_trained = True
        return "Training complete ✅"

    def save(self, file_path):
        """Save trained model to file."""
        if not self.model_trained:
            return "Error: Train model first!"
        
        joblib.dump(self.model, file_path)
        return "Model saved ✅"

    def load(self, file_path):
        """Load trained model from file."""
        self.model = joblib.load(file_path)
        self.model_trained = True
        return "Model loaded ✅"

    def detect_anomaly(self, pitch, roll, yaw, pitch_v, roll_v, yaw_v):
        """Detect anomalies using trained model."""
        if not self.model_trained:
            return False

        self.imu_window.append([pitch, roll, yaw, pitch_v, roll_v, yaw_v])
        if len(self.imu_window) < self.window_size:
            return False

        window_data = np.array(self.imu_window).flatten().reshape(1, -1)
        prediction = self.model.predict(window_data)

        return prediction[0] == -1  # True if anomaly detected


