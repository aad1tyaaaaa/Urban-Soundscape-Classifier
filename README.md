# 🎧 Urban Soundscape Classifier

> An intelligent audio classification system for detecting and mapping urban sounds using machine learning.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

</div>

## 🛠️ Technical Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend Framework** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask) |
| **Machine Learning** | ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow) ![Scikit Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=flat&logo=scikit-learn) ![Librosa](https://img.shields.io/badge/Librosa-3776AB?style=flat) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript) |
| **Audio Processing** | ![Librosa](https://img.shields.io/badge/Librosa-3776AB?style=flat) ![SoundFile](https://img.shields.io/badge/SoundFile-FF6B6B?style=flat) |
| **Mapping** | ![OpenStreetMap](https://img.shields.io/badge/OpenStreetMap-7EBC6F?style=flat&logo=openstreetmap) ![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat) |

</div>

## ✨ Features

- 🎵 **Real-time Audio Classification**: Upload audio files to classify urban sounds
- 🗺️ **Interactive Noise Map**: Visualize noise pollution data on OpenStreetMap
- 🤖 **Machine Learning Pipeline**: TensorFlow-based classification with Librosa feature extraction
- 💻 **Web Interface**: Clean, responsive Flask web application
- 📍 **Noise Hotspot Detection**: Identify areas with high noise pollution

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd urban-sound-classifier
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create directory structure:
```bash
mkdir -p models data/training static/uploads
```

## Usage

### Training the Model

1. Prepare your dataset in the following structure:
```
data/training/
├── air_conditioner/
├── car_horn/
├── children_playing/
├── dog_bark/
├── drilling/
├── engine_idling/
├── gun_shot/
├── jackhammer/
├── siren/
└── street_music/
```

2. Train the model:
```bash
python ml_pipeline/train.py
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser to:
- Main application: http://localhost:5000
- Noise map: http://localhost:5000/map

### API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Upload and classify audio
- `GET /map` - Interactive noise pollution map
- `GET /api/noise-data` - Get noise pollution data
- `GET /health` - Health check

## Audio Classification Categories

The system can classify the following urban sounds:

1. **Air Conditioner** - HVAC system sounds
2. **Car Horn** - Vehicle horn sounds
3. **Children Playing** - Sounds of children at play
4. **Dog Bark** - Canine vocalizations
5. **Drilling** - Construction drilling sounds
6. **Engine Idling** - Vehicle engine sounds
7. **Gun Shot** - Firearm discharge sounds
8. **Jackhammer** - Pneumatic tool sounds
9. **Siren** - Emergency vehicle sirens
10. **Street Music** - Live musical performances

## File Structure

```
urban-sound-classifier/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── models/              # Trained model files
├── data/                # Dataset directory
│   └── training/        # Training data organized by category
├── ml_pipeline/         # Machine learning components
│   ├── train.py        # Model training script
│   └── model.py        # Model definition
├── utils/              # Utility functions
│   └── audio_processor.py  # Audio processing utilities
├── static/             # Static web assets
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript files
│   ├── uploads/       # Uploaded audio files
│   └── audio/         # Sample audio files
├── templates/          # HTML templates
└── tests/             # Test files
```

## Configuration

Edit `config.py` to customize:

- Audio processing parameters
- Model settings
- Map configuration
- Upload limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- UrbanSound8K dataset for training data
- TensorFlow team for the ML framework
- OpenStreetMap contributors for mapping data
