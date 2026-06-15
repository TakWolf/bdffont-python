import textwrap
from copy import copy, deepcopy
from pathlib import Path

import pytest

from bdffont import BdfFont, BdfGlyph
from bdffont.error import BdfXlfdError, BdfDumpError


def test_font_1():
    font = BdfFont()

    font.resolution = 1, 2
    assert font.resolution == (1, 2)
    assert font.resolution_x == 1
    assert font.resolution_y == 2

    font.dimensions = 3, 4
    assert font.dimensions == (3, 4)
    assert font.width == 3
    assert font.height == 4

    font.offset = 5, 6
    assert font.offset == (5, 6)
    assert font.offset_x == 5
    assert font.offset_y == 6
    assert font.bounding_box == (3, 4, 5, 6)

    font.bounding_box = 7, 8, 9, 10
    assert font.bounding_box == (7, 8, 9, 10)
    assert font.width == 7
    assert font.height == 8
    assert font.offset_x == 9
    assert font.offset_y == 10


def test_font_2():
    font = BdfFont()

    font.point_size = 16
    font.resolution = 75, 75

    font.properties.foundry = 'TakWolf Studio'
    font.properties.family_name = 'Demo Pixel'
    font.properties.weight_name = 'Medium'
    font.properties.slant = 'R'
    font.properties.setwidth_name = 'Normal'
    font.properties.add_style_name = 'Sans Serif'
    font.properties.pixel_size = font.point_size
    font.properties.point_size = font.point_size * 10
    font.properties.resolution_x = font.resolution_x
    font.properties.resolution_y = font.resolution_y
    font.properties.spacing = 'P'
    font.properties.average_width = 80
    font.properties.charset_registry = 'ISO10646'
    font.properties.charset_encoding = '1'

    font.generate_name_as_xlfd()
    assert font.name == '-TakWolf Studio-Demo Pixel-Medium-R-Normal-Sans Serif-16-160-75-75-P-80-ISO10646-1'


def test_font_3():
    font = BdfFont()

    with pytest.raises(BdfXlfdError) as info:
        font.update_by_name_as_xlfd()
    assert info.value.args[0] == "must start with '-'"

    font.name = '--------------'
    font.update_by_name_as_xlfd()
    assert font.resolution_x == 0
    assert font.resolution_y == 0
    assert len(font.properties) == 0

    font.name = '-Adobe-Times-Medium-R-Normal--14-100-100-100-P-74-ISO8859-1'
    font.update_by_name_as_xlfd()
    assert font.resolution_x == 100
    assert font.resolution_y == 100
    assert font.properties.foundry == 'Adobe'
    assert font.properties.family_name == 'Times'
    assert font.properties.weight_name == 'Medium'
    assert font.properties.slant == 'R'
    assert font.properties.setwidth_name == 'Normal'
    assert font.properties.add_style_name is None
    assert font.properties.pixel_size == 14
    assert font.properties.point_size == 100
    assert font.properties.resolution_x == 100
    assert font.properties.resolution_y == 100
    assert font.properties.spacing == 'P'
    assert font.properties.average_width == 74
    assert font.properties.charset_registry == 'ISO8859'
    assert font.properties.charset_encoding == '1'


def test_demo(assets_dir: Path):
    font = BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))

    assert font.name == '-Adobe-Helvetica-Bold-R-Normal--24-240-75-75-P-65-ISO8859-1'
    assert font.point_size == 24
    assert font.resolution_x == 75
    assert font.resolution_y == 75
    assert font.resolution == (75, 75)
    assert font.width == 9
    assert font.height == 24
    assert font.dimensions == (9, 24)
    assert font.offset_x == -2
    assert font.offset_y == -6
    assert font.offset == (-2, -6)
    assert font.bounding_box == (9, 24, -2, -6)
    assert font.comments == ['This is a sample font in 2.1 format.']

    assert len(font.properties) == 19
    assert font.properties.foundry == 'Adobe'
    assert font.properties.family_name == 'Helvetica'
    assert font.properties.weight_name == 'Bold'
    assert font.properties.slant == 'R'
    assert font.properties.setwidth_name == 'Normal'
    assert font.properties.add_style_name == ''
    assert font.properties.pixel_size == 24
    assert font.properties.point_size == 240
    assert font.properties.resolution_x == 75
    assert font.properties.resolution_y == 75
    assert font.properties.spacing == 'P'
    assert font.properties.average_width == 65
    assert font.properties.charset_registry == 'ISO8859'
    assert font.properties.charset_encoding == '1'
    assert font.properties['MIN_SPACE'] == 4
    assert font.properties.font_ascent == 21
    assert font.properties.font_descent == 7
    assert font.properties.copyright == 'Copyright (c) 1987 Adobe Systems, Inc.'
    assert font.properties.notice == 'Helvetica is a registered trademark of Linotype Inc.'
    assert font.properties.comments == ['This is a comment in properties.']

    assert len(font.glyphs) == 2
    glyph = {glyph.encoding: glyph for glyph in font.glyphs}[39]
    assert glyph.name == 'quoteright'
    assert glyph.encoding == 39
    assert glyph.scalable_width_x == 223
    assert glyph.scalable_width_y == 0
    assert glyph.scalable_width == (223, 0)
    assert glyph.device_width_x == 5
    assert glyph.device_width_y == 0
    assert glyph.device_width == (5, 0)
    assert glyph.width == 4
    assert glyph.height == 6
    assert glyph.dimensions == (4, 6)
    assert glyph.offset_x == 2
    assert glyph.offset_y == 12
    assert glyph.offset == (2, 12)
    assert glyph.bounding_box == (4, 6, 2, 12)
    assert glyph.attributes == 0b_0000000111000000
    assert glyph.bitmap == [
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 0],
        [1, 1, 1, 0],
        [1, 1, 0, 0],
    ]
    assert glyph.comments == ['This is a comment in char.']


def test_multi_line_1():
    font = BdfFont()
    font.comments.append('Hello\nWorld')
    with pytest.raises(BdfDumpError) as info:
        font.dump_to_string()
    assert info.value.args[0] == 'tail cannot be multi-line string'


def test_multi_line_2():
    font = BdfFont()
    font.properties['ABC'] = 'Hello\nWorld'
    with pytest.raises(BdfDumpError) as info:
        font.dump_to_string()
    assert info.value.args[0] == 'property value cannot be multi-line string'


def test_multi_line_3():
    font = BdfFont()
    font.properties.comments.append('Hello\nWorld')
    with pytest.raises(BdfDumpError) as info:
        font.dump_to_string()
    assert info.value.args[0] == 'tail cannot be multi-line string'


def test_multi_line_4():
    font = BdfFont()
    font.glyphs.append(BdfGlyph(
        name='A',
        encoding=65,
        comments=['Hello\nWorld'],
    ))
    with pytest.raises(BdfDumpError) as info:
        font.dump_to_string()
    assert info.value.args[0] == 'tail cannot be multi-line string'


def test_parse_bitmap_1():
    font = BdfFont.parse(textwrap.dedent('''\
        STARTFONT 2.1
        FONT
        SIZE 0 0 0
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR _
        ENCODING 0
        SWIDTH 0 0
        DWIDTH 0 0
        BBX 10 1 0 0
        BITMAP
        FF
        ENDCHAR
        ENDFONT
    '''))
    assert font.glyphs[0].bitmap == [
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    ]


def test_parse_bitmap_2():
    font = BdfFont.parse(textwrap.dedent('''\
        STARTFONT 2.1
        FONT
        SIZE 0 0 0
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR _
        ENCODING 0
        SWIDTH 0 0
        DWIDTH 0 0
        BBX 6 1 0 0
        BITMAP
        FF
        ENDCHAR
        ENDFONT
    '''))
    assert font.glyphs[0].bitmap == [
        [1, 1, 1, 1, 1, 1],
    ]


def test_dump_bitmap_1():
    font = BdfFont()
    font.glyphs.append(BdfGlyph(
        name='_',
        encoding=0,
        bounding_box=(10, 1, 0, 0),
        bitmap=[
            [2, 2, 2, 2, 2, 2],
        ],
    ))
    assert font.dump_to_string() == textwrap.dedent('''\
        STARTFONT 2.1
        FONT
        SIZE 0 0 0
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR _
        ENCODING 0
        SWIDTH 0 0
        DWIDTH 0 0
        BBX 10 1 0 0
        BITMAP
        FC00
        ENDCHAR
        ENDFONT
    ''')


def test_dump_bitmap_2():
    font = BdfFont()
    font.glyphs.append(BdfGlyph(
        name='_',
        encoding=0,
        bounding_box=(6, 1, 0, 0),
        bitmap=[
            [2, 2, 2, 2, 2, 2, 2, 2],
        ],
    ))
    assert font.dump_to_string() == textwrap.dedent('''\
        STARTFONT 2.1
        FONT
        SIZE 0 0 0
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR _
        ENCODING 0
        SWIDTH 0 0
        DWIDTH 0 0
        BBX 6 1 0 0
        BITMAP
        FC
        ENDCHAR
        ENDFONT
    ''')


def test_copy(assets_dir: Path):
    font_1 = BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))
    font_2 = copy(font_1)

    assert font_1 == font_2
    assert font_1 is not font_2
    assert font_1.properties is font_2.properties
    assert font_1.glyphs is font_2.glyphs
    assert font_1.comments is font_2.comments


def test_deepcopy(assets_dir: Path):
    font_1 = BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))
    font_2 = deepcopy(font_1)

    assert font_1 == font_2
    assert font_1 is not font_2
    assert font_1.properties is not font_2.properties
    assert font_1.glyphs is not font_2.glyphs
    assert font_1.comments is not font_2.comments

    for glyph_1, glyph_2 in zip(font_1.glyphs, font_2.glyphs):
        assert glyph_1 is not glyph_2


def test_eq(assets_dir: Path):
    file_path = assets_dir.joinpath('demo', 'demo.bdf')
    font_1 = BdfFont.load(file_path)
    font_2 = BdfFont.load(file_path)
    assert font_1 == font_2
