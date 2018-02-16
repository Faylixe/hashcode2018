#!/usr/bin/env python
# coding: utf8

""" Toolkit for automatic submission to judge platform. """

from os import listdir
from os.path import join, isfile
from uuid import uuid4 as uuid
from zipfile import ZipFile, ZIP_DEFLATED

from selenium import webdriver

_HOST = 'https://hashcodejudge.withgoogle.com/'
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
        filter(listdir(directory), isfile),
        lambda f: join(directory, f)
    )


def _build_archive_filelist(workspace):
    """ Builds a list of file that aims to be
    archive for a source code submission.

    :param workspace: Target workspace to build source archive for.
    :returns: List of file to archive.
    """
    files = ['requirements.txt', 'run.sh']
    map(_build_filelist(_UTILS), files.append)
    map(_build_filelist(join(_WORKSPACE, workspace)), files.append)
    return files


def _create_source_archive(workspace):
    """ Creates source code archive for the given workspace.

    :param workspace: Workspace to create archive for.
    :returns: The path of the temporary archive file created.
    """
    suffix = uuid()
    path = _ARCHIVE_FILE % (workspace, suffix)
    with ZipFile(path, 'w', ZIP_DEFLATED) as archive:
        map(_create_source_archive(workspace), archive.write)
    return path


class PlatformXPATH(object):
    """ Simple namespace for XPath constant. """

    LOGIN_BUTTON = '/html/body/div/div/div/md-content/md-card/md-card-actions/button'


def _get_driver():
    """
    """
    pass


class JudgeUploader(object):
    """
    """

    def __init__(self):
        """
        """
        self._driver = _get_driver()

    def _authenticate(self):
        """
        """
        self._driver.get(_HOST)
        self._driver.find_element_by_xpath(PlatformXPATH.LOGIN_BUTTON).click()


    def upload(self, dataset, solution, workspace):
        """
        :param dataset:
        :param solution:
        :param workspace:
        """
        pass
