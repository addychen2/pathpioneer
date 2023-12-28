export async function getRoute() {
    // Default options are marked with *
    const response = await fetch('https://routes.googleapis.com/directions/v2:computeRoutes', {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
        'X-Goog-Api-Key': 'AIzaSyCPsqAOFiYHgfX0mKLHeOChxQkGY-03JWc',
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
    .then((data) => console.log(data.routes[0].polyline));
  }

export async function sendAddress(){
  const response = await fetch('https://127.0.0.1/whatever', {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(
        {
        "hierarchy": [["addresses in hierarchy 1", "address 2 in hierarchy 1"], ["addresses in hierarchy 2......", "address 2 in hierarchy 2"], ["etc...."]] // hierarchy corresponds to index in array
      }), // body data type must match "Content-Type" header
    })
    .then((result) => result.json())
    .then((data) => console.log(data));
}
