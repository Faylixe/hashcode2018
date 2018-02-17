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

def _create_session(cookies_file=COOKIE_FILE):
    """
    :param cookies_file:
    :returns:
    """
    session = Session()
    with open(cookies_file, 'rb') as stream:
        cookies = load(stream)
        for cookie in cookies:
            session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie['domain'],
                path=cookie['path']
            )

def upload(round, dataset, solution, workspace):
    """
    :param round:
    :param dataset:
    :param solution:
    :param workspace:
    """
    archive = _create_source_archive(workspace)
    session = _create_session()
    #session.post()
