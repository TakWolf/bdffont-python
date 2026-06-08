from copy import copy, deepcopy

from bdffont import BdfGlyph


def test_glyph():
    glyph = BdfGlyph(name='A', encoding=65)
    assert glyph.name == 'A'
    assert glyph.encoding == 65
    assert glyph.scalable_width == (0, 0)
    assert glyph.device_width == (0, 0)
    assert glyph.bounding_box == (0, 0, 0, 0)
    assert glyph.bitmap == []
    assert glyph.comments == []

    glyph.scalable_width = 1, 2
    assert glyph.scalable_width == (1, 2)
    assert glyph.scalable_width_x == 1
    assert glyph.scalable_width_y == 2

    glyph.device_width = 3, 4
    assert glyph.device_width == (3, 4)
    assert glyph.device_width_x == 3
    assert glyph.device_width_y == 4

    glyph.dimensions = 5, 6
    assert glyph.dimensions == (5, 6)
    assert glyph.width == 5
    assert glyph.height == 6

    glyph.offset = 7, 8
    assert glyph.offset == (7, 8)
    assert glyph.offset_x == 7
    assert glyph.offset_y == 8

    glyph.bounding_box = 9, 10, 11, 12
    assert glyph.bounding_box == (9, 10, 11, 12)
    assert glyph.width == 9
    assert glyph.height == 10
    assert glyph.offset_x == 11
    assert glyph.offset_y == 12


def test_copy():
    glyph_1 = BdfGlyph(
        name='A',
        encoding=65,
        scalable_width=(1, 2),
        device_width=(3, 4),
        bounding_box=(5, 6, 7, 8),
        bitmap=[[1, 0, 0, 1]],
        comments=['This is a comment.'],
    )
    glyph_2 = copy(glyph_1)

    assert glyph_1 == glyph_2
    assert glyph_1 is not glyph_2
    assert glyph_1.bitmap is glyph_2.bitmap
    assert glyph_1.comments is glyph_2.comments


def test_deepcopy():
    glyph_1 = BdfGlyph(
        name='A',
        encoding=65,
        scalable_width=(1, 2),
        device_width=(3, 4),
        bounding_box=(5, 6, 7, 8),
        bitmap=[[1, 0, 0, 1]],
        comments=['This is a comment.'],
    )
    glyph_2 = deepcopy(glyph_1)

    assert glyph_1 == glyph_2
    assert glyph_1 is not glyph_2
    assert glyph_1.bitmap is not glyph_2.bitmap
    assert glyph_1.comments is not glyph_2.comments

    for bitmap_row_1, bitmap_row_2 in zip(glyph_1.bitmap, glyph_2.bitmap):
        assert bitmap_row_1 is not bitmap_row_2


def test_eq():
    glyph_1 = BdfGlyph(
        name='A',
        encoding=65,
        scalable_width=(1, 2),
        device_width=(3, 4),
        bounding_box=(5, 6, 7, 8),
        bitmap=[[1, 0, 0, 1]],
        comments=['This is a comment.'],
    )
    glyph_2 = BdfGlyph(
        name='A',
        encoding=65,
        scalable_width=(1, 2),
        device_width=(3, 4),
        bounding_box=(5, 6, 7, 8),
        bitmap=[[1, 0, 0, 1]],
        comments=['This is a comment.'],
    )
    assert glyph_1 == glyph_2
