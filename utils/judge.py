#!/usr/bin/env python
# coding: utf8

""" Toolkit for automatic submission to judge platform. """

from os import listdir
from os.path import join, isdir, isfile
from pickle import load
from requests import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4 as uuid
from zipfile import ZipFile, ZIP_DEFLATED

from utils.configuration import configuration

__author__ = 'fv'

_ARCHIVE_FILE = '/tmp/source-%s.zip'


def _build_filelist(directory):
    """ Builds and returns a list of file that the given
    directory contains. Path are directory relative.

    :param directory:  Directory to build file list from.
    :returns: List of file found in the given directory, with full path.
    """
    return filter(isfile, map(
        lambda f: join(directory, f),
        listdir(directory))
    )


def _build_archive_filelist():
    """ Builds a list of file that aims to be
    archive for a source code submission.

    :returns: List of file to archive.
    """
    files = ['requirements.txt', 'init.sh']
    for package in ('tests', 'utils', 'workspace'):
        for module in _build_filelist(package):
            files.append(module)
    for workspace in filter(isdir, listdir('workspace')):
        for module in _build_filelist(join('workspace', workspace)):
            files.append(module)
    return files


def _create_source_archive():
    """ Creates source code archive for the given workspace.

    :returns: The path of the temporary archive file created.
    """
    suffix = uuid()
    path = _ARCHIVE_FILE % suffix
    with ZipFile(path, 'w', ZIP_DEFLATED) as archive:
        for source in _build_archive_filelist():
            archive.write(source)
    return path


def _create_driver():
    """ Selenium webdriver factory function.

    :returns: A webdriver instance according to the internal configuration.
    """
    if configuration.SELENIUM_DRIVER == 'phantomjs':
        # TODO : Switch to phantomjs
        return webdriver.Firefox()
    return webdriver.Firefox()


class JudgeSite(object):
    """ Class for uploading submission to the judge platform. """

    MYACCOUNT = 'https://myaccount.google.com'
    LOGIN = 'https://accounts.google.com/signin/v2/sl/pwd'
    SITE = 'https://hashcodejudge.withgoogle.com'
    SUBMISSION = SITE + '/#/rounds/%s/submissions/'
    SOURCE_XPATH = '//*[@id="dialogContent_6"]/div/div/judge-upload/div/md-input-container/div[2]/div/button'
    SUBMISSION_XPATH = '/html/body/div/div/div/md-content/div[1]/md-card/md-card-header/div/button'

    def __init__(self, round):
        """ Default constructor.

        :param round: Target contest round.
        """
        self._url = JudgeSite.SUBMISSION % round
        self._driver = _create_driver()

    def __enter__(self):
        """ Context manager initializer. """
        return self

    def __exit__(self, type, value, traceback):
        """ Context manager exit method. """
        self._driver.close()

    def _get(self, locator):
        """ Suger method for element access using driver wait. """
        wait = WebDriverWait(self._driver, 10)
        condition = EC.visibility_of_element_located(locator)
        return wait.until(condition)
    
    def _click(self, locator):
        """ Suger method for element clicking using driver wait. """
        wait = WebDriverWait(self._driver, 10)
        condition = EC.element_to_be_clickable(locator)
        wait.until(condition).click()

    def login(self, username, password):
        """ Performs login into Google Services.

        :param username: Google account username (email).
        :param password: Google account password.
        """
        self._driver.get(JudgeSite.LOGIN)
        username_holder = self._get((By.ID, 'identifierId'))
        username_holder.clear()
        username_holder.send_keys(username)
        self._click((By.ID, 'identifierNext'))
        password_holder = self._get((By.NAME, 'password'))
        password_holder.clear()
        password_holder.send_keys(password)
        self._click((By.ID, 'passwordNext'))
        wait = WebDriverWait(self._driver, 10)
        wait.until(lambda d: d.current_url.startswith(JudgeSite.MYACCOUNT))

    def upload(self, dataset, solution):
        """
        :param dataset:
        :param solution:
        :param workspace:
        """
        # Navigate to submission panel.
        self._driver.get(self._url)
        self._get(By.XPATH, JudgeSite.SUBMISSION_XPATH).click()
        # Source code upload.
        archive = _create_source_archive()
        self._get(By.ID, 'input_1').send_keys(archive)
        # Solution upload.
        self._get(By.ID, 'input_%s' % target).send_keys(solution) # TODO : Check for path.
        # Submit.
