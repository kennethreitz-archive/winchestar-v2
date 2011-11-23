# -*- coding: utf-8 -*-

"""
star.core
~~~~~~~~~

The core of the star.
"""

from os import environ

from flask import Flask, render_template
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from rfc3339 import rfc3339


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.debug = True

db = SQLAlchemy(app)


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




@app.route('/')
def hello_world():
    s = ''
    # articles = SavedArticle.query.all()
    articles = SavedArticle.query.order_by(desc(SavedArticle.published)).limit(30).all()

    for a in articles:
        s += str(a.title) + '  ' + str(a.link)
        s += '<br />'
        print a


    return s


@app.route('/feed.atom')
def rss_feed():
    articles = SavedArticle.query.order_by(
        desc(SavedArticle.published)
    ).limit(30).all()

    return render_template('feed.atom', articles=articles)


def function():
    pass

if __name__ == '__main__':
    app.run()
