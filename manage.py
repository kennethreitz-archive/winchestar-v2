#!/usr/bin/env python
# -*- coding: utf-8 -*-

from star import app
from star.core import db
from flaskext.script import Manager, Command


manager = Manager(app)

@manager.command
def syncdb():
    db.create_all()

@manager.command
def hello():
    """Hello World!"""
    print r'\o/'


if __name__ == "__main__":
    manager.run()