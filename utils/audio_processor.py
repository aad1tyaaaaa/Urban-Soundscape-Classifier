import librosa
import numpy as np
from config import Config

class AudioProcessor:
    def __init__(self):
        self.config = Config()
    
    def extract_features(self, file_path):
        """Extract mel-spectrogram features from audio file."""
        try:
            # Load audio file
            y, sr = librosa.load(
                file_path, 
                sr=self.config.SAMPLE_RATE, 
                duration=self.config.DURATION
            )
            
            # Ensure consistent length
            if len(y) < self.config.SAMPLE_RATE * self.config.DURATION:
                y = np.pad(y, (0, self.config.SAMPLE_RATE * self.config.DURATION - len(y)))
            
            # Extract mel-spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=y, 
                sr=sr, 
                n_mels=self.config.N_MELS,
                hop_length=512,
                n_fft=2048
            )
            
            # Convert to log scale
            log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Normalize
            log_mel_spec = (log_mel_spec - np.mean(log_mel_spec)) / np.std(log_mel_spec)
            
            # Add channel dimension for CNN
            log_mel_spec = np.expand_dims(log_mel_spec, axis=-1)
            
            return log_mel_spec
            
        except Exception as e:
            raise Exception(f"Error processing audio file: {str(e)}")
    
    def get_audio_info(self, file_path):
        """Get basic information about the audio file."""
        try:
            y, sr = librosa.load(file_path, sr=None)
            duration = len(y) / sr
            
            return {
                'duration': duration,
                'sample_rate': sr,
                'channels': 1 if y.ndim == 1 else y.shape[0]
            }
        except Exception as e:
            raise Exception(f"Error getting audio info: {str(e)}")
    
    def preprocess_audio(self, file_path):
        """Complete preprocessing pipeline for audio file."""
        features = self.extract_features(file_path)
        info = self.get_audio_info(file_path)
        
        return {
            'features': features,
            'info': info
        }
