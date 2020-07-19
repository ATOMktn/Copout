import functools
import datetime
import requests
import os

from requests.exceptions import HTTPError

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from copout.db import get_db

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not confirm:
            error = 'Password confirmation required.'
        elif password != confirm:
            error = 'Passwords must match.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:    
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/profile', methods=('POST', 'GET'))
@login_required
def profile():
    if request.method == 'POST':
        title = request.form['title']
        date_of_inc = request.form['date-of-inc']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        org = request.form['org']
        persons = request.form['persons']
        persons_id = request.form['persons-id']
        summary = request.form['summary']
        now = datetime.datetime.now()
        error = None
        date_error = 'Must provide valid date of incident (yyyy-mm-dd)'
        location_error = "Must provide valid U.S address"
        db = get_db()

        if not title:
            error = 'Must provide title'

        if not date_of_inc:
            error = date_error
        else:
            date_dict = {}
            date_list = date_of_inc.split('-')
            for i in range(0, len(date_list)):
                value = int(date_list[i])
                if i == 0:
                    date_dict['year'] = value
                elif i == 1:
                    date_dict['month'] = value
                else:
                    date_dict['day'] = value
            try:
                valid_date = datetime.date(date_dict['year'], date_dict['month'], date_dict['day'])
            except ValueError:
                error = 'date_error'
    
        if not city or not state or not address:
            error = location_error
        else:
            payload = { 'address': f'{address} {city} {state}'.replace(' ', '%20'), 'key': os.environ['SECRET_GEO'] }

            try:
                resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload)
                response = resp.json()
      
                if response['status'] == 'OK':
                    street = response['results'][0]['formatted_address'].split(',')[0]
                    coords = response['results'][0]['geometry']['location']
                    lat = coords['lat']
                    lng = coords['lng']
                    city_name = None
                    valid_state = None
                    country = None

                    for component in response['results'][0]['address_components']:
                        comp_type = component['types'][0]
                        name = component['short_name']

                        if comp_type == 'administrative_area_level_1':
                            valid_state = name
                        
                        if comp_type == 'locality':
                            city_name = name

                        if comp_type == 'country':
                            country = name

                    if country != 'US':
                        error = location_error

                else:
                    error = location_error

            except HTTPError:
                error = "Address could not be verified. Please try again"
                 
        if not org:
            error = 'Please provide name of Organization involved'
        if not persons:
            error = 'Please provide name of the persons involved i.e name of officer'
        if not persons_id:
            error = "Please provide some identifier for persons involved i.e badge number"
        if not summary or len(summary) < 50:
            error = 'Please provide a breif summary of the incident'

        if error is None:
            db.execute(
                'INSERT INTO post (author_id, created, title, date_of_inc, address, city_of_inc, state_of_inc, lat, lng, persons, persons_id, org, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                (g.user['id'], now, title, valid_date, street, city_name, valid_state, lat, lng, persons, persons_id, org, summary)
                )
            db.commit()
            return redirect(url_for('index'))
    
        flash(error)

    return render_template('auth/profile.html')