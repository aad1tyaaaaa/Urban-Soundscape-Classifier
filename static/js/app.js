// Global variables
let map;
let noiseLayer;
let heatmapLayer;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    setupEventListeners();
    loadNoiseData();
});

// Event listeners
function setupEventListeners() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleUpload);
    }
}

// Handle file upload
async function handleUpload(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select an audio file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
            // Add to map
            addNoiseToMap(data.predictions[0][0], data.predictions[0][1]);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error uploading file: ' + error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

// Display classification results
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const predictionsDiv = document.getElementById('predictions');
    
    predictionsDiv.innerHTML = '';
    
    data.predictions.forEach(([index, confidence]) => {
        const soundTypes = [
            'Air Conditioner', 'Car Horn', 'Children Playing', 'Dog Bark',
            'Drilling', 'Engine Idling', 'Gun Shot', 'Jackhammer', 'Siren', 'Street Music'
        ];
        
        const div = document.createElement('div');
        div.className = 'prediction-item';
        div.innerHTML = `
            <div class="sound-type">${soundTypes[index]}</div>
            <div class="confidence">${(confidence * 100).toFixed(1)}% confidence</div>
        `;
        predictionsDiv.appendChild(div);
    });
    
    // Set up audio player
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.src = `/static/uploads/${data.filename}`;
    
    resultsDiv.classList.remove('hidden');
}

// Initialize map
function initializeMap() {
    if (typeof L === 'undefined') return;
    
    map = L.map('map').setView([40.7589, -73.9851], 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    noiseLayer = L.layerGroup().addTo(map);
}

// Load noise data
async function loadNoiseData() {
    try {
        const response = await fetch('/api/noise-data');
        const data = await response.json();
        
        displayNoiseData(data);
    } catch (error) {
        console.error('Error loading noise data:', error);
    }
}

// Display noise data on map
function displayNoiseData(data) {
    if (!map) return;
    
    noiseLayer.clearLayers();
    
    data.forEach(item => {
        const color = getColorForSoundType(item.sound_type);
        const marker = L.circleMarker([item.lat, item.lng], {
            color: color,
            fillColor: color,
            fillOpacity: 0.7,
            radius: 10 + (item.intensity * 20)
        });
        
        marker.bindPopup(`
            <strong>${item.sound_type}</strong><br>
            Intensity: ${(item.intensity * 100).toFixed(0)}%<br>
            Time: ${new Date(item.timestamp).toLocaleString()}
        `);
        
        noiseLayer.addLayer(marker);
    });
}

// Get color for sound type
function getColorForSoundType(soundType) {
    const colors = {
        'siren': '#ff4444',
        'construction': '#ff8800',
        'traffic': '#ffaa00',
        'street_music': '#44ff44',
        'default': '#4444ff'
    };
    
    return colors[soundType] || colors.default;
}

// Add noise to map
function addNoiseToMap(soundType, intensity) {
    if (!map) return;
    
    // Get current center
    const center = map.getCenter();
    
    // Add marker
    const color = getColorForSoundType(soundType);
    const marker = L.circleMarker([center.lat, center.lng], {
        color: color,
        fillColor: color,
        fillOpacity: 0.7,
        radius: 10 + (intensity * 20)
    });
    
    marker.bindPopup(`
        <strong>Live Classification</strong><br>
        Type: ${soundType}<br>
        Intensity: ${(intensity * 100).toFixed(1)}%
    `);
    
    noiseLayer.addLayer(marker);
}

// Utility functions
function centerMap() {
    if (map) {
        map.setView([40.7589, -73.9851], 12);
    }
}

// File input styling
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('audioFile');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'Choose Audio File';
            document.querySelector('.file-label span').textContent = fileName;
        });
    }
});
