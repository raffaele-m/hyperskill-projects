from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func
from db_tables import db, Weather, app
import requests
import datetime
import sys
from weather_api import API_KEY

db.create_all()


# write your code here
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        dicts_cities_info = []
        cities = Weather.query.with_entities(Weather.id, Weather.name).all()
        if not cities:
            return render_template('index.html')
        for city_name in cities:
            params = dict(
                q=city_name.name,
                appid=API_KEY,
                units='metric',
            )
            r = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
            if r.status_code != requests.codes.ok:
                city = Weather.query.filter(func.lower(Weather.name) == func.lower(city_name.name)).first()
                db.session.delete(city)
                db.session.commit()
                flash("The city doesn't exist!")
                return redirect('/')
            r = r.json()
            time = (datetime.datetime.utcnow() + datetime.timedelta(seconds=r['timezone'])).hour
            if (8 <= time <= 11) or (20 <= time <= 23):
                background_class = 'evening-morning'
            elif 12 <= time <= 19:
                background_class = 'day'
            elif 0 <= time <= 7:
                background_class = 'night'
            else:
                background_class = 'evening-morning'
            dict_with_weather_info = {
                'id': city_name.id,
                'city': city_name.name,
                'degrees': int(r['main']['temp']),
                'state': r['weather'][0]['description'],
                'background_class': background_class
            }
            dicts_cities_info.append(dict_with_weather_info)
        return render_template('index.html', list_cities_info=dicts_cities_info)
    elif request.method == "POST":
        city_name = request.form['city_name']
        city = Weather.query.filter(func.lower(Weather.name) == func.lower(city_name)).first()
        if city:
            flash('The city has already been added to the list!')
            return redirect(url_for('index'))
        db.session.add(Weather(name=city_name))
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = Weather.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('index'))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
