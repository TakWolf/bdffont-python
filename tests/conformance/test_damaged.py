import re
from pathlib import Path

import pytest

from bdffont import BdfFont
from bdffont.error import BdfParseError, BdfMissingWordError, BdfIllegalWordError, BdfCountError


def test_not_bdf(assets_dir: Path) -> None:
    with pytest.raises(BdfIllegalWordError, match=re.escape("illegal word: 'This'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'not_bdf.bdf'))
    assert info.value.word == 'This'


def test_unsupported_version(assets_dir: Path) -> None:
    with pytest.raises(BdfParseError, match=re.escape("unsupported BDF version: '2.2'")):
        BdfFont.load(assets_dir.joinpath('damaged', 'unsupported_version.bdf'))


def test_no_line_font(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'FONT'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_font.bdf'))
    assert info.value.word == 'FONT'


def test_no_line_size(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'SIZE'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_size.bdf'))
    assert info.value.word == 'SIZE'


def test_no_line_fontboundingbox(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'FONTBOUNDINGBOX'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_fontboundingbox.bdf'))
    assert info.value.word == 'FONTBOUNDINGBOX'


def test_no_line_end_properties(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'ENDPROPERTIES'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_end_properties.bdf'))
    assert info.value.word == 'ENDPROPERTIES'


def test_no_line_chars(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'CHARS'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_chars.bdf'))
    assert info.value.word == 'CHARS'


def test_no_line_encoding(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'ENCODING'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_encoding.bdf'))
    assert info.value.word == 'ENCODING'


def test_no_line_swidth(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'SWIDTH'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_swidth.bdf'))
    assert info.value.word == 'SWIDTH'


def test_no_line_dwidth(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'DWIDTH'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_dwidth.bdf'))
    assert info.value.word == 'DWIDTH'


def test_no_line_bbx(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'BBX'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_bbx.bdf'))
    assert info.value.word == 'BBX'


def test_no_line_end_char(assets_dir: Path) -> None:
    with pytest.raises(ValueError, match=re.escape("invalid literal for int() with base 16: 'STARTCHAR'")):
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_end_char.bdf'))


def test_no_line_end_font(assets_dir: Path) -> None:
    with pytest.raises(BdfMissingWordError, match=re.escape("missing word: 'ENDFONT'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'no_line_end_font.bdf'))
    assert info.value.word == 'ENDFONT'


def test_illegal_word_in_font(assets_dir: Path) -> None:
    with pytest.raises(BdfIllegalWordError, match=re.escape("illegal word: 'ABC'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'illegal_word_in_font.bdf'))
    assert info.value.word == 'ABC'


def test_illegal_word_in_char(assets_dir: Path) -> None:
    with pytest.raises(BdfIllegalWordError, match=re.escape("illegal word: 'DEF'")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'illegal_word_in_char.bdf'))
    assert info.value.word == 'DEF'


def test_incorrect_properties_count(assets_dir: Path) -> None:
    with pytest.raises(BdfCountError, match=re.escape("the count of 'STARTPROPERTIES' is incorrect: 1000 -> 19")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'incorrect_properties_count.bdf'))
    assert info.value.word == 'STARTPROPERTIES'


def test_incorrect_chars_count(assets_dir: Path) -> None:
    with pytest.raises(BdfCountError, match=re.escape("the count of 'CHARS' is incorrect: 1000 -> 2")) as info:
        BdfFont.load(assets_dir.joinpath('damaged', 'incorrect_chars_count.bdf'))
    assert info.value.word == 'CHARS'
