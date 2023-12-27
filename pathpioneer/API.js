const API_KEY = 'AIzaSyCPsqAOFiYHgfX0mKLHeOChxQkGY-03JWc'

export async function getRoute() {
    // Default options are marked with *
    const response = await fetch('https://routes.googleapis.com/directions/v2:computeRoutes', {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline'
      },
      body: JSON.stringify({"origin":{
        "location":{
            "latLng":{
        "latitude": 37.419734,
        "longitude": -122.0827784
      }
    }
    },
    "destination":{
    "location":{
      "latLng":{
        "latitude": 37.417670,
        "longitude": -122.079595
      }
    }
  },
  "travelMode": "DRIVE",
  "routingPreference": "TRAFFIC_AWARE",
  "departureTime": "2024-10-15T15:01:23.045123456Z",
  "computeAlternativeRoutes": false,
  "routeModifiers": {
    "avoidTolls": false,
    "avoidHighways": false,
    "avoidFerries": false
  },
  "languageCode": "en-US",
  "units": "IMPERIAL"}), // body data type must match "Content-Type" header
    })
    .then((result) => result.json())
    .then((data) => console.log(data.routes[0]));
}

export async function getLonLat() {
    // Default options are marked with *
    const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?place_id=ChIJeRpOeF67j4AR9ydy_PIzPuM&key=${API_KEY}`, {
        headers: {
            "Content-Type": "application/json"
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        method: "GET", // *GET, POST, PUT, DELETE, etc.
    })
    .then((result) => result.json())
    .then((data) => console.log(data));
}

  export async function getDistanceMatrix() {
    const url = 'https://maps.googleapis.com/maps/api/distancematrix/json';
    const params = {
        destinations: 'New York City, NY',
        origins: 'Washington, DC|Boston',
        units: 'imperial',
        key: API_KEY
    };

    // Construct the full URL with parameters
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = `${url}?${queryString}`;

    try {
        const response = await fetch(fullUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data.rows[0].elements[0]) // This will be the JSON response
    } catch (error) {
        console.error('Error fetching distance matrix:', error);
    }
}