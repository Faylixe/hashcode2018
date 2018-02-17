#!/usr/bin/env python
# coding: utf8

""" Tools function for manipulating google session related cookies. """

from os.path import exists
from pickle import dump, load
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

_MYACCOUNT_URL = 'https://myaccount.google.com'
_LOGIN_URL = 'https://accounts.google.com/signin/v2/sl/pwd?hl=fr&passive=true&continue=https%3A%2F%2Fmyaccount.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin'

COOKIE_FILE = 'cookies.pkl'


class CookieSupplier(object):
    """ Simple class for managing cookie retrieval. """

    def __enter__(self):
        """ Context manager initializer. """
        self._driver = webdriver.Firefox()
        return self

    def __exit__(self, type, value, traceback):
       """ Context manager exit method. """
       self._driver.close()

    def save_cookie(self, path):
        """ Save internal driver cookies to file. """
        cookies = self._driver.get_cookies()
        with open(path, 'wb') as stream:
            dump(cookies, stream)

    def authenticate(self):
        """ Starts authentification and wait until user is logged. """
        self._driver.get(_LOGIN_URL)
        wait = WebDriverWait(self._driver, 1000)
        wait.until(lambda driver: driver.current_url.startswith(_MYACCOUNT_URL))


if __name__ == '__main__':
    with CookieSupplier() as supplier:
        supplier.authenticate()
        supplier.save_cookie(COOKIE_FILE)
