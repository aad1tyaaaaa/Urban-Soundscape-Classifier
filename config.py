import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg'}
    
    # Model settings
    MODEL_PATH = 'models/urban_sound_classifier.h5'
    LABELS = ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark',
              'drilling', 'engine_idling', 'gun_shot', 'jackhammer', 'siren', 'street_music']
    
    # Audio processing
    SAMPLE_RATE = 22050
    DURATION = 3  # seconds
    N_MELS = 128
    
    # Map settings
    MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
    DEFAULT_LAT = 40.7128
    DEFAULT_LNG = -74.0060
    DEFAULT_ZOOM = 12

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
