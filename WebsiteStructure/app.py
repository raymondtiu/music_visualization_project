import pandas as pd
import datetime as dt
from wtforms import Form, StringField
import requests

from flask import (
    Flask,
    request,
    render_template,
    jsonify)

  
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
engine = create_engine("sqlite:///db/events.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Use the following functions to convert api info to GeoJSON
def to_geojson(results):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for result in results:
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [result.lng,result.lat]
        feature['properties']['name'] = result.consert_name
        feature['properties']['date'] = result.date
        feature['properties']['city'] = result.city
        feature['properties']['popularity'] = result.popularity
        geojson['features'].append(feature)
    return geojson

"""def df_to_geojson(df, properties, lat='lat', lon='lng'):
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
    return geojson """

"""def get_geojson(df):
    df = df
    properties = ['event_name','popularity','date','city']
    lat = 'lat'
    lon = 'lng'
    geojson = df_to_geojson(df,properties,lat=lat,lon=lon)
    return geojson"""

"""def sqlquery_to_df(sqlresults):
    df = pd.DataFrame({'artist_name':[],
                       'event_name':[],
                       'city':[],
                       'date':[],
                       'lat':[],
                       'lng':[],
                       'popularity':[]
    })
    for result in sqlresults:
        df = df.append({
            'artist_name':result.artist_name,
            'event_name':result.consert_name,
            'city':result.city,
            'date':result.date,
            'lat':result.lat,
            'lng':result.lng,
            'popularity':result.popularity
            },ignore_index=True) 
    return df"""

def query_artist(artist):
    artist_events = Base.classes.artist_events
    results = session.query(artist_events.artist_name, artist_events.city, artist_events.consert_name, artist_events.date, artist_events.lat, artist_events.lng, artist_events.popularity).filter(artist_events.artist_name == artist).all()
    geojson = to_geojson(results)
    print("Loading GeoJSON...")
    return jsonify(geojson)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

class ArtistSearch(Form):
    artistName = StringField('Artist Name')

@app.route('/artist', methods=['GET','POST'])
def artist():
    form = ArtistSearch(request.form)
    artist_name = ''
    if request.method == 'POST':
        artist_name = form.artistName.data
        print(artist_name)
    return render_template('artist.html', artist_name=artist_name)

@app.route('/api/<artist>')
def api(artist):
    artist_events = Base.classes.artist_events
    results = session.query(artist_events.artist_name, artist_events.city, artist_events.consert_name, artist_events.date, artist_events.lat, artist_events.lng, artist_events.popularity).filter(artist_events.artist_name == artist).all()
    return jsonify(results)

@app.route('/api_geojson/<artist>')
def api_geojson(artist):
    artist_events = Base.classes.artist_events
    results = session.query(artist_events.artist_name, artist_events.city, artist_events.consert_name, artist_events.date, artist_events.lat, artist_events.lng, artist_events.popularity).filter(artist_events.artist_name == artist).all()
    geojson = to_geojson(results)
    print("Loading GeoJSON...")
    return jsonify(geojson)

if __name__ == '__main__':
    app.run(debug=True)
