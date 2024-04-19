#!/usr/bin/python3
''' Module that starts a Flask web application '''
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    ''' Function that generates a page with a message '''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    ''' Function that generates a page with a message '''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def html(text):
    '''Function to return text'''
    return f'C {escape(text.replace("_", " "))}'


@app.route('/python/', defaults={"text": "is cool"}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def res(text):
    '''func'''
    return f'Python {escape(text.replace("_", " "))}'


@app.route('/number/<int:n>', strict_slashes=False)
def page(n):
    '''func'''
    return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def page2(n):
    '''func'''
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def page3(n):
    '''func'''
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
