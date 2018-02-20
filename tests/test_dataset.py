#!/usr/bin/env python
# coding: utf-8

""" Test utils.dataset """

from io import StringIO
from utils.dataset import DatasetReader, load_dataset

__author__ = 'fv'


def test_dataset_reader():
    """ Test dataset reader class. """
    with StringIO("69\n42 51\nfoo\nX.") as stream:
        reader = DatasetReader(stream)
        print(reader._lines)
        assert reader.next_int() == 69
        ints = reader.next_ints()
        assert len(ints) == 2
        assert ints[0] == 42
        assert ints[1] == 51
        assert reader.next_line() == 'foo'
        row = reader.next_row()
        assert len(row) == 2
        assert row[0] == 'X'
        assert row[1] == '.'


def test_load_dataset():
    """ Unit test for dataset loading. """
    pass
