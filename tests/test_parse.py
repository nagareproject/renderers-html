# --
# Copyright (c) 2008-2025 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import os

import pytest

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from nagare.renderers import xml
from nagare.renderers import html_base as html


def test_parse1():
    h = html.HeadRenderer()

    root = h.fromfile(StringIO('<html><body/></html>'))
    assert isinstance(root, html.Tag)
    assert root.tostring() == b'<html><body></body></html>'

    root = h.fromfile(StringIO('<html><body/></html>'), xml.Tag)
    assert isinstance(root, xml.Tag)
    assert root.tostring() == b'<html><body/></html>'

    root = h.fromstring('<html><body/></html>')
    assert isinstance(root, html.Tag)
    assert root.tostring() == b'<html><body></body></html>'

    root = h.fromstring('<html><body/></html>', xml.Tag)
    assert isinstance(root, xml.Tag)
    assert root.tostring() == b'<html><body/></html>'


def test_parse2():
    h = html.Renderer()

    root = h.fromfile(StringIO('<html><body/></html>'))
    assert isinstance(root, html.Tag)
    assert root.tostring() == b'<html><body></body></html>'

    root = h.fromfile(StringIO('<html><body/></html>'), xml.Tag)
    assert isinstance(root, xml.Tag)
    assert root.tostring() == b'<html><body/></html>'

    root = h.fromstring('<html><body/></html>')
    assert isinstance(root, html.Tag)
    assert root.tostring() == b'<html><body></body></html>'

    root = h.fromstring('<html><body/></html>', xml.Tag)
    assert isinstance(root, xml.Tag)
    assert root.tostring() == b'<html><body/></html>'


def test_parse3():
    """XHTML namespace unit test - HTMLRender - parse_html - bad encoding"""
    h = html.Renderer()
    filename = os.path.join(os.path.dirname(__file__), 'iso-8859.xml')

    with pytest.raises(UnicodeDecodeError):
        h.fromfile(filename, encoding='utf-8')

    h.fromfile(filename, encoding='iso8859-1')


def test_parse4():
    h = html.Renderer()
    root = h.fromstring('<html><head><body></body></head><html>')
    assert root.tostring() == b'<html><head></head><body></body></html>'


def test_parse5():
    h = html.Renderer()
    root = h.fromstring('test')
    assert root.tostring() == b'<html><body><p>test</p></body></html>'


def test_parse6():
    h = html.Renderer()
    root = h.fromstring('<a>text</a>')
    assert type(root) == html.Tag

    x = xml.Renderer()
    root = x.fromstring('<a>text</a>')
    assert type(root) == xml.Tag


def test_parse8():
    h = html.Renderer()
    root = h.fromstring('<a>text</a>', fragment=True)
    assert isinstance(root, tuple)
    assert len(root) == 1
    assert root[0].tostring() == b'<a>text</a>'


def test_parse9():
    h = html.Renderer()
    root = h.fromstring('<a>text</a><b>text</b>', fragment=True)
    assert isinstance(root, tuple)
    assert len(root) == 2
    assert root[0].tostring() == b'<a>text</a>'
    assert root[1].tostring() == b'<b>text</b>'


def test_parse10():
    h = html.Renderer()
    root = h.fromstring('hello<a>text</a><b>text</b>', fragment=True)
    assert isinstance(root, tuple)
    assert len(root) == 3
    assert root[0] == b'hello'
    assert root[1].tostring() == b'<a>text</a>'
    assert root[2].tostring() == b'<b>text</b>'

    root = h.fromstring('hello<a>text</a><b>text</b>', fragment=True, no_leading_text=True)
    assert isinstance(root, tuple)
    assert len(root) == 2
    assert root[0].tostring() == b'<a>text</a>'
    assert root[1].tostring() == b'<b>text</b>'
