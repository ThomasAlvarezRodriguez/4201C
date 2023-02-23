from flask import Flask, render_template
import requests
import json
import random as rd
app = Flask(__name__)
@app.route('/')
def get_ssd():
    
    with open ('SSD.json','r',encoding="utf8") as file:
        SSD_json=json.loads(file.read())
    ssd_index=rd.randint(0,len(SSD_json))
    SSD = {
        'name': SSD_json[ssd_index]['name'],
        'asin': SSD_json[ssd_index]['asin'],
        'keyword': SSD_json[ssd_index]['keyword'],
        'price': SSD_json[ssd_index]['price'],
        'stars': SSD_json[ssd_index]['stars'],
        'rating_count': SSD_json[ssd_index]['rating_count'],
        'url': SSD_json[ssd_index]['url'],
        'capacity':SSD_json[ssd_index]['capacity'],
        'harmonized_capacity':SSD_json[ssd_index]['harmonized_capacity'],
    }
    return render_template('index.html', SSD=SSD)
  