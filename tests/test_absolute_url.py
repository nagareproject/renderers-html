# --
# Copyright (c) 2008-2020 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from nagare.renderers import html_base as html


def test_absolute_asset_url1():
    assert html.absolute_asset_url('', None) == ''

    assert html.absolute_asset_url('/', None) == '/'
    assert html.absolute_asset_url('/abc', '/static/root') == '/abc'

    assert html.absolute_asset_url('http://abc', None) == 'http://abc'

    assert html.absolute_asset_url('abc', None) == 'abc'
    assert html.absolute_asset_url('abc/', None) == 'abc/'


def test_absolute_asset_url2():
    assert html.absolute_asset_url('', None, foo='bar') == '?foo=bar'
    assert html.absolute_asset_url('', None, foo='bar', hello='world') == '?foo=bar&hello=world'
    assert html.absolute_asset_url('abc', '/static/root', foo='bar') == '/static/root/abc?foo=bar'
    assert html.absolute_asset_url('abc', '/static/root', foo='bar', hello='world') == '/static/root/abc?foo=bar&hello=world'


def test_absolute_asset_url3():
    assert html.absolute_asset_url('', '/static/root') == '/static/root/'

    assert html.absolute_asset_url('/', '/static/root') == '/'
    assert html.absolute_asset_url('/abc', '/static/root') == '/abc'

    assert html.absolute_asset_url('http://abc', '/static/root') == 'http://abc'

    assert html.absolute_asset_url('abc', '') == 'abc'
    assert html.absolute_asset_url('abc/', '') == 'abc/'

    assert html.absolute_asset_url('abc', '/static/root') == '/static/root/abc'
    assert html.absolute_asset_url('abc', '/static/root/') == '/static/root/abc'
    assert html.absolute_asset_url('abc/', '/static/root') == '/static/root/abc/'
    assert html.absolute_asset_url('abc/', '/static/root/') == '/static/root/abc/'


def test_absolute_asset_url4():
    head = html.HeadRenderer('/static/root2')

    assert head.absolute_asset_url('', '/static/root') == '/static/root/'

    assert head.absolute_asset_url('/', '/static/root') == '/'
    assert head.absolute_asset_url('/abc', '/static/root') == '/abc'

    assert head.absolute_asset_url('http://abc', '/static/root') == 'http://abc'

    assert head.absolute_asset_url('abc', '') == 'abc'
    assert head.absolute_asset_url('abc/', '') == 'abc/'

    assert head.absolute_asset_url('abc', '/static/root') == '/static/root/abc'
    assert head.absolute_asset_url('abc', '/static/root/') == '/static/root/abc'
    assert head.absolute_asset_url('abc/', '/static/root') == '/static/root/abc/'
    assert head.absolute_asset_url('abc/', '/static/root/') == '/static/root/abc/'

    assert head.absolute_asset_url('') == '/static/root2/'

    assert head.absolute_asset_url('/') == '/'
    assert head.absolute_asset_url('/abc') == '/abc'

    assert head.absolute_asset_url('http://abc') == 'http://abc'

    assert head.absolute_asset_url('abc', '') == 'abc'
    assert head.absolute_asset_url('abc/', '') == 'abc/'

    assert head.absolute_asset_url('abc') == '/static/root2/abc'
    assert head.absolute_asset_url('abc') == '/static/root2/abc'
    assert head.absolute_asset_url('abc/') == '/static/root2/abc/'
    assert head.absolute_asset_url('abc/') == '/static/root2/abc/'


def test_absolute_asset_url5():
    h = html.Renderer(static_url='/static/root2')

    assert h.absolute_asset_url('', '/static/root') == '/static/root/'

    assert h.absolute_asset_url('/', '/static/root') == '/'
    assert h.absolute_asset_url('/abc', '/static/root') == '/abc'

    assert h.absolute_asset_url('http://abc', '/static/root') == 'http://abc'

    assert h.absolute_asset_url('abc', '') == 'abc'
    assert h.absolute_asset_url('abc/', '') == 'abc/'

    assert h.absolute_asset_url('abc', '/static/root') == '/static/root/abc'
    assert h.absolute_asset_url('abc', '/static/root/') == '/static/root/abc'
    assert h.absolute_asset_url('abc/', '/static/root') == '/static/root/abc/'
    assert h.absolute_asset_url('abc/', '/static/root/') == '/static/root/abc/'

    assert h.absolute_asset_url('') == '/static/root2/'

    assert h.absolute_asset_url('/') == '/'
    assert h.absolute_asset_url('/abc') == '/abc'

    assert h.absolute_asset_url('http://abc') == 'http://abc'

    assert h.absolute_asset_url('abc', '') == 'abc'
    assert h.absolute_asset_url('abc/', '') == 'abc/'

    assert h.absolute_asset_url('abc') == '/static/root2/abc'
    assert h.absolute_asset_url('abc') == '/static/root2/abc'
    assert h.absolute_asset_url('abc/') == '/static/root2/abc/'
    assert h.absolute_asset_url('abc/') == '/static/root2/abc/'


def test_absolute_asset_url6():
    h = html.Renderer(static_url='/static/root')

    assert h.absolute_asset_url('/tmp?a=42', '/abc') == '/tmp?a=42'
    assert h.absolute_asset_url('tmp?a=42', '/abc') == '/abc/tmp?a=42'
    assert h.absolute_asset_url('http://localhost/tmp?a=42', '/abc') == 'http://localhost/tmp?a=42'

    assert h.absolute_asset_url('/tmp?a=42', '/abc', b=43) in ('/tmp?a=42&b=43', '/tmp?b=43&a=42')
    assert h.absolute_asset_url('tmp?a=42', '/abc', b=43) in ('/abc/tmp?a=42&b=43', '/abc/tmp?b=43&a=42')
    assert h.absolute_asset_url('http://localhost/tmp?a=42', '/abc', b=43) in ('http://localhost/tmp?a=42&b=43', 'http://localhost/tmp?b=43&a=42')
