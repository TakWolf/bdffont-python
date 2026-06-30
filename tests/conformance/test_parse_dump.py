from pathlib import Path

import pytest

from bdffont import BdfFont


@pytest.mark.parametrize(
    'font_dir, font_file_name', [
        ('demo', 'demo.bdf'),
        ('misaki', 'misaki_gothic.bdf'),
        ('misaki', 'misaki_gothic_2nd.bdf'),
        ('misaki', 'misaki_mincho.bdf'),
        ('unifont', 'unifont-17.0.05.bdf'),
    ],
)
def test_parse_dump(assets_dir: Path, font_dir: str, font_file_name: str):
    data = assets_dir.joinpath(font_dir, font_file_name).read_text('utf-8')
    font = BdfFont.parse(data)
    assert font.dump_to_string() == data.replace('\r\n', '\n').replace('\nBITMAP \n', '\nBITMAP\n')
