import folium
import os

import requests
from requests import HTTPError

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from copout.auth import login_required
from copout.db import get_db

bp = Blueprint('report', __name__)

@bp.route('/')
def index():  
    db = get_db()
    reports = db.execute('SELECT * FROM post ORDER BY created DESC').fetchall()

    start_coords = (39.381266, -97.922211)
    folium_map = folium.Map(location=start_coords, zoom_start=4)

    for report in reports:
        lat = report['lat']
        lng = report['lng']
        tooltip = report['city_of_inc'] + ', ' + report['state_of_inc']
        #TODO: popup
        folium.Marker([lat, lng], tooltip=tooltip).add_to(folium_map)
    
    return render_template('report/index.html', reports=reports, map=folium_map.get_root().render())


