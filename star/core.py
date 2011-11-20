# -*- coding: utf-8 -*-

"""
star.core
~~~~~~~~~

The core of the star.
"""

from os import environ

from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class SavedArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False)
    author = db.Column(db.String(80), unique=False)
    published = db.Column(db.DateTime(), unique=False)
    body = db.Column(db.Text(), unique=False)
    link = db.Column(db.String(140), unique=False)

    def __init__(self):
        pass

    def __repr__(self):
        return '<SavedArticle %r>' % self.id


@app.route('/')
def hello_world():
    return str(SavedArticle.query.all())


@app.route('/feed.rss')
def hello_world():
    return str(SavedArticle.query.all())


if __name__ == '__main__':
    app.run()
