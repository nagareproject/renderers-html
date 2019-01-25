# --
# Copyright (c) 2008-2019 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""The XHTML5 renderer
"""

from nagare.renderers import html_base
from nagare.renderers.xml import TagProp


class ObsoleteTagProp(TagProp):
    """Class of all the HTML4 tags obsolete in HTML5
    """
    def __get__(self, renderer, cls):
        # Raise the same exception as when an attribute doesn't exist
        raise AttributeError("'%s' object has no attribute '%s'" % (renderer.__class__.__name__, self._name))


class Renderer(html_base.Renderer):
    """The XHTML5 synchronous renderer
    """

    doctype = '<!DOCTYPE html>'

    # New HTML5 tags
    # --------------

    section = TagProp('section')
    article = TagProp('article')
    aside = TagProp('aside')
    hgroup = TagProp('hgroup')
    header = TagProp('header')
    footer = TagProp('footer')
    nav = TagProp('nav')
    figure = TagProp('figure')
    figcaption = TagProp('figcaption')
    main = TagProp('main')
    time = TagProp('time')
    video = TagProp('video')
    audio = TagProp('audio')
    source = TagProp('source')
    embed = TagProp('embed')
    mark = TagProp('mark')
    meta = TagProp('meta')
    progress = TagProp('progress')
    meter = TagProp('meter')
    ruby = TagProp('ruby')
    rt = TagProp('rt')
    rp = TagProp('rp')
    wbr = TagProp('wbr')
    canvas = TagProp('canvas')
    command = TagProp('command')
    details = TagProp('details')
    summary = TagProp('summary')
    datalist = TagProp('datalist')
    keygen = TagProp('keygen')
    output = TagProp('output')
    track = TagProp('track')

    # Obsolete HTML4 tags
    # -------------------

    basefont = ObsoleteTagProp('basefont')
    big = ObsoleteTagProp('big')
    center = ObsoleteTagProp('center')
    font = ObsoleteTagProp('font')
    strike = ObsoleteTagProp('strike')
    tt = ObsoleteTagProp('tt')
    frame = ObsoleteTagProp('frame')
    frameset = ObsoleteTagProp('frameset')
    noframes = ObsoleteTagProp('u')
    acronym = ObsoleteTagProp('acronym')
    applet = ObsoleteTagProp('applet')
    isindex = ObsoleteTagProp('isindex')
    dir = ObsoleteTagProp('dir')
