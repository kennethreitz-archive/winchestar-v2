#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ
from datetime import datetime

import dateutil.parser
import requests
from requests import async
from BeautifulSoup import BeautifulSoup


HOME_URL = 'http://winchesterstar.com'
LOGIN_URL = HOME_URL + '/members/login'
EDITION_URL = HOME_URL + '/pages/choose_edition/date:{0}'

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
        """Returns a new article instance, built from the given HTML string."""

        article = Article()

        this_year = str(datetime.now().year)

        soup = BeautifulSoup(content)

        art = max(soup.findAll('td'), key=len)
        article.title = art.find('h2').text
        article.published = (
            art.findNext('div').text.split('By')[0].
                split(this_year)[0] + this_year)

        # Datetime it.
        article.published = dateutil.parser.parse(unicode(article.published))

        _content = (
            max(str(art).split('<hr />'), key=len).lstrip().
                split('</style>')[-1].lstrip())
        article.body = BeautifulSoup(_content).prettify()

        try:
            article.subtitle = art.find('h3').text
        except AttributeError:
            pass

        try:
            article.author = art.find('div').find('div').find('em').text.replace('By ', '')
        except AttributeError:
            pass

        # Skip Image-only posts.
        if len(article.body) < 1000:
            return None

        return article


class Newspaper(object):
    """The Winchester Star interface."""

    def __init__(self):
        super(Newspaper, self).__init__()
        self.s = requests.session()

    def login(self, username, password):
        """Logs into the Newspaper website."""

        package = {
            '_method': 'POST',
            'data[Member][email]': username,
            'data[Member][password]': password,
        }

        self.s.post(LOGIN_URL, data=package)


    def fetch_articles(self, date=None):
        """Returns a list of articles for the given date.

        If no date is provided, today is assumed.
        """

        if date is None:
            date = datetime.today()

        if isinstance(date, basestring):
            date = dateutil.parser.parse(unicode(date))

        assert isinstance(date, datetime)

        timestamp = date.strftime('%Y-%m-%d')
        url = EDITION_URL.format(timestamp)

        # The page for the current day.
        r = self.s.get(url)


        # Parse it for links.
        soup = BeautifulSoup(r.content)

        # List of requests to make.
        reqs = []

        for a in soup.findAll('a'):
            link = a.get('href')

            if link and ('homepage_links' in link):
                url = HOME_URL + link
                req = async.get(url, cookies=self.s.cookies)
                reqs.append(req)

        # Get all the articles.
        # reqs = reqs[:4]  # testing.
        reqs = async.map(reqs, size=5)

        articles = []

        for r in reqs:
            article = Article.new_from_html(r.content)

            if article:
                article.link = r.url
                articles.append(article)

        return articles


star = Newspaper()
star.login(USERNAME, PASSWORD)
for article in star.fetch_articles():
    print article.title
    print article.author
    print article.published

    print len(article.body)
    print