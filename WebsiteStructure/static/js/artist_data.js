var artistName = 'PitBull';

var artist_apilink = '/api_geojson/' + 'PitBull';

d3.json(artist_apilink, function(data) {
    console.log(data)
});

