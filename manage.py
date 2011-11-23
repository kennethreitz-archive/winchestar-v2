#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from flaskext.script import Manager

from star import app
from star.core import db, SavedArticle
from star.scraper import star


manager = Manager(app)


@manager.command
def syncdb():
    """Initializes the database."""
    db.create_all()


@manager.command
def cleardb():
    """Drops the database."""
    for article in SavedArticle.query.all():
        db.session.delete(article)

    db.session.commit()

@manager.command
@manager.option('-s', '--start', dest='start', default=datetime.now())
@manager.option('-e', '--end', dest='end', default=None)
def fetch(start=None, end=None):
    for article in star.fetch_articles(start, end):
        try:
            print 'Fetched: {0}'.format(article.title)
            article = SavedArticle.from_article(article)
            article.save()
        except Exception:
            pass

    print 'Done!'


if __name__ == "__main__":
    manager.run()