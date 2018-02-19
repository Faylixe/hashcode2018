#!/usr/bin/env python
# coding: utf8

""" Toolkit for automatic submission to judge platform. """

from os import listdir
from os.path import join, isfile
from pickle import load
from requests import Session
from uuid import uuid4 as uuid
from zipfile import ZipFile, ZIP_DEFLATED

from cookie import COOKIE_FILE

_ARCHIVE_FILE = '/tmp/source-%s-%s.zip'
_ROOT_FILES = ['requirements.txt', 'run.sh']
_UTILS = 'utils'
_WORKSPACE = 'workspace'


def _build_filelist(directory):
    """ Builds and returns a list of file that the given
    directory contains. Path are directory relative.

    :param directory:  Directory to build file list from.
    :returns: List of file found in the given directory, with full path.
    """
    return map(
        lambda f: join(directory, f),
        filter(isfile, listdir(directory))
    )


def _build_archive_filelist(workspace):
    """ Builds a list of file that aims to be
    archive for a source code submission.

    :param workspace: Target workspace to build source archive for.
    :returns: List of file to archive.
    """
    files = ['requirements.txt', 'run.sh']
    map(files.append, _build_filelist(_UTILS))
    map(files.append, _build_filelist(join(_WORKSPACE, workspace)))
    return files


def _create_source_archive(workspace):
    """ Creates source code archive for the given workspace.

    :param workspace: Workspace to create archive for.
    :returns: The path of the temporary archive file created.
    """
    suffix = uuid()
    path = _ARCHIVE_FILE % (workspace, suffix)
    with ZipFile(path, 'w', ZIP_DEFLATED) as archive:
        map(archive.write, _build_archive_filelist(workspace))
    return path


class JudgeSite(object):
    """ """

    MYACCOUNT = 'https://myaccount.google.com'
    LOGIN = 'https://accounts.google.com/signin/v2/sl/pwd'
    SITE = 'https://hashcodejudge.withgoogle.com'
    SUBMISSION = SITE + '/#/rounds/%s/submissions/'
    NEXT_XPATH = '/html/body/div[1]/div[1]/div[2]/div[2]/%s/div[2]/div/div[2]/div[1]/div/content/span'
    SOURCE_XPATH = '//*[@id="dialogContent_6"]/div/div/judge-upload/div/md-input-container/div[2]/div/button'
    SUBMISSION_XPATH = '/html/body/div/div/div/md-content/div[1]/md-card/md-card-header/div/button'

    def __init__(self, round):
        """ Default constructor.

        :param round: Target contest round.
        """
        self._url = SUBMISSION % round
        self._driver = None

    def _get(self, by, value):
        """ Suger method for element access using driver wait.

        :param by: Selenium by to build locator.
        :param value: Value of the expected By.
        :returns: Located element if any.
        """
        wait = WebDriverWait(self._driver, 1000)
        locator = (by, id)
        condition = EC.presence_of_element_located(locator)
        return wait.until(condition)

    def login(self, username, password):
        """ Performs login into Google Services.

        :param username: Google account username (email).
        :param password: Google account password.
        """
        self._driver.get(_LOGIN_URL)
        username_holder = self._get(By.ID, 'identifierId')
        username_holder.clear()
        username_holder.send_keys(username)
        self._get(By.XPATH, NEXT_XPATH % 'form').click()
        password_holder = self._get(By.NAME, 'password')
        password_holder.clear()
        password_holder.send_keys(password)
        self._get(By.XPATH, NEXT_XPATH % 'div').click()
        wait = WebDriverWait(self._driver, 1000)
        wait.until(lambda d: d.current_url.startswith(_MYACCOUNT_URL))

    def upload(self, dataset, solution, workspace):
        """
        :param dataset:
        :param solution:
        :param workspace:
        """
        # Navigate to submission panel.
        self._driver.get(self._url)
        self._get(By.XPATH, SUBMISSION_XPATH).click()
        # Source code upload.
        archive = _create_source_archive(workspace)
        self._get(By.ID, 'input_1').send_keys(archive)
        # Solution upload.
        self._get(By.ID, 'input_%s' % target).send_keys(solution) # TODO : Check for path.
        # Submit.
