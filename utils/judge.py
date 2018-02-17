#!/usr/bin/env python
# coding: utf8

""" Toolkit for automatic submission to judge platform. """

from os import listdir
from os.path import join, isfile
from uuid import uuid4 as uuid
from zipfile import ZipFile, ZIP_DEFLATED

from selenium import webdriver

from utils.cookie import get_authenticated_driver

_HOST = 'https://hashcodejudge.withgoogle.com'
_PATH = '#/rounds/%s/submissions/
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


class JudgeUploader(object):
    """ """

    def __init__(self, round):
        """
        :param round:
        """
        self._url = '%s/%s' % (_HOST, _PATH % round)
        self._driver = None

    def __enter__(self):
        """ Context manager initializer. """
        self._driver = get_authenticated_driver()
        self._driver.get(self._url)
        return self

    def __exit__(self, type, value, traceback):
       """ Context manager exit method. """
       self._driver.close()

    def open_submission_panel(self):
        """ """
        buttons = self._driver.find_elements_by_tagname('button')
        filtered = filter(buttons, lambda b: b.text == 'Create a new submission')
        if len(filtered) == 0:
            raise IOError('No submission button found')
        filtered[0].click()


def upload(round, dataset, solution, workspace):
    """
    :param round:
    :param dataset:
    :param solution:
    :param workspace:
    """
    archive = _create_source_archive(workspace)
    with JudgeUploader(round) as uploader:
        uploader.open_submission_panel()        
        # TODO : Set source archive upload.
        # TODO : Locate dataset upload form.
        # TODO : Set solution upload.
        # TODO : Upload submission.
