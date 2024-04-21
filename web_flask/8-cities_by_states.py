#!/usr/bin/python3
'''module'''

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session'''
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def page():
    '''render page'''
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states.values())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
