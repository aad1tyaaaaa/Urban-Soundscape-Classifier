// Global variables
let map;
let noiseLayer;
let heatmapLayer;
let noiseData = [];

// Initialize map
function initMap() {
    // Initialize map centered on NYC
    map = L.map('map').setView([40.7589, -73.9851], 12);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Initialize layers
    noiseLayer = L.layerGroup().addTo(map);
    
    // Load initial data
    loadNoiseData();
}

// Load noise data from API
async function loadNoiseData() {
    try {
        const response = await fetch('/api/noise-data');
        const data = await response.json();
        noiseData = data;
        
        displayNoiseMarkers(data);
        updateHeatmap(data);
    } catch (error) {
        console.error('Error loading noise data:', error);
    }
}

// Display noise markers on map
function displayNoiseMarkers(data) {
    noiseLayer.clearLayers();
    
    data.forEach(item => {
        const marker = createNoiseMarker(item);
        noiseLayer.addLayer(marker);
    });
}

// Create marker for noise data
function createNoiseMarker(item) {
    const color = getColorForSoundType(item.sound_type);
    const intensity = item.intensity || 0.5;
    
    const marker = L.circleMarker([item.lat, item.lng], {
        color: color,
        fillColor: color,
        fillOpacity: 0.7,
        radius: 5 + (intensity * 15),
        weight: 2
    });
    
    const popupContent = `
        <div class="popup-content">
            <h4>${capitalizeFirst(item.sound_type)}</h4>
            <p><strong>Intensity:</strong> ${(intensity * 100).toFixed(1)}%</p>
            <p><strong>Time:</strong> ${new Date(item.timestamp).toLocaleString()}</p>
            <p><strong>Location:</strong> ${item.lat.toFixed(4)}, ${item.lng.toFixed(4)}</p>
        </div>
    `;
    
    marker.bindPopup(popupContent);
    
    marker.on('click', function() {
        updateInfoPanel(item);
    });
    
    return marker;
}

// Update heatmap layer
function updateHeatmap(data) {
    if (heatmapLayer) {
        map.removeLayer(heatmapLayer);
    }
    
    // Create heatmap data
    const heatmapData = data.map(item => ({
        lat: item.lat,
        lng: item.lng,
        intensity: item.intensity || 0.5
    }));
    
    // Simple heatmap implementation using circle markers
    heatmapLayer = L.layerGroup();
    
    heatmapData.forEach(point => {
        const circle = L.circle([point.lat, point.lng], {
            color: 'transparent',
            fillColor: '#ff0000',
            fillOpacity: point.intensity * 0.3,
            radius: 100
        });
        heatmapLayer.addLayer(circle);
    });
}

// Toggle heatmap visibility
function toggleHeatmap() {
    if (map.hasLayer(heatmapLayer)) {
        map.removeLayer(heatmapLayer);
    } else {
        heatmapLayer.addTo(map);
    }
}

// Get color for sound type
function getColorForSoundType(soundType) {
    const colors = {
        'air_conditioner': '#888888',
        'car_horn': '#ff4444',
        'children_playing': '#44ff44',
        'dog_bark': '#ff8800',
        'drilling': '#ffaa00',
        'engine_idling': '#666666',
        'gun_shot': '#ff0000',
        'jackhammer': '#ff6600',
        'siren': '#ff0088',
        'street_music': '#8844ff'
    };
    
    return colors[soundType] || '#4444ff';
}

// Update info panel
function updateInfoPanel(item) {
    const infoPanel = document.getElementById('location-info');
    
    infoPanel.innerHTML = `
        <h4>${capitalizeFirst(item.sound_type)}</h4>
        <p><strong>Intensity:</strong> ${(item.intensity * 100).toFixed(1)}%</p>
        <p><strong>Coordinates:</strong> ${item.lat.toFixed(4)}, ${item.lng.toFixed(4)}</p>
        <p><strong>Recorded:</strong> ${new Date(item.timestamp).toLocaleString()}</p>
    `;
}

// Center map on NYC
function centerMap() {
    map.setView([40.7589, -73.9851], 12);
}

// Add new noise data
function addNoiseData(soundType, intensity, lat, lng) {
    const newData = {
        sound_type: soundType,
        intensity: intensity,
        lat: lat,
        lng: lng,
        timestamp: new Date().toISOString()
    };
    
    noiseData.push(newData);
    displayNoiseMarkers(noiseData);
    updateHeatmap(noiseData);
}

// Utility functions
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, ' ');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    
    // Add some sample data if no data exists
    if (noiseData.length === 0) {
        setTimeout(() => {
            loadNoiseData();
        }, 1000);
    }
});

// Handle map events
map?.on('click', function(e) {
    // Add noise data at click location
    const soundTypes = ['siren', 'construction', 'traffic', 'street_music'];
    const randomType = soundTypes[Math.floor(Math.random() * soundTypes.length)];
    const randomIntensity = Math.random();
    
    addNoiseData(randomType, randomIntensity, e.latlng.lat, e.latlng.lng);
});
