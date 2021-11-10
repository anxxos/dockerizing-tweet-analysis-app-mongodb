import os
from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Creamos base de datos en Mongo:
client = MongoClient('db', 27017)
db = client.twitterdb 

@app.route('/')
def twitter():
    
    _items = db.twitterdb.find()
    items = [item for item in _items]

    # Generamos .html:
    return render_template('twitter.html', items = items)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
