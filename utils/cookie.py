#!/usr/bin/env python
# coding: utf8

""" Tools function for manipulating google session related cookies. """

from os.path import exists
from pickle import dump, load
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

_MYACCOUNT_DOMAIN = 'myaccount.google.com'
_MYACCOUNT_URL = 'https://' + _MYACCOUNT_DOMAIN
_GOOGLE_DOMAIN = 'google.com'
_GOOGLE_URL = 'https://' + _GOOGLE_DOMAIN
_LOGIN_URL = 'https://accounts.google.fr/signin/v2/identifier'
_COOKIE_FILE = 'cookies.pkl'


def get_authenticated_driver(
    driver_supplier=webdriver.Firefox,
    cookies_path=_COOKIE_FILE):
    """ Function that creates a webdriver instance
    authenticated in google services using provided
    cookie file.

    :param driver_supplier: Function that creates a webdriver instance.
    :param cookies_path: Path of the cookie file to load.
    :returns: Built driver instance.
    """
    if not exists(cookies_path):
        raise IOError('No cookie file %s found' % cookies_path)
    driver = driver_supplier()
    with open(cookies_path, 'rb') as stream:
        cookies = load(stream)
        driver.get(_MYACCOUNT_URL)
        for cookie in filter(lambda c: c['domain'] == _MYACCOUNT_DOMAIN, cookies):
            driver.add_cookie(cookie)
        driver.get(_GOOGLE_URL)
        for cookie in filter(lambda c: c['domain'] == _GOOGLE_DOMAIN, cookies):
            driver.add_cookie(cookie)
    return driver


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
        supplier.save_cookie(_COOKIE_FILE)
