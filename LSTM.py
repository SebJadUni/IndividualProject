import numpy as np                  # Handles numerical operations (e.g. reshaping data, making predicitions)
import tensorflow as tf             # Deep learning framework used to create and train the LSTM model
from keras import Sequential                  # Used to build a sequential neural network where layers stack on top of eachother 
# from tensorflow.keras.models import Sequential                  # Used to build a sequential neural network where layers stack on top of eachother 
import os
import joblib
import pandas as pd 

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from collections import Counter, deque
# from keras import LSTM, Dense, Dropout        
from tensorflow.keras.layers import LSTM, Dense, Dropout    

from sklearn.model_selection import train_test_split

# LSTM - A Long Short-Term Memory layer that learns from sequential time-series data
# Dense - Fully connected layers for classification
# Dropout - A technique to prevent overfitting by randomly ignoring neurons during training 
from sklearn.preprocessing import LabelEncoder, StandardScaler 
# LabelEncoder - Converts categorical movement labels (e.g. "Nod", "Shake") into numerical format
# StandardScaler - Normalises input data to improve training performance
# from keras import to_categorical # Converts integer labels into a one-hot encoded format for classification
from tensorflow.keras.utils import to_categorical # Converts integer labels into a one-hot encoded format for classification

class MovementClassifier:
    def __init__(self, input_shape, num_classes, smoothing_window=10):
        # input_shape => defines shape of input IMU data, e.g. (10,6) => 10 time steps and 6 features
        # num_classes => defines the number of movement categories (e.g. 3 for "Nod", "Shake", "Tilt")

        self.model_trained = False

        self.model = self.build_model(input_shape, num_classes)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        # categorical_crossentropy => loss function for multi-class classification
        # adam optimiser => adjusts learning rate dynamically for better convergence
        # accuracy metric => tracks classification accuracy during training 
            
            # Store previous predictions for smoothing
        self.prediction_history = []
        self.smoothing_window = smoothing_window  # How many past predictions to consider


    # Building the LSTM Model
    def build_model(self, input_shape, num_classes):
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=input_shape),
            # 64 LSTM units => memory cells to capture sequential movement patterns
            # return_sequence_true => ensures next LSTM layer receives sequences (needed when stacking LSTMs)
            # input_shape => defines 10 time steps x 6 IMU features
            Dropout(0.2),
            # randomly drops 20% of neurons per training step
            # prevents overfitting by forcing the model to generalise
            LSTM(64),
            # another 64-unit LSTM later that processes sequences and outputs final movement features
            Dense(32, activation='relu'),
            # extracts features from LSTM output
            Dense(num_classes, activation='softmax')
            # produces class probabilities (e.g. "nod : 70%", "shake : 20%")
        ])
        return model


    # Training the Model
    def train(self, file_path_csv, epochs=70, batch_size=32):
        # Pre-process the data 
        X_train, X_val, y_train, y_val, label_encoder = self.load_and_preprocess_data(file_path_csv)
        self.label_encoder = label_encoder  # Store it in the class
        
        # Train the Model
        history = self.model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)

        print("Model Trained ✅")

        self.model_trained = True

        file_path_ML_Model, _ = QFileDialog.getSaveFileName(None, "Save Model As", "C:/Users/ASUS/Documents/UOM-Y3-2024-2025/IndividualProject/DataGathering/Master_CSV/model.h5", "HDF5 Files (*.h5);;All Files (*)")
        if file_path_ML_Model:
            # Save trained model
            saved_message = self.save_model(file_path_ML_Model)
            joblib.dump(self.label_encoder, file_path_ML_Model.replace(".h5", "_labels.pkl"))  # Save label encoder

            QMessageBox.warning(None, "Model saved", saved_message)

        else:
            QMessageBox.warning(None, "No File Selected", "Please specify a valid file name to save the model.")            
        
        return history
        # X_train, y_train: Training data (IMU readings and corresponding labels).
        # X_val, y_val: Validation set to track model performance during training.
        # epochs=20: The model sees the entire dataset 20 times (increases learning but can overfit if too high).
        # batch_size=32: The model processes 32 samples at a time (tradeoff between memory and efficiency).


    # Saving and Loading the Model
    def save_model(self, file_path):
        self.model.save(file_path)
        return "Model saved ✅"
        
    def load_model(self, file_path):

            self.model = tf.keras.models.load_model(file_path)
            self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])  # Fix for missing metrics
            self.model_trained = True

            # Load label encoder if it exists
            label_encoder_path = os.path.splitext(file_path)[0] + "_labels.pkl"
            print(f"Looking for Label Encoder at: {label_encoder_path}")  # Debugging print

            try:
                if os.path.exists(label_encoder_path):  # ✅ Explicit check
                    self.label_encoder = joblib.load(label_encoder_path)
                    print("Label Encoder loaded ✅")
                else:
                    self.label_encoder = None
                    print("Warning: Label Encoder file not found ❌")

            except FileNotFoundError:
                self.label_encoder = None  # Set as None if label file is missing
            # print("Warning: Label Encoder file not found ❌")
            print("Woopsy")


            return "Model LSTM loaded ✅"

    # Pre-processing Function 
    def load_and_preprocess_data(self, file_path):
        # Load CSV
        df = pd.read_csv(file_path)

        # Define feature columns
        feature_cols = [col for col in df.columns if col not in ["timestamp", "label"]]  # Exclude timestamp and label
        label_col = "label"  # Ensure your CSV has this column

        # Extract X and y
        X = df[feature_cols].values
        y = df[label_col].values

        # Normalize X (scale all features)
        scaler = StandardScaler()
        X = scaler.fit_transform(X)  # Scale all feature values

        # Reshape X into 3D (samples, time_steps, features)
        num_samples = X.shape[0]
        time_steps = 10  # Fixed window size
        num_features = 6  # Each step contains 6 values (pitch, roll, yaw, pitch_v, roll_v, yaw_v)
        X = X.reshape(num_samples, time_steps, num_features)

        # Encode labels into numerical form
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)  # e.g. ["Nod", "Shake", "Roll"] → [0, 1, 2]

        # Convert labels to categorical (one-hot encoding)
        y = to_categorical(y)

        # Split into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        return X_train, X_val, y_train, y_val, label_encoder


# Functions for Post-Processing

    # Making Predictions
    def predict(self, X):
        # return np.argmax(self.model.predict(X), axis=1)   # old version

        """Predicts movement while applying a moving average smoothing filter."""
        raw_predictions = np.argmax(self.model.predict(X), axis=1)

        # Initialize a deque for efficient sliding window smoothing
        smoothed_predictions = []
        prediction_history = deque(maxlen=self.smoothing_window)

        for pred in raw_predictions:
            prediction_history.append(pred)  # Add new prediction
            most_common_label = Counter(prediction_history).most_common(1)[0][0]
            smoothed_predictions.append(most_common_label)  # Use smoothed prediction

        return smoothed_predictions  # Return a properly smoothed sequence
       
        # Takes a new IMU sequence and predicts movement.
        # np.argmax() finds the class with the highest probability
        # Model output: [0.2, 0.7, 0.1] → Class 1 (e.g., "Shake").

    def extract_attention_weights(self):
        """Extract attention scores for analysis."""
        attention_layer = self.model.get_layer(index=2)
        attention_model = tf.keras.Model(self.model.input, attention_layer.output)
        return attention_model


# X: The input features (e.g., pitch, roll, yaw, and their velocities).
# y: The labels (e.g., movement types like "Nod", "Shake", "Tilt").

# StandardScaler() scales the input data so that it has zero mean and unit variance, improving training stability.
# X.reshape(-1, X.shape[-1]):
# This flattens all time steps into a 2D shape so that StandardScaler can process it.
# fit_transform(X): Learns the mean and variance from training data and applies normalization.
# reshape(X.shape): Reshapes the data back into the original 3D shape (samples, time steps, features), which is required for LSTMs.
# LabelEncoder() converts categorical labels (e.g., "Nod", "Shake") into integer values (0, 1, 2...).
# This is necessary because neural networks work with numbers, not text.

# to_categorical
# Converts the encoded labels into a one-hot encoded format.
# Example: If you have 3 classes ("Nod", "Shake", "Tilt") and "Shake" is labeled as 1, one-hot encoding turns it into [0,1,0].
# This is required for categorical_crossentropy, the loss function used in multi-class classification.

# Returns the preprocessed input data (X)
# Returns the one-hot encoded labels (y)
# Returns the label encoder (so you can later decode predictions back into movement names).
