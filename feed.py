#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ

import requests


LOGIN_URL = 'http://winchesterstar.com/members/login'

USERNAME = environ.get('WINCHESTAR_USER')
PASSWORD = environ.get('WINCHESTAR_PASS')


class Article(object):
    """A newspaper article."""

    def __init__(self):
        super(Article, self).__init__()

        self.title = None
        self.author = None
        self.published = None
        self.body = None
        self.link = None

    def __repr__(self):
        return '<article at 0x%x>' % (id(self))

    @staticmethod
    def new_from_html(content):
        article = Article()

        return article


class Newspaper(object):
    """The Winchester Star interface."""

    def __init__(self):
        super(Newspaper, self).__init__()
        self.s = requests.session()

    def login(self, username, password):
        """Logs into the site."""

        package = {
            '_method': 'POST',
            'data[Member][email]': username,
            'data[Member][password]': password,
        }

        self.s.post(LOGIN_URL, data=package)

    def fetch_articles(date=None):
        """Returns a list of articles for the given date.

        If no date is provided, today is assumed.
        """
        pass


star = Newspaper()
star.login(USERNAME, PASSWORD)

