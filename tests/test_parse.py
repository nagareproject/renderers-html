# --
# Copyright (c) 2008-2018 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

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
