# -*- coding: utf-8 -*-

"""
star.core
~~~~~~~~~

The core of the star.
"""

from os import environ
from collections import OrderedDict

import raven
from flask import Flask, render_template, make_response
from flaskext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from sqlalchemy import desc
from rfc3339 import rfc3339

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.debug = True

# Bootstrap raven config from environ.
raven.load(environ['SENTRY_DSN'], app.config)

db = SQLAlchemy(app)
sentry = Sentry(app)


class SavedArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=False)
    author = db.Column(db.String(80), unique=False)
    published = db.Column(db.DateTime(), unique=False)
    body = db.Column(db.Text(), unique=False)
    link = db.Column(db.String(140), unique=True)

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


def list_n_articles(n=None):
    # GRAB THEM ALL!
    articles = OrderedDict()
    _articles =  SavedArticle.query.order_by(desc(SavedArticle.published))

    if n is None:
        _articles = _articles.all()
    else:
        _articles = _articles.limit(n)

    # Big ordered dict of dates.
    for article in _articles:
        if not article.published in articles:
            articles[article.published] = []
        articles[article.published].append(article)

    return articles


@app.route('/')
def list_articles():
    articles = list_n_articles(100)
    return render_template('index.html', articles=articles)


@app.route('/all')
def list_all_articles():
    articles = list_n_articles()
    return render_template('index.html', articles=articles)


@app.route('/article/<article_id>')
def single_article(article_id):

    article = SavedArticle.query.filter_by(id=article_id).first()

    return render_template('article.html', article=article)


@app.route('/feed.atom')
def atom_feed():
    articles = SavedArticle.query.order_by(
        desc(SavedArticle.published)
    ).limit(40).all()

    r = make_response(render_template('feed.atom', articles=articles))
    r.headers['Content-Type'] = 'application/atom+xml'

    return r

if __name__ == '__main__':
    app.run()
