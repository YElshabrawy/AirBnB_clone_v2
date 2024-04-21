#!/usr/bin/pyrhon3
'''module'''

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session'''
    storage.close()


@app.route('/states_list', strict_slashes=False)
def page():
    states = storage.all(State)
    print(states.values())
    return render_template('7-states_list.html', states=states.values())


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)