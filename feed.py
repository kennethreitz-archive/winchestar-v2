#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ

import requests

LOGIN_URL = 'http://winchesterstar.com/members/login'
url = 'http://www.winchesterstar.com/articles/view/stephens_city_woman_dies_in_crash_3_still_in_hospital'

USERNAME = environ.get('WINCHESTAR_USER')
PASSWORD = environ.get('WINCHESTAR_PASS')



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



star = Newspaper()
star.login(USERNAME, PASSWORD)

