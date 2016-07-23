# -*- coding: utf-8 -*-

"""
star.core
~~~~~~~~~

The core of the star.
"""

from os import environ
from collections import OrderedDict

from flask import Flask, render_template, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from sqlalchemy import desc
from rfc3339 import rfc3339
from mistune import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.debug = True

db = SQLAlchemy(app)
sentry = Sentry(app, dsn=environ['SENTRY_DSN'])


class SavedArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(800), unique=False)
    author = db.Column(db.String(140), unique=False)
    published = db.Column(db.DateTime(), unique=False)
    body = db.Column(db.Text(), unique=False)
    link = db.Column(db.String(800), unique=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<SavedArticle %r>' % self.id

    @staticmethod
    def from_article(article):

        a = SavedArticle()

        a.title = article.title
        a.author = article.author
        a.published = article.published
        a.body = article.body
        a.link = article.link

        return a

    def save(self):
        if not list(SavedArticle.query.filter_by(link=self.link)):
            db.session.add(self)
            db.session.commit()

    @property
    def rfc_published(self):
        return rfc3339(self.published)



@app.route('/feed.atom')
def atom_feed():

    # Default length, over-ridable, is 40.
    # Let an exception occur if invalid data passed.
    length = int(request.args.get('length', 40))

    articles = SavedArticle.query.order_by(
        desc(SavedArticle.published),
        desc(SavedArticle.id)
    ).limit(length).all()

    for i, article in enumerate(articles):
        article.body = markdown(article.body)

    r = make_response(render_template('feed.atom', articles=articles))
    r.headers['Content-Type'] = 'application/atom+xml'

    return r

if __name__ == '__main__':
    app.run()
