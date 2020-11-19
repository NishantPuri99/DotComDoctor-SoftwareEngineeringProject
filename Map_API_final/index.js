
const here = {
   id : 'pta1H2sVHzLh5CNPif7h',
   apiKey: 'EEMxGvUh7Mq3XQq64jA4j-fwJCfmKtm2-4OvIkj8q_Y'
};

const map = L.map('map', {
   center: [30.767343, 76.787078],
   zoom: 13,
   layers: [
      Tangram.leafletLayer({
         scene: 'scene.yaml',
         events: {
            click: onMapClick
         }
      })
   ],
   zoomControl: false
});

var popup = L.popup();
let startCoordinates = '';

document.getElementById('clear').onclick = clearMap;
document.getElementById('change-start').onclick = addStartingMarker;
addStartingMarker();

async function geocode(query) {
   const url = `https://geocoder.ls.hereapi.com/6.2/geocode.json
?apiKey=${here.apiKey}&searchtext=${query}`
   const response = await fetch(url);
   const data = await response.json();
   return await data.Response.View[0].Result[0].Location.NavigationPosition[0];
}

async function route(start, end) {
   const mode = document.querySelector('input[name="routing-mode"]:checked').value;
   const url = `https://route.ls.hereapi.com/routing/7.2/calculateroute.json
?apiKey=${here.apiKey}&waypoint0=geo!${start}&waypoint1=geo!${end}&mode=fastest;${mode};traffic:disabled&routeattributes=shape`
   const response = await fetch(url);
   const data = await response.json();
   return await data.response.route[0];
}

function clearMap() {
   map.eachLayer((layer) => {
      if (!layer.hasOwnProperty('_updating_tangram') && !layer.options.hasOwnProperty('alt')) {
         map.removeLayer(layer);
      }
   });
}

async function addStartingMarker() {
   clearMap();
   const startAddress = document.getElementById('start').value;
   startCoordinates = await geocode(startAddress);
   const startingCircle = L.marker([startCoordinates.Latitude, startCoordinates.Longitude], {alt: 'start'}).addTo(map);
}

async function onMapClick(selection) {
   if (selection.feature) {
      var latlng = selection.leaflet_event.latlng;
      var label = selection.feature.properties.Name;
      var type = selection.feature.properties.Type;
      var contact = selection.feature.properties.Contact;
      showPopup(latlng, label, type, contact);  
      const endCoordinates = `${selection.leaflet_event.latlng.lat},${selection.leaflet_event.latlng.lng}`;
      const routeData = await route(`${startCoordinates.Latitude},${startCoordinates.Longitude}`, endCoordinates);
      const shape = routeData.shape.map(x => x.split(","));
      const poly = L.polyline(shape).addTo(map).snakeIn();
      
   }

   function showPopup(latlng, label, type, contact) {
      popup
        .setLatLng(latlng)
        .setContent('<p>' +label+ '</p>')
        .openOn(map);
    }

   var scene;
      map.on('tangramloaded', function(e) {
        var tangramLayer = e.tangramLayer;
        scene = tangramLayer.scene;

        tangramLayer.setSelectionEvents({
          click: onMapClick
        });

      });
}