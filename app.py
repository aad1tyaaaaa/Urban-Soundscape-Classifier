from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import numpy as np
from ml_pipeline.model import UrbanSoundClassifier
from utils.audio_processor import AudioProcessor
from config import config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['default'])

# Initialize classifier and processor
classifier = UrbanSoundClassifier()
processor = AudioProcessor()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Home page with upload interface."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and classification."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process audio and classify
            features = processor.extract_features(filepath)
            prediction = classifier.predict(features)
            
            # Get top 3 predictions with confidence
            top_predictions = classifier.get_top_predictions(prediction, top_k=3)
            
            result = {
                'filename': filename,
                'predictions': top_predictions,
                'success': True
            }
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/classify', methods=['POST'])
def classify_api():
    """API endpoint for classification."""
    return upload_file()

@app.route('/map')
def noise_map():
    """Interactive noise pollution map."""
    return render_template('map.html')

@app.route('/api/noise-data')
def get_noise_data():
    """API endpoint for noise pollution data."""
    # This would fetch real data from database
    # For demo, return sample data
    sample_data = [
        {
            'lat': 40.7589,
            'lng': -73.9851,
            'sound_type': 'siren',
            'intensity': 0.8,
            'timestamp': '2024-01-15T10:30:00Z'
        },
        {
            'lat': 40.7505,
            'lng': -73.9934,
            'sound_type': 'construction',
            'intensity': 0.9,
            'timestamp': '2024-01-15T11:15:00Z'
        }
    ]
    return jsonify(sample_data)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': '2024-01-15T12:00:00Z'})

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Load model on startup
    try:
        classifier.load_model()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load model - {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
