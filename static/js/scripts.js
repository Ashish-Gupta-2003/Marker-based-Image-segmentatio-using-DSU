let markers = [];
let markerCount = 1;

function addMarker(event) {
    const img = document.getElementById('image');
    const rect = img.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    
    // Scale the coordinates to the original image size
    const originalWidth = img.naturalWidth;
    const originalHeight = img.naturalHeight;
    const displayedWidth = rect.width;
    const displayedHeight = rect.height;
    
    const scaledX = Math.round(x * (originalWidth / displayedWidth));
    const scaledY = Math.round(y * (originalHeight / displayedHeight));

    // Use the displayed coordinates for positioning the markers
    const marker = { scaledX, scaledY, displayX: x, displayY: y, name: `Marker ${markerCount++}` };
    markers.push(marker);

    console.log(`Marker added at: (${x}, ${y})`); // Debugging: log the marker coordinates
    console.log('Markers array:', markers); // Debugging: log the markers array

    displayMarker(marker, markers.length - 1);
}

function displayMarker(marker, index) {
    const markerList = document.getElementById('marker-list');

    const markerItem = document.createElement('div');
    markerItem.classList.add('marker-item');
    markerItem.dataset.index = index;

    const markerName = document.createElement('span');
    markerName.textContent = marker.name;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.classList.add('delete-button');
    deleteButton.onclick = () => deleteMarker(index);

    markerItem.appendChild(markerName);
    markerItem.appendChild(deleteButton);
    markerList.appendChild(markerItem);
}

function deleteMarker(index) {
    markers = markers.filter((_, i) => i !== index);
    updateMarkersDisplay();
}

function updateMarkersDisplay() {
    const markerList = document.getElementById('marker-list');
    markerList.innerHTML = '<h3>Markers</h3>';

    markers.forEach((marker, index) => displayMarker(marker, index));
}

function submitMarkers() {
    console.log(`Submitting markers: ${JSON.stringify(markers)}`); // Debugging: log the markers

    fetch('/process_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename, markers })
    })
        .then(response => response.json())
        .then(data => {
            const segmented_image_path = data.segmented_image_path;
            window.location.href = `/result/${segmented_image_path}`;
        });
}
