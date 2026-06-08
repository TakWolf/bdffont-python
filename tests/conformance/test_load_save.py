from pathlib import Path

import pytest

from bdffont import BdfFont


@pytest.mark.parametrize(
    'font_dir, font_file_name', [
        ('demo', 'demo.bdf'),
        ('misaki', 'misaki_gothic.bdf'),
        ('misaki', 'misaki_gothic_2nd.bdf'),
        ('misaki', 'misaki_mincho.bdf'),
        ('unifont', 'unifont-17.0.04.bdf'),
    ],
)
def test_load_save(assets_dir: Path, tmp_path: Path, font_dir: str, font_file_name: str):
    load_path = assets_dir.joinpath(font_dir, font_file_name)
    save_path = tmp_path.joinpath(font_file_name)
    font = BdfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes().replace(b'\r\n', b'\n').replace(b'\nBITMAP \n', b'\nBITMAP\n') == save_path.read_bytes()
