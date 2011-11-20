# -*- coding: utf-8 -*-

"""
star.core
~~~~~~~~~

The core of the star.
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
