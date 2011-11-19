#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ
from datetime import datetime

import dateutil.parser
import requests
from lxml.html import html5parser, tostring
from lxml import etree


HOME_URL = 'http://www.winchesterstar.com/'
LOGIN_URL = HOME_URL + 'members/login'
EDITION_URL = HOME_URL + 'pages/choose_edition/date:{0}'

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
        r = self.s.get(url)

        print r
        print r.content
        # from lxml.html import tostring, html5parser
        # t = html5parser.fromstring(r.content)



        # from lxml.cssselect import CSSSelector

        # print dir(t)

        # print t.text
        # print [e.get('href') for e in CSSSelector('a')(t)]

        # print t.xpath('//a/@href')
        # print t.xpath('//a')

        # print t
        # print dir(t)
        # print t.cssselect('a')

        # Convert to epic html.
        # content = tostring(html5parser.fromstring(r.content))
        # t = etree.fromstring(content)
        # t.resolve_base_href()
        # t.make_links_absolute(r.url)
        # for tup in t.iterlinks():
        #     print tup
        # print dir(t)
        # for u in t.xpath('//a'):
            # print u

        # print t.findall('a')
        # print type(t)

        # print dir(p)
        # for url in t.iterfind('a'):
            # print url
        # p.getroot().make_links_absolute()
        # print r
        # print r.history
        # print r.headers
        # print r.content


star = Newspaper()
star.login(USERNAME, PASSWORD)
star.fetch_articles()
# star.fetch_articles('september 3rd')