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


@app.route('/states', strict_slashes=False)
def states():
    '''render page'''
    data = storage.all(State).values()
    return render_template('9-states.html', states=data)


@app.route('/states/<id>', strict_slashes=False)
def single_state(id):
    '''render page'''
    states = storage.all(State).values()
    obj = None
    notfound = True
    for state in states:
        if state.id == id:
            obj = state
            notfound = False
            break

    return render_template('9-states.html',
                           state=obj, id=id, notfound=notfound)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
