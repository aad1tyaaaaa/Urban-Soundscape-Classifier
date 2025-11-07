import numpy as np
import tensorflow as tf

class UrbanSoundClassifier:
    def __init__(self):
        self.model = None

    def load_model(self):
        """Load the trained model from disk."""
        self.model = tf.keras.models.load_model('models/urban_sound_classifier.h5')

    def predict(self, features):
        """Predict the class of the given audio features."""
        features = np.expand_dims(features, axis=0)  # Add batch dimension
        predictions = self.model.predict(features)
        return predictions

    def get_top_predictions(self, predictions, top_k=3):
        """Get the top K predictions with their confidence scores."""
        top_indices = np.argsort(predictions[0])[-top_k:][::-1]
        top_scores = predictions[0][top_indices]
        return [(index, score) for index, score in zip(top_indices, top_scores)]
