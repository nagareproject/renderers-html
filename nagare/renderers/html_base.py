# --
# Copyright (c) 2008-2019 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""The XHTML renderer

This renderer only depends on the ``nagare.renderers.xml`` module.
Having not dependencies to the Nagare framework make it suitable to be used in
others frameworks.
"""

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
from os import path
from collections import OrderedDict

from lxml import etree as ET

from nagare.renderers import xml
from nagare.renderers.xml import TagProp

# ---------------------------------------------------------------------------


# Common attributes
# -----------------

componentattrs = {'id', 'class', 'style', 'title'}
i18nattrs = {'lang', 'dir'}
eventattrs = {
    'onclick', 'ondblclick', 'onmousedown', 'onmouseup', 'onmousemove',
    'onmouseover', 'onmouseout', 'onkeypress', 'onkeydown', 'onkeyup'
}
allattrs = componentattrs | i18nattrs | eventattrs
focusattrs = {'accesskey', 'tabindex', 'onfocus', 'onblur'}

# ---------------------------------------------------------------------------


def absolute_url(url, url_prefix, always_relative=False, **params):
    """Convert a relative URL of a static content to an absolute one

    In:
      - ``url`` -- url to convert
      - ``url_prefix`` -- URL prefix of the static contents

    Return:
      - an absolute URL
    """
    parts = list(urlparse.urlparse(url))

    if not parts[0]:
        if always_relative or not parts[2].startswith('/'):
            parts[2] = path.join(url_prefix or '', parts[2].lstrip('/'))

        parts[4] = (parts[4] + '&' + '&'.join('%s=%s' % param for param in params.items())).lstrip('&')

        url = urlparse.urlunparse(parts)

    return url


class Tag(xml.Tag):
    """A html tag
    """

    def tostring(self, method='html', encoding='utf-8', pipeline=True, **kw):
        """Serialize in HTML the tree beginning at this tag

        In:
          - ``encoding`` -- encoding of the XML
          - ``pipeline`` -- if False, the ``meld:id`` attributes are deleted

        Return:
          - the HTML
        """
        return super(Tag, self).tostring(method, encoding, pipeline, **kw)

    def error(self, msg):
        """Mark this tag as erroneous

        In:
          - ``msg`` -- the error message

        Return:
          - ``self``
        """
        self.renderer.decorate_error(self, msg)


class HrefAttribute(Tag):
    ASSET_ATTR = 'href'

    def on_change(self):
        super(HrefAttribute, self).on_change()

        url = self.get(self.ASSET_ATTR, None)
        if url is not None:
            self.set(self.ASSET_ATTR, self.renderer.absolute_assets_url(url))
Base = Link = A = Area = HrefAttribute  # noqa: E305


class SrcAttribute(HrefAttribute):
    ASSET_ATTR = 'src'
IFrame = Input = Script = SrcAttribute  # noqa: E305


class Img(SrcAttribute):

    def on_change(self):
        super(Img, self).on_change()

        url = self.get('lowsrc', None)
        if url is not None:
            self.set('lowsrc', self.renderer.absolute_assets_url(url))


class HeadRenderer(xml.XmlRenderer):
    """The HTML head Renderer

    This renderer knows about the possible tags of a html ``<head>``
    """

    # Tag factories
    # -------------

    base = TagProp('base', {'id', 'href', 'target'}, Base)
    head = TagProp('head', i18nattrs | {'id', 'profile'})
    link = TagProp('link', allattrs | {'charset', 'href', 'hreflang', 'type', 'rel', 'rev', 'media', 'target'}, Link)
    meta = TagProp('meta', i18nattrs | {'id', 'http_equiv', 'name', 'content', 'scheme'})
    title = TagProp('title', i18nattrs | {'id'})
    style = TagProp('style', i18nattrs | {'id', 'media', 'type'})
    script = TagProp('script', i18nattrs | {'id', 'async', 'charset', 'defer', 'src', 'type'}, SrcAttribute)

    _parser = ET.HTMLParser()
    _parser.set_element_class_lookup(ET.ElementDefaultClassLookup(element=Tag))

    def __init__(self, static_url=None, assets_version=None):
        """Renderer initialisation

        The ``HeadRenderer`` keeps track of the javascript and css used by every views,
        to be able to concatenate them into the ``<head>`` section.
        """
        super(HeadRenderer, self).__init__()

        # Directory where are located the static contents of the application
        self.static_url = static_url
        self.assets_version = assets_version

        self._named_css = OrderedDict()  # CSS code
        self._css_url = OrderedDict()  # CSS URLs
        self._named_javascript = OrderedDict()  # Javascript code
        self._javascript_url = OrderedDict()  # Javascript URLs

    def fromfile(self, source, tags_factory=Tag, fragment=False, no_leading_text=False, **kw):
        return super(HeadRenderer, self).fromfile(source, tags_factory, fragment, no_leading_text, **kw)

    def fromstring(self, text, tags_factory=Tag, fragment=False, no_leading_text=False, **kw):
        return super(HeadRenderer, self).fromstring(text, tags_factory, fragment, no_leading_text, **kw)

    def absolute_url(self, url, url_prefix=None, always_relative=False, **params):
        return absolute_url(url, url_prefix if url_prefix is not None else self.static_url, always_relative, **params)

    def absolute_assets_url(self, url, static=None, **params):
        if self.assets_version:
            params.setdefault('ver', self.assets_version)

        return self.absolute_url(url, static, **params)

    def css(self, id_, style, **attributes):
        """Memorize an in-line named css style

        In:
          - ``id_`` -- unique id of this css style (to prevent double definition)
          - ``style`` -- the css style
          - ``attributes`` -- attributes of the generated ``<style>`` tag
        """
        self._named_css.setdefault(id_, (style, attributes))

    def css_url(self, url, **attributes):
        """Memorize a css style URL

        In:
          - ``url`` -- the css style URL
          - ``attributes`` -- attributes of the generated ``<link>`` tag
        """
        self._css_url.setdefault(self.absolute_assets_url(url), attributes)

    def javascript(self, id_, script, **attributes):
        """Memorize an in-line named javascript code

        In:
          - ``id_`` -- unique id of this javascript code (to prevent double definition)
          - ``script`` -- the javascript code
          - ``attributes`` -- attributes of the generated ``<script>`` tag
        """
        self._named_javascript.setdefault(id_, (script, attributes))

    def javascript_url(self, url, **attributes):
        """Memorize a javascript URL

        In:
          - ``url`` -- the javascript URL
          - ``attributes`` -- attributes of the the generated ``<script>`` tag

        Return:
          - ``()``
        """
        self._javascript_url.setdefault(self.absolute_assets_url(url), attributes)

    def render(self):
        # Create the tags to include the CSS styles and the javascript codes
        head = self.root

        if isinstance(head, ET.ElementBase) and (head.tag == 'head'):
            # If a ``<head>`` tag already exist, take its content
            head = self.head(head[:], dict(head.attrib))
        else:
            head = self.head(head)

        head.extend(
            self.link(rel='stylesheet', type='text/css', href=url, **attributes)
            for url, attributes
            in self._css_url.items()
        )
        head.extend(
            self.script(type='text/javascript', src=url, **attributes)
            for url, attributes
            in self._javascript_url.items()
        )

        head.extend(
            self.style(css, type='text/css', data_nagare_css=name, **attributes)
            for name, (css, attributes)
            in self._named_css.items()
        )
        head.extend(
            self.script(js, type='text/javascript', data_nagare_js=name, **attributes)
            for name, (js, attributes)
            in self._named_javascript.items()
        )

        return head


class Renderer(xml.XmlRenderer):
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    content_type = 'text/html'
    head_renderer_factory = HeadRenderer

    componentattrs = {'id', 'class', 'style', 'title'}
    i18nattrs = {'lang', 'dir'}
    eventattrs = {
        'onclick', 'ondblclick', 'onmousedown', 'onmouseup', 'onmousemove',
        'onmouseover', 'onmouseout', 'onkeypress', 'onkeydown', 'onkeyup'
    }
    focusattrs = {'accesskey', 'tabindex', 'onfocus', 'onblur'}
    cellhalignattrs = {'align', 'char', 'charoff'}
    cellvalignattrs = {'valign'}
    allattrs = componentattrs | i18nattrs | eventattrs

    # The HTML tags
    # -------------

    a = TagProp('a', allattrs | focusattrs | {
        'charset', 'type', 'name', 'href', 'hreflang', 'rel',
        'rev', 'shape', 'coords', 'target', 'oncontextmenu'
    }, A)
    abbr = TagProp('abbr', allattrs)
    acronym = TagProp('acronym', allattrs)
    address = TagProp('address', allattrs)
    applet = TagProp('applet', componentattrs | {
        'codebase', 'archive', 'code', 'object', 'alt', 'name', 'width',
        'height', 'align', 'hspace', 'vspace'
    })
    area = TagProp('area', allattrs | focusattrs | {'shape', 'coords', 'href', 'nohref', 'alt', 'target'}, Area)
    b = TagProp('b', allattrs)
    basefont = TagProp('basefont', componentattrs | i18nattrs | {'id', 'size', 'color', 'face'})
    bdo = TagProp('bdo', componentattrs | eventattrs | {'lang', 'dir'})
    big = TagProp('big', allattrs)
    blockquote = TagProp('blockquote', allattrs | {'cite'})
    body = TagProp('body', allattrs | {
        'onload', 'onunload', 'onfocus', 'background', 'bgcolor', 'text',
        'link', 'vlink', 'alink', 'leftmargin', 'topmargin', 'marginwidth', 'marginheight'
    })
    br = TagProp('br', componentattrs | {'clear'})
    button = TagProp('button', allattrs | focusattrs | {'name', 'value', 'type', 'disabled'})
    caption = TagProp('caption', allattrs | {'align'})
    center = TagProp('center', allattrs)
    cite = TagProp('cite', allattrs)
    code = TagProp('code', allattrs)
    col = TagProp('col', allattrs | cellhalignattrs | cellvalignattrs | {'span', 'width'})
    colgroup = TagProp('colgroup', allattrs | cellhalignattrs | cellvalignattrs | {'span', 'width'})
    dd = TagProp('dd', allattrs)
    del_ = TagProp('del', allattrs | {'cite', 'datetime'})
    dfn = TagProp('dfn', allattrs)
    dir = TagProp('dir', allattrs | {'compact'})
    div = TagProp('div', allattrs | {'align'})
    dl = TagProp('dl', allattrs | {'compact'})
    dt = TagProp('dt', allattrs)
    em = TagProp('em', allattrs)
    embed = TagProp('embed', {
        'width', 'height', 'src', 'controller', 'src', 'target',
        'border', 'pluginspage', 'quality', 'type', 'bgcolor', 'menu'
    }, SrcAttribute)
    fieldset = TagProp('fieldset', allattrs)
    font = TagProp('font', componentattrs | i18nattrs | {'face', 'size', 'color'})
    form = TagProp('form', allattrs | {
        'action', 'method', 'name', 'enctype',
        'onsubmit', 'onreset', 'accept_charset', 'target'
    })
    frame = TagProp('frame', set())
    frameset = TagProp('frameset', componentattrs | {
        'rows', 'cols', 'onload', 'onunload', 'framespacing', 'border',
        'marginwidth', 'marginheight', 'frameborder', 'noresize', 'scrolling'
    })
    h1 = TagProp('h1', allattrs | {'align'})
    h2 = TagProp('h2', allattrs | {'align'})
    h3 = TagProp('h3', allattrs | {'align'})
    h4 = TagProp('h4', allattrs | {'align'})
    h5 = TagProp('h5', allattrs | {'align'})
    h6 = TagProp('h6', allattrs | {'align'})
    hr = TagProp('hr', allattrs | {'align', 'noshade', 'size', 'width', 'color'})
    html = TagProp('html', i18nattrs | {'id'})
    i = TagProp('i', allattrs)
    iframe = TagProp('iframe', componentattrs | {
        'longdesc', 'name', 'src', 'frameborder', 'marginwidth', 'marginheight',
        'noresize', 'scrolling', 'align', 'height', 'width', 'hspace', 'vspace', 'bordercolor',
    }, IFrame)
    img = TagProp('img', allattrs | {
        'src', 'alt', 'name', 'longdesc', 'width', 'height', 'usemap',
        'ismap', 'align', 'border', 'hspace', 'vspace', 'lowsrc'
    }, Img)
    input = TagProp('input', allattrs | focusattrs | {
        'type', 'name', 'value', 'checked', 'disabled', 'readonly', 'size', 'maxlength',
        'src', 'alt', 'usemap', 'onselect', 'onchange', 'accept', 'align', 'border'
    }, Input)
    ins = TagProp('ins', allattrs | {'cite', 'datetime'})
    isindex = TagProp('isindex', componentattrs | i18nattrs | {'prompt'})
    kbd = TagProp('kbd', allattrs)
    label = TagProp('label', allattrs | {'for', 'accesskey', 'onfocus', 'onblur'})
    legend = TagProp('legend', allattrs | {'accesskey', 'align'})
    li = TagProp('li', allattrs | {'type', 'value'})
    map = TagProp('map', i18nattrs | eventattrs | {'id', 'class', 'style', 'title', 'name'})
    menu = TagProp('menu', allattrs | {'compact'})
    noframes = TagProp('noframes', allattrs)
    noscript = TagProp('noscript', allattrs)
    object = TagProp('object', allattrs | {
        'declare', 'classid', 'codebase', 'data', 'type', 'codetype',
        'archive', 'standby', 'height', 'width', 'usemap', 'name',
        'tabindex', 'align', 'border', 'hspace', 'vspace'
    })
    ol = TagProp('ol', allattrs | {'type', 'compact', 'start'})
    optgroup = TagProp('optgroup', allattrs | {'disabled', 'label'})
    option = TagProp('option', allattrs | {'selected', 'disabled', 'label', 'value'})
    p = TagProp('p', allattrs | {'align'})
    param = TagProp('param', {'id', 'name', 'value', 'valuetype', 'type'})
    pre = TagProp('pre', allattrs | {'width'})
    q = TagProp('q', allattrs | {'cite'})
    s = TagProp('s', allattrs)
    samp = TagProp('samp', allattrs)
    script = TagProp('script', {'id', 'charset', 'type', 'language', 'src', 'defer'}, Script)
    select = TagProp('select', allattrs | {
        'name', 'size', 'multiple', 'disabled', 'tabindex',
        'onfocus', 'onblur', 'onchange', 'rows'
    })
    small = TagProp('small', allattrs)
    span = TagProp('span', allattrs)
    strike = TagProp('strike', allattrs)
    strong = TagProp('strong', allattrs)
    style = TagProp('style', i18nattrs | {'id', 'type', 'media', 'title'})
    sub = TagProp('sub', allattrs)
    sup = TagProp('sup', allattrs)
    table = TagProp('table', componentattrs | i18nattrs | {'prompt'})
    tbody = TagProp('tbody', allattrs | cellhalignattrs | cellvalignattrs)
    td = TagProp('td', allattrs | cellhalignattrs | cellvalignattrs | {
        'abbr', 'axis', 'headers', 'scope', 'rowspan',
        'colspan', 'nowrap', 'bgcolor', 'width', 'height',
        'background', 'bordercolor'
    })
    textarea = TagProp('textarea', allattrs | focusattrs | {
        'name', 'rows', 'cols', 'disabled',
        'readonly', 'onselect', 'onchange', 'wrap'
    })
    tfoot = TagProp('tfoot', allattrs | cellhalignattrs | cellvalignattrs)
    th = TagProp('th', allattrs | cellhalignattrs | cellvalignattrs | {
        'abbr', 'axis', 'headers', 'scope', 'rowspan',
        'colspan', 'nowrap', 'bgcolor', 'width', 'height'
        'background', 'bordercolor'
    })
    thead = TagProp('thead', allattrs | cellhalignattrs | cellvalignattrs)
    tr = TagProp('tr', allattrs | cellhalignattrs | cellvalignattrs | {'bgcolor', 'nowrap', 'width', 'background'})
    tt = TagProp('tt', allattrs)
    u = TagProp('u', allattrs)
    ul = TagProp('ul', allattrs | {'type', 'compact'})
    var = TagProp('var', allattrs)

#    frame = TagProp('frame', componentattrs | {'longdesc', 'name', 'src', 'frameborder', 'marginwidht', 'marginheight',
#                                                                  'noresize', 'scrolling', 'framespacing', 'border', 'marginwidth', 'marginheight',
#                                                                  'frameborder', 'noresize', 'scrolling'}, SrcAttribute)
    _parser = ET.HTMLParser()
    _parser.set_element_class_lookup(ET.ElementDefaultClassLookup(element=Tag))

    def __init__(self, parent=None, **kw):
        """Renderer initialisation

        In:
          - ``parent`` -- parent renderer
        """
        super(Renderer, self).__init__(parent)

        if parent:
            self.head = parent.head
        else:
            self.head = self.head_renderer_factory(**kw)

    def fromfile(self, source, tags_factory=Tag, fragment=False, no_leading_text=False, **kw):
        return super(Renderer, self).fromfile(source, tags_factory, fragment, no_leading_text, **kw)

    def fromstring(self, text, tags_factory=Tag, fragment=False, no_leading_text=False, **kw):
        return super(Renderer, self).fromstring(text, tags_factory, fragment, no_leading_text, **kw)

    def absolute_url(self, url, static=None, **params):
        return (self.head.absolute_url if self.head is not None else absolute_url)(url, static, **params)

    def absolute_assets_url(self, url, static=None, **params):
        return (self.head.absolute_assets_url if self.head is not None else absolute_url)(url, static, **params)

    @staticmethod
    def decorate_error(tag, msg):
        return tag
