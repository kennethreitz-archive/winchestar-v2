# -*- coding: utf-8 -*-

"""
star.scraper
~~~~~~~~~~~~

The Winchester Star scraper.
"""

from os import environ
from datetime import datetime

import requests
from BeautifulSoup import BeautifulSoup

from .utils import date, date_range


# Configuration
HOME_URL = 'http://www.winchesterstar.com'
LOGIN_URL = HOME_URL + '/members/login'
EDITION_URL = HOME_URL + '/articles/setEdition/{0}'

# Credentials.
USERNAME = environ.get('WINCHESTAR_USER')
PASSWORD = environ.get('WINCHESTAR_PASS')
LOGIN_REQUIRED = True


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

        from pyquery import PyQuery as pq

        d = pq(content)


        from html2text import html2text


        article.title = d('h1.title').text()
        article.published = d('p.posted').text().replace('Posted: ', '')
        article.published = date(unicode(article.published))

        story = html2text(str(d('div.story')))
        story = story.replace('/files/uploads', HOME_URL + '/files/uploads')
        article.body = story

        article.author = d('p.byline > span').text()

        # Skip Image-only posts.
        # if len(article.body) < 1000:
        #     return None

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

        r = self.s.post(LOGIN_URL, data=package)

    def get_url(self, path, relative=False):
        if relative:
            url = HOME_URL + path
        else:
            url = path

        r = self.s.get(url)
        # r.encoding = None
        return r


    def article_from_url(self, path):
        r = self.get_url(path)
        content = r.text
        content = content.replace(u"\u2018", "'").replace(u"\u2019", "'")
        content = content.replace(u'\xa0', '')
        content = content.replace(u'\u2014', '--')

        article = Article.new_from_html(content)

        article.link = r.url
        return article

    def urls_from_edition_url(self, url):

        # Grab the page for the day.
        r = self.get_url(url)

        # Parse it for links.
        soup = BeautifulSoup(r.content)

        links = set()

        for a in soup.findAll('a'):
            link = a.get('href')

            if link and ('article' in link):
                url = HOME_URL + link

            if 'setEdition' not in url:
                links.add(url)

        return links



                # req = requests.get(url, cookies=self.s.cookies)
                # reqs.append(req)


    def fetch_articles(self, start_date=None, end_date=None):
        """Returns a list of articles for the given date.

        If no date is provided, today is assumed.
        """

        # Assume today.
        if start_date is None:
            start_date = datetime.today()

        if end_date is None:
            end_date = start_date

        # For every date...
        for date in date_range(start_date, end_date):
            print date

            timestamp = date.strftime('%Y-%m-%d')
            url = EDITION_URL.format(timestamp)

            urls = self.urls_from_edition_url(url)

            for url in urls:
                print url
                yield self.article_from_url(url)




star = Newspaper()
star.login(USERNAME, PASSWORD)
