from pprint import pprint
import requests
import pandas as pd

song_kick_apikey = 'xk56NDs8PXLU1467'

def GetartistID(artist):
    artist_name = artist
    artist_url = f'https://api.songkick.com/api/3.0/search/artists.json?apikey={song_kick_apikey}&query={artist_name}'
    response = requests.get(artist_url)
    data = response.json()
    artist_id = data['resultsPage']['results']['artist'][0]['id']
    return artist_id
def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson
# for loop to request 20 pages, since there's 50 max per page, we are limiting to 1,000 records max. 
def song_kick_scrape(artist):
    artist_id = GetartistID(artist)
    event_url = f'https://api.songkick.com/api/3.0/artists/{artist_id}/gigography.json?'
    event_query_param = {
    'apikey':song_kick_apikey,
    'order':'desc'
    }
    artist_data = []
    for i in range(1,20):
        event_query_param['page'] = i
        response = requests.get(event_url, params=event_query_param)
        try:
            events = response.json()['resultsPage']['results']['event']
            for event in events:
                data_dict = {}
                data_dict['Name'] = event['displayName']
                data_dict['Popularity'] = event['popularity']
                data_dict['Date'] = event['start']['date']
                data_dict['City'] = event['location']['city']
                data_dict['Lat'] = event['location']['lat']
                data_dict['Lng'] = event['location']['lng']
                artist_data.append(data_dict)
        except KeyError:
            next
    return (artist_data)

def get_geojson(artist):
    artist_data = song_kick_scrape(artist)
    df = pd.DataFrame(artist_data)
    properties = ['Name','Popularity','Date','City']
    lat = 'Lat'
    lon = 'Lng'
    geojson = df_to_geojson(df,properties,lat=lat,lon=lon)
    return geojson