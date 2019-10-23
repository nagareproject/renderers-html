# --
# Copyright (c) 2008-2019 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

try:
    from cStringIO import StringIO as BuffIO
except ImportError:
    from io import BytesIO as BuffIO

import pytest
from lxml import etree
from nagare.renderers import html_base as html


def c14n(node):
    if not isinstance(node, (str, type(u''))):
        node = node.tostring(method='xml').decode('utf-8')

    node = etree.fromstring(node).getroottree()

    buf = BuffIO()
    node.write_c14n(buf)

    return buf.getvalue()


def test_head1():
    h = html.HeadRenderer()

    assert h.head(h.title('test')).tostring() == b'<head><title>test</title></head>'

    with pytest.raises(AttributeError):
        h.foo


def test_head2():
    h = html.HeadRenderer()

    assert h.link.tostring() == b'<link>'
    assert h.link.tostring(method='xml') == b'<link/>'


def test_url():
    h = html.HeadRenderer()

    assert h.link(href='/abc').tostring() == b'<link href="/abc">'
    assert h.link(href='abc').tostring() == b'<link href="abc">'

    h = html.HeadRenderer(static_url='/root')

    assert h.link(rel='stylesheet', href='/abc').get('href') == '/abc'
    assert h.link(rel='stylesheet', href='abc').get('href') == '/root/abc'

    h = html.HeadRenderer()

    assert h.script(src='/abc').tostring() == b'<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == b'<script src="abc"></script>'

    h = html.HeadRenderer(static_url='/root')

    assert h.script(src='/abc').tostring() == b'<script src="/abc"></script>'
    assert h.script(src='abc').tostring() == b'<script src="/root/abc"></script>'


def test_css_js_order():
    head = html.HeadRenderer('')

    for i in range(10):
        head.css(str(i), 'style_%d.css' % i, a=42 + i)

    result = [(str(i), ('style_%d.css' % i, {'a': 42 + i})) for i in range(10)]
    assert list(head._named_css.items()) == result

    for i in range(10):
        head.css_url('http://example.com/style_%d.css' % i, a=42 + i)

    result = [('http://example.com/style_%d.css' % i, {'a': 42 + i}) for i in range(10)]
    assert list(head._css_url.items()) == result

    for i in range(10):
        head.javascript(str(i), 'js_%d.js' % i, a=42 + i)

    result = [(str(i), ('js_%d.js' % i, {'a': 42 + i}, False)) for i in range(10)]
    assert list(head._named_javascript.items()) == result

    for i in range(10):
        head.javascript_url('http://example.com/js_%d.js' % i, a=42 + i)

    result = [('http://example.com/js_%d.js' % i, ({'a': 42 + i}, False)) for i in range(10)]
    assert list(head._javascript_url.items()) == result


def test_css_js_override():
    head = html.HeadRenderer('')

    head.css('css1', 'css1', a=42)
    head.css('css1', 'css2', b=42)

    assert list(head._named_css.items()) == [('css1', ('css1', {'a': 42}))]

    head.css_url('http://example.com/style_1.css', a=42)
    head.css_url('http://example.com/style_1.css', b=42)

    assert list(head._css_url.items()) == [('http://example.com/style_1.css', {'a': 42})]

    head.javascript('js1', 'javascript1', a=42)
    head.javascript('js1', 'javascript2', b=42)

    assert list(head._named_javascript.items()) == [('js1', ('javascript1', {'a': 42}, False))]

    head.javascript_url('http://example.com/js_1.js', a=42)
    head.javascript_url('http://example.com/js_1.js', b=42)

    assert list(head._javascript_url.items()) == [('http://example.com/js_1.js', ({'a': 42}, False))]


def test_head_render_javascript_css1():
    h = html.HeadRenderer('/tmp/static_directory')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.css_url('css')

    assert list(h._css_url.items()) == [('/tmp/static_directory/css', {})]

    h = html.HeadRenderer('/tmp/static_directory', assets_version='1.2')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.css_url('css')

    assert list(h._css_url.items()) == [('/tmp/static_directory/css?ver=1.2', {})]


def test_head_render_javascript_css2():
    """ XHTML namespace unit test - HeadRender - css_url - absolute url """
    h = html.HeadRenderer('/tmp/static_directory/')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.css_url('/css')

    assert list(h._css_url.items()) == [('/css', {})]

    h = html.HeadRenderer('/tmp/static_directory/', assets_version='1.2')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.css_url('/css')

    assert list(h._css_url.items()) == [('/css', {})]


def test_head_render_css_url3():
    """ XHTML namespace unit test - HeadRender - css_url - absolute url + relative url """
    h = html.HeadRenderer('/tmp/static_directory/')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.css_url('/css', a=42)
        h << h.css_url('css', b=10)

    assert h._css_url['/css'] == {'a': 42}
    assert h._css_url['/tmp/static_directory/css'] == {'b': 10}


def test_head_render_javascript_url1():
    """ XHTML namespace unit test - HeadRender - javascript_url - relative url """
    h = html.HeadRenderer('/tmp/static_directory/')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.javascript_url('test.js')

    assert list(h._javascript_url.items()) == [('/tmp/static_directory/test.js', ({}, False))]


def test_head_render_javascript_url2():
    """ XHTML namespace unit test - HeadRender - javascript_url - absolute url """
    h = html.HeadRenderer('/tmp/static_directory/')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.javascript_url('/test.js')
    assert list(h._javascript_url.items()) == [('/test.js', ({}, False))]


def test_head_render_javascript_url3():
    """ XHTML namespace unit test - HeadRender - javascript_url - absolute url + relative url """
    h = html.HeadRenderer('/tmp/static_directory/')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.javascript_url('/test.js', a=42)
        h << h.javascript_url('test.js', b=10)

    assert h._javascript_url['/test.js'] == ({'a': 42}, False)
    assert h._javascript_url['/tmp/static_directory/test.js'] == ({'b': 10}, False)


def test_head_render_javascript_url4():
    """ XHTML namespace unit test - HeadRender - javascript_url - Add twice the same js_url"""
    h = html.HeadRenderer('/tmp/static_directory/')
    with h.head({'lang': 'lang', 'dir': 'dir', 'id': 'id', 'profile': 'profile'}):
        h << h.javascript_url('test.js')
        h << h.javascript_url('test.js')

    assert list(h._javascript_url.items()) == [('/tmp/static_directory/test.js', ({}, False))]


def test_head_render_render1():
    """ XHTML namespace unit test - HeadRender - Render - render only style tag """
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.style()
    assert c14n(h.render_top()) == c14n('<head><style></style></head>')


def test_head_render_render2():
    """ XHTML namespace unit test - HeadRender - Render - render only css_url method """
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.css_url('css')
    assert c14n(h.render_top()) == c14n('<head><link href="/tmp/static_directory/css" type="text/css" rel="stylesheet"/></head>')


def test_head_render_render3():
    """ XHTML namespace unit test - HeadRender - Render - render only css method """
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.css('css_test', 'test')
    assert c14n(h.render_top()) == c14n('<head><style data-nagare-css="css_test" type="text/css">test</style></head>')


def test_head_render_render4():
    """ XHTML namespace unit test - HeadRender - Render - call render two times with css_url method"""
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.css_url('css')
    h.render_top()
    renderResult = h.render_top()
    assert not isinstance(renderResult, list)
    assert c14n(h.render_top()) == c14n('<head><link href="/tmp/static_directory/css" type="text/css" rel="stylesheet"/></head>')


def test_head_render_render5():
    """ XHTML namespace unit test - HeadRender - Render - render only css method """
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.css('css_test', 'test')
    assert c14n(h.render_top()) == c14n('<head><style type="text/css" data-nagare-css="css_test">test</style></head>')


def test_head_render_render6():
    """ XHTML namespace unit test - HeadRender - Render - render only javascript_url method """
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.javascript_url('test.js')
    assert c14n(h.render_top()) == c14n('<head><script src="/tmp/static_directory/test.js" type="text/javascript"></script></head>')


def test_head_render_render7():
    """ XHTML namespace unit test - HeadRender - Render - render only string js method """
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.javascript('test.js', 'function test() { return True }')
    assert c14n(h.render_top()) == c14n('<head><script data-nagare-js="test.js" type="text/javascript">function test() { return True }</script></head>')


def test_head_render_render8():
    """ XHTML namespace unit test - HeadRender - Render - render with head """
    h = html.HeadRenderer('/tmp/static_directory/')
    h << h.head({'id': 'id'})
    assert c14n(h.render_top()) == c14n('<head id="id"></head>')


def test_head_render_render9():
    """ XHTML namespace unit test - HeadRender - Render - render with head & style """
    h = html.HeadRenderer('/tmp/static_directory/')
    with h.head({'id': 'id'}):
        h << h.style('test', {'id': 'id'})
    assert c14n(h.render_top()) == c14n('<head id="id"><style id="id">test</style></head>')


def test_cache_buster():
    h = html.HeadRenderer(assets_version='1.2')

    assert h.link(rel='stylesheet', href='/abc').get('href') == '/abc'
    assert h.link(rel='stylesheet', href='abc').get('href') == 'abc?ver=1.2'

    assert h.link(rel='next', href='/abc').get('href') == '/abc'
    assert h.link(rel='next', href='abc').get('href') == 'abc'

    h = html.HeadRenderer(static_url='/root', assets_version='1.2')

    assert h.link(rel='stylesheet', href='/abc').get('href') == '/abc'
    assert h.link(rel='stylesheet', href='abc').get('href') == '/root/abc?ver=1.2'

    assert h.link(rel='next', href='/abc').get('href') == '/abc'
    assert h.link(rel='next', href='abc').get('href') == 'abc'

    h = html.HeadRenderer(static_url='/root', assets_version='1.2')

    assert h.link(rel='stylesheet', href='/abc?foo=bar').get('href') == '/abc?foo=bar'
    assert h.link(rel='stylesheet', href='abc?foo=bar').get('href') == '/root/abc?foo=bar&ver=1.2'
    assert h.link(rel='stylesheet', href='/abc?foo=bar&hello=world').get('href') == '/abc?foo=bar&hello=world'
    assert h.link(rel='stylesheet', href='abc?foo=bar&hello=world').get('href') == '/root/abc?foo=bar&hello=world&ver=1.2'
