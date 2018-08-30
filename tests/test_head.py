# --
# Copyright (c) 2008-2018 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import pytest
from nagare.renderers import html_base as html


def test_head1():
    h = html.HeadRenderer()

    assert h.head(h.title('test')).tostring() == '<head><title>test</title></head>'

    with pytest.raises(AttributeError):
        h.foo


def test_head2():
    h = html.HeadRenderer()

    assert h.link.tostring() == '<link>'
    assert h.link.tostring(method='xml') == '<link/>'


def test_url():
    h = html.HeadRenderer()

    assert h.link(href='/abc').tostring() == '<link href="/abc">'
    assert h.link(href='abc').tostring() == '<link href="abc">'

    h = html.HeadRenderer(static_url='/root')

    assert h.link(href='/abc').tostring() == '<link href="/abc">'
    assert h.link(href='abc').tostring() == '<link href="/root/abc">'

    h = html.HeadRenderer()

    assert h.base(href='/abc').tostring() == '<base href="/abc">'
    assert h.base(href='abc').tostring() == '<base href="abc">'

    h = html.HeadRenderer(static_url='/root')

    assert h.base(href='/abc').tostring() == '<base href="/abc">'
    assert h.base(href='abc').tostring() == '<base href="/root/abc">'

    h = html.HeadRenderer()

    assert h.script(src='/abc').tostring() == '<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == '<script src="abc"></script>'

    h = html.HeadRenderer(static_url='/root')

    assert h.script(src='/abc').tostring() == '<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == '<script src="/root/abc"></script>'


def test_cache_buster():
    h = html.HeadRenderer(assets_version='1.2')

    assert h.link(href='/abc').tostring() == '<link href="/abc">'
    assert h.link(href='abc').tostring() == '<link href="abc?ver=1.2">'

    h = html.HeadRenderer(static_url='/root', assets_version='1.2')

    assert h.link(href='/abc').tostring() == '<link href="/abc">'
    assert h.link(href='abc').tostring() == '<link href="/root/abc?ver=1.2">'

    h = html.HeadRenderer(static_url='/root', assets_version='1.2')

    assert h.link(href='/abc?foo=bar').tostring() == '<link href="/abc?foo=bar">'
    assert h.link(href='abc?foo=bar').tostring() == '<link href="/root/abc?foo=bar&amp;ver=1.2">'
    assert h.link(href='/abc?foo=bar&hello=world').tostring() == '<link href="/abc?foo=bar&amp;hello=world">'
    assert h.link(href='abc?foo=bar&hello=world').tostring() == '<link href="/root/abc?foo=bar&amp;hello=world&amp;ver=1.2">'
