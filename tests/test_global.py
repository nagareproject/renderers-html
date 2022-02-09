# --
# Copyright (c) 2008-2022 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from nagare.renderers import html_base as html
from nagare.renderers import html5_base as html5


RESULT = b'''
<html>
    <head>
        <title>A test</title>
        <script>function() {}</script>
    </head>
    <body onload="javascript:alert()">
        %s
        <ul>
            <li>Hello</li>
            <li>world</li>
            <li>foo</li>
        </ul>
        <div class="foo">
            <h1>bar<i>foo</i></h1>
        </div>
        <div>hello012</div>
        <table foo="bar">
            <tr>
                <td>1</td>
                <td>a</td>
            </tr>
            <tr>
                <td>2</td>
                <td>b</td>
            </tr>
            <tr>
                <td>3</td>
                <td>c</td>
            </tr>
        </table>
    </body>
</html>
'''


def test_html():
    t = ((1, 'a'), (2, 'b'), (3, 'c'))

    h = html.Renderer()

    h.head << h.head.title('A test')
    h.head << h.head.script('function() {}')

    with h.body(onload='javascript:alert()'):
        with h.ul:
            with h.li('Hello'):
                pass
            with h.li:
                h << 'world'
            h << h.li('foo')

        with h.div(class_='foo'):
            with h.h1('bar'):
                h << h.i('foo')

        with h.div:
            h << 'hello'
            for i in range(3):
                h << i

        with h.table(foo='bar'):
            for row in t:
                with h.tr:
                    for column in row:
                        with h.td:
                            h << column

    root = h.html(h.head.head(h.head.root), h.root)

    result = RESULT % b''
    result = b''.join(line.strip() for line in result.splitlines())

    assert root.tostring() == result


def test_html5():
    t = ((1, 'a'), (2, 'b'), (3, 'c'))

    h = html5.Renderer()

    h.head << h.head.title('A test')
    h.head << h.head.script('function() {}')

    with h.body(onload='javascript:alert()'):
        h << h.section(name='name')
        h << h.article
        h << h.aside
        h << h.hgroup
        h << h.header
        h << h.footer
        h << h.nav
        h << h.figure

        h << h.video
        h << h.audio
        h << h.source
        h << h.embed
        h << h.mark
        h << h.progress
        h << h.meter
        h << h.ruby
        h << h.rt
        h << h.rp
        h << h.wbr
        h << h.canvas
        h << h.command
        h << h.details
        h << h.summary
        h << h.datalist
        h << h.keygen
        h << h.output

        with h.ul:
            with h.li('Hello'):
                pass
            with h.li:
                h << 'world'
            h << h.li('foo')

        with h.div(class_='foo'):
            with h.h1('bar'):
                h << h.i('foo')

        with h.div:
            h << 'hello'
            for i in range(3):
                h << i

        with h.table(foo='bar'):
            for row in t:
                with h.tr:
                    for column in row:
                        with h.td:
                            h << column

    root = h.html(h.head.head(h.head.root), h.root)

    result = [
        b'<%s></%s>' % (tag, tag) for tag in b'article aside hgroup header footer nav figure '
        b'video audio source embed mark progress meter ruby rt '
        b'rp wbr canvas command details summary datalist keygen output'.split()
    ]

    result = RESULT % (b'<section name="name"></section>' + b''.join(result))
    result = b''.join(line.strip() for line in result.splitlines())

    assert root.tostring() == result
