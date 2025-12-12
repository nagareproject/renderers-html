# --
# Copyright (c) 2008-2025 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

import pytest

from nagare.renderers import html5_base as html5
from nagare.renderers import html_base as html


def test_new_tags():
    h = html.Renderer()

    with pytest.raises(AttributeError):
        h.section

    h = html5.Renderer()

    root = h.section
    assert root.tostring() == b"<section></section>"


def test_obsolete_tags():
    h = html.Renderer()

    root = h.center
    assert root.tostring() == b"<center></center>"

    h = html5.Renderer()

    with pytest.raises(AttributeError):
        h.center
