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


def test_html1():
    h = html.Renderer()

    assert h.div(h.p('test')).tostring() == '<div><p>test</p></div>'

    with pytest.raises(AttributeError):
        h.foo


def test_head2():
    h = html.Renderer()

    assert h.p.tostring() == '<p></p>'
    assert h.p.tostring(method='xml') == '<p/>'


def test_url():
    h = html.Renderer()

    assert h.a(href='/abc').tostring() == '<a href="/abc"></a>'
    assert h.a(href='abc').tostring() == '<a href="abc"></a>'

    h = html.Renderer(static_url='/root')

    assert h.a(href='/abc').tostring() == '<a href="/abc"></a>'
    assert h.a(href='abc').tostring() == '<a href="/root/abc"></a>'

    h = html.Renderer()

    assert h.area(href='/abc').tostring() == '<area href="/abc">'
    assert h.area(href='abc').tostring() == '<area href="abc">'

    h = html.Renderer(static_url='/root')

    assert h.area(href='/abc').tostring() == '<area href="/abc">'
    assert h.area(href='abc').tostring() == '<area href="/root/abc">'

    h = html.Renderer()

    assert h.embed(src='/abc').tostring() == '<embed src="/abc"></embed>'
    assert h.embed(src='abc').tostring() == '<embed src="abc"></embed>'

    h = html.Renderer(static_url='/root')

    assert h.embed(src='/abc').tostring() == '<embed src="/abc"></embed>'
    assert h.embed(src='abc').tostring() == '<embed src="/root/abc"></embed>'

    h = html.Renderer()

    assert h.iframe(src='/abc').tostring() == '<iframe src="/abc"></iframe>'
    assert h.iframe(src='abc').tostring() == '<iframe src="abc"></iframe>'

    h = html.Renderer(static_url='/root')

    assert h.iframe(src='/abc').tostring() == '<iframe src="/abc"></iframe>'
    assert h.iframe(src='abc').tostring() == '<iframe src="/root/abc"></iframe>'

    h = html.Renderer()

    assert h.img(src='/abc').tostring() == '<img src="/abc">'
    assert h.img(src='abc').tostring() == '<img src="abc">'

    h = html.Renderer(static_url='/root')

    assert h.img(src='/abc').tostring() == '<img src="/abc">'
    assert h.img(src='abc').tostring() == '<img src="/root/abc">'

    h = html.Renderer()

    assert h.img(lowsrc='/abc').tostring() == '<img lowsrc="/abc">'
    assert h.img(lowsrc='abc').tostring() == '<img lowsrc="abc">'

    h = html.Renderer(static_url='/root')

    assert h.img(lowsrc='/abc').tostring() == '<img lowsrc="/abc">'
    assert h.img(lowsrc='abc').tostring() == '<img lowsrc="/root/abc">'

    h = html.Renderer()

    assert h.input(src='/abc').tostring() == '<input src="/abc">'
    assert h.input(src='abc').tostring() == '<input src="abc">'

    h = html.Renderer(static_url='/root')

    assert h.input(src='/abc').tostring() == '<input src="/abc">'
    assert h.input(src='abc').tostring() == '<input src="/root/abc">'

    h = html.Renderer()

    assert h.script(src='/abc').tostring() == '<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == '<script src="abc"></script>'

    h = html.Renderer(static_url='/root')

    assert h.script(src='/abc').tostring() == '<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == '<script src="/root/abc"></script>'


def test_cache_buster():
    h = html.Renderer(assets_version='1.2')

    assert h.a(href='/abc').tostring() == '<a href="/abc"></a>'
    assert h.a(href='abc').tostring() == '<a href="abc?ver=1.2"></a>'

    h = html.Renderer(static_url='/root', assets_version='1.2')

    assert h.a(href='/abc').tostring() == '<a href="/abc"></a>'
    assert h.a(href='abc').tostring() == '<a href="/root/abc?ver=1.2"></a>'

    h = html.Renderer(static_url='/root', assets_version='1.2')

    assert h.a(href='/abc?foo=bar').tostring() == '<a href="/abc?foo=bar"></a>'
    assert h.a(href='abc?foo=bar').tostring() == '<a href="/root/abc?foo=bar&amp;ver=1.2"></a>'
    assert h.a(href='/abc?foo=bar&hello=world').tostring() == '<a href="/abc?foo=bar&amp;hello=world"></a>'
    assert h.a(href='abc?foo=bar&hello=world').tostring() == '<a href="/root/abc?foo=bar&amp;hello=world&amp;ver=1.2"></a>'
