#!/usr/bin/env python
# coding: utf8

""" Tools function for manipulating google session related cookies. """

from os.path import exists
from pickle import dump, load
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

_HOST = 'https://accounts.google.com'
_PATH = 'signin/v2/identifier'
_PARAMETERS = 'hl=fr&passive=true&continue=https%3A%2F%2Fwww.google.fr%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
_COOKIE_FILE = 'cookies.pkl'
_EXPECTED = 'https://www.google.fr'


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
    if not exists(cookie):
        raise IOError('No cookie file %s found' % cookies_path)
    driver = driver_supplier()
    with open(cookies_path, 'rb') as stream:
        cookies = load(stream)
        for cookie in cookies:
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
        url = '%s/%s?%s' % (_HOST, _PATH, _PARAMETERS)
        self._driver.get(url)
        wait = WebDriverWait(self._driver, 1000)
        wait.until(lambda driver: driver.current_url.startswith(_EXPECTED))


if __name__ == '__main__':
    with CookieSupplier() as supplier:
        supplier.authenticate()
        supplier.save_cookie(_COOKIE_FILE)
