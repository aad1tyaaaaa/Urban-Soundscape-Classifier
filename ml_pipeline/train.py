import os
import numpy as np
import librosa
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from config import Config

class ModelTrainer:
    def __init__(self):
        self.config = Config()
        self.label_encoder = LabelEncoder()
        
    def extract_features(self, file_path):
        """Extract mel-spectrogram features from audio file."""
        try:
            # Load audio file
            y, sr = librosa.load(file_path, sr=self.config.SAMPLE_RATE, duration=self.config.DURATION)
            
            # Extract mel-spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=y, 
                sr=sr, 
                n_mels=self.config.N_MELS
            )
            
            # Convert to log scale
            log_mel_spec = librosa.power_to_db(mel_spec)
            
            # Normalize
            log_mel_spec = (log_mel_spec - np.mean(log_mel_spec)) / np.std(log_mel_spec)
            
            return log_mel_spec
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def load_dataset(self, data_path):
        """Load and preprocess the dataset."""
        features = []
        labels = []
        
        # Walk through dataset directory
        for label in self.config.LABELS:
            label_path = os.path.join(data_path, label)
            if not os.path.exists(label_path):
                continue
                
            for file in os.listdir(label_path):
                if file.endswith(('.wav', '.mp3', '.flac')):
                    file_path = os.path.join(label_path, file)
                    feature = self.extract_features(file_path)
                    
                    if feature is not None:
                        features.append(feature)
                        labels.append(label)
        
        # Convert to numpy arrays
        features = np.array(features)
        labels = np.array(labels)
        
        # Encode labels
        labels_encoded = self.label_encoder.fit_transform(labels)
        
        return features, labels_encoded
    
    def build_model(self, input_shape, num_classes):
        """Build the CNN model for audio classification."""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, data_path, model_path='models/urban_sound_classifier.h5'):
        """Train the model on the dataset."""
        print("Loading dataset...")
        features, labels = self.load_dataset(data_path)
        
        # Reshape features for CNN (add channel dimension)
        features = features.reshape(features.shape[0], features.shape[1], features.shape[2], 1)
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )
        
        # Build model
        input_shape = (features.shape[1], features.shape[2], 1)
        num_classes = len(self.config.LABELS)
        
        model = self.build_model(input_shape, num_classes)
        
        # Train model
        print("Training model...")
        history = model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=32,
            validation_data=(X_test, y_test),
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_accuracy = model.evaluate(X_test, y_test)
        print(f"Test accuracy: {test_accuracy:.4f}")
        
        # Save model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save(model_path)
        print(f"Model saved to {model_path}")
        
        return model, history

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train('data/training')
