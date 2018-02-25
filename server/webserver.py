from flask import Flask, request, redirect, url_for, render_template, make_response
import keys
import sqlite3

db = sqlite3.connect('potholes.db')
app = Flask(__name__)

def get_potholes():
    global db

    if db is None:
        print("Database is none!")
        return []

    c = db.cursor()
    c.execute("SELECT * FROM holes")
    
    return c.fetchall()

@app.route("/")
def index():
    potholes = get_potholes()
    api_key = keys.map_key
    json='{"type":"FeatureCollection","features":[' \
         + ','.join([ \
           '{"type":"Feature","properties":{' \
         + '"count": %d' % count \
         + '}, "geometry":{"type":"Point",' \
         + '"coordinates":[%f,%f]}' % (lon, lat) \
         + '}' for (_, lat, lon, count) in potholes]) \
       + ']}'
    return render_template('index.html', api_key=api_key, json=json)

if __name__ == "__main__":
    app.run()
