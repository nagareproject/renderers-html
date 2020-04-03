# --
# Copyright (c) 2008-2020 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import pytest
from nagare.renderers import html_base as html


def test_html1():
    h = html.Renderer()

    assert h.div(h.p('test')).tostring() == b'<div><p>test</p></div>'

    with pytest.raises(AttributeError):
        h.foo


def test_head():
    """ XHTML namespace unit test - HTMLRender - init - test if head exists """
    h = html.Renderer()
    assert hasattr(h, 'head')
    assert isinstance(h.head, html.HeadRenderer)


def test_xml():
    h = html.Renderer()

    assert h.p.tostring() == b'<p></p>'
    assert h.p.tostring(method='xml') == b'<p/>'


def test_url():
    h = html.Renderer()

    assert h.embed(src='/abc').tostring() == b'<embed src="/abc"></embed>'
    assert h.embed(src='abc').tostring() == b'<embed src="abc"></embed>'

    h = html.Renderer(static_url='/root')

    assert h.embed(src='/abc').tostring() == b'<embed src="/abc"></embed>'
    assert h.embed(src='abc').tostring() == b'<embed src="/root/abc"></embed>'

    h = html.Renderer()

    assert h.img(src='/abc', lowsrc='/def').tostring() == b'<img src="/abc" lowsrc="/def">'
    assert h.img(src='abc', lowsrc='def').tostring() == b'<img src="abc" lowsrc="def">'

    h = html.Renderer(static_url='/root')

    assert h.img(src='/abc', lowsrc='/def').tostring() == b'<img src="/abc" lowsrc="/def">'
    assert h.img(src='abc', lowsrc='def').tostring() == b'<img src="/root/abc" lowsrc="/root/def">'

    h = html.Renderer()

    assert h.input(src='/abc').tostring() == b'<input src="/abc">'
    assert h.input(src='abc').tostring() == b'<input src="abc">'

    h = html.Renderer(static_url='/root')

    assert h.input(src='/abc').tostring() == b'<input src="/abc">'
    assert h.input(src='abc').tostring() == b'<input src="/root/abc">'

    h = html.Renderer()

    assert h.head.link(href='/abc').tostring() == b'<link href="/abc">'
    assert h.head.link(href='abc').tostring() == b'<link href="abc">'

    assert h.head.link(rel="stylesheet", href='/abc').get('href') == '/abc'
    assert h.head.link(rel="stylesheet", href='abc').get('href') == 'abc'

    h = html.Renderer(static_url='/root')

    assert h.head.link(href='/abc').tostring() == b'<link href="/abc">'
    assert h.head.link(href='abc').tostring() == b'<link href="abc">'

    assert h.head.link(rel="stylesheet", href='/abc').get('href') == '/abc'
    assert h.head.link(rel="stylesheet", href='abc').get('href') == '/root/abc'

    h = html.Renderer()

    assert h.script(src='/abc').tostring() == b'<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == b'<script src="abc"></script>'

    h = html.Renderer(static_url='/root')

    assert h.script(src='/abc').tostring() == b'<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == b'<script src="/root/abc"></script>'


def test_cache_buster():
    h = html.Renderer(assets_version='1.2')

    assert h.a(href='/abc').tostring() == b'<a href="/abc"></a>'
    assert h.a(href='abc').tostring() == b'<a href="abc"></a>'

    assert h.head.link(rel='stylesheet', href='/abc').get('href') == '/abc'
    assert h.head.link(rel='stylesheet', href='abc').get('href') == 'abc?ver=1.2'

    assert h.head.link(rel='next', href='/abc').get('href') == '/abc'
    assert h.head.link(rel='next', href='abc').get('href') == 'abc'

    assert h.script(src='/abc').tostring() == b'<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == b'<script src="abc?ver=1.2"></script>'

    h = html.Renderer(static_url='/root', assets_version='1.2')

    assert h.a(href='/abc').tostring() == b'<a href="/abc"></a>'
    assert h.a(href='abc').tostring() == b'<a href="abc"></a>'

    assert h.head.link(rel='stylesheet', href='/abc').get('href') == '/abc'
    assert h.head.link(rel='stylesheet', href='abc').get('href') == '/root/abc?ver=1.2'

    assert h.head.link(rel='next', href='/abc').get('href') == '/abc'
    assert h.head.link(rel='next', href='abc').get('href') == 'abc'

    assert h.script(src='/abc').tostring() == b'<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == b'<script src="/root/abc?ver=1.2"></script>'

    h = html.Renderer(static_url='/root', assets_version='1.2')

    assert h.script(src='/abc?foo=bar').tostring() == b'<script src="/abc?foo=bar"></script>'
    assert h.script(src='abc?foo=bar').tostring() == b'<script src="/root/abc?foo=bar&amp;ver=1.2"></script>'
    assert h.script(src='/abc?foo=bar&hello=world').tostring() == b'<script src="/abc?foo=bar&amp;hello=world"></script>'
    assert h.script(src='abc?foo=bar&hello=world').tostring() == b'<script src="/root/abc?foo=bar&amp;hello=world&amp;ver=1.2"></script>'


def test_htmltag_write_xmlstring1():
    h = html.Renderer()
    h << h.table(h.tr(h.td()), h.tr(h.td()))
    assert h.root.tostring() == b'<table><tr><td></td></tr><tr><td></td></tr></table>'


def test_htmltag_write_xmlstring2():
    h = html.Renderer()
    h << h.table(h.tr(h.td().meld_id('test'), h.tr(h.td().meld_id('test'))))
    assert h.root.tostring(pipeline=True) == b'<table><tr><td xmlns:ns0="http://www.plope.com/software/meld3" ns0:id="test"></td><tr><td xmlns:ns0="http://www.plope.com/software/meld3" ns0:id="test"></td></tr></tr></table>'


def test_htmltag_write_xmlstring3():
    h = html.Renderer()
    h << h.table(h.tr(h.td().meld_id('false'), h.tr(h.td().meld_id('false'))))
    assert h.root.tostring(pipeline=False) == b'<table><tr><td xmlns:ns0="http://www.plope.com/software/meld3"></td><tr><td xmlns:ns0="http://www.plope.com/software/meld3"></td></tr></tr></table>'
