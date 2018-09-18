var artistName = 'PitBull';

var artist_apilink = 'http://127.0.0.1:5000/api_geojson/' + 'PitBull';

d3.json(artist_apilink, function(data) {
    console.log(data)
});

