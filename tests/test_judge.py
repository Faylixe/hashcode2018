#!/usr/bin/env python
# coding: utf8

""" Tests utils.judge """

from os import remove
from os.path import exists
from zipfile import ZipFile

from utils.judge import _build_filelist
from utils.judge import _build_archive_filelist
from utils.judge import _create_source_archive

__author__ = 'fv'

tests = [
    'tests/conftest.py',
    'tests/test_configuration.py',
    'tests/test_dataset.py',
    'tests/test_eval_solution.py',
    'tests/test_judge.py',
    'tests/test_slack.py'
]

utils = [
    'utils/configuration.py',
    'utils/dataset.py',
    'utils/eval_solution.py',
    'utils/judge.py',
    'utils/score.py',
    'utils/slack.py',
    'utils/template.py'
]


def test_build_filelist():
    """ Test build filelist function. """
    files = list(_build_filelist('tests'))
    for f in tests:
        assert f in files


def _verify_files(files):
    """ Verify that all required files are presents in the given collection. """
    assert 'init.sh' in files
    assert 'requirements.txt' in files
    assert 'workspace/__init__.py' in files
    for f in tests:
        assert f in files
    for f in utils:
        assert f in files


def test_build_archive_filelist():
    """ Test archive file list building function. """
    files = _build_archive_filelist()
    _verify_files(files)


def test_create_source_archive():
    """ Test archive creation. """
    archive = _create_source_archive()
    assert exists(archive)
    with ZipFile(archive) as stream:
        names = stream.namelist()
        _verify_files(names)
    remove(archive)
