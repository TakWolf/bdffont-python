from pathlib import Path

from bdffont import BdfFont


def test_unifont(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('unifont', 'unifont-16.0.02.bdf')
    save_path = tmp_path.joinpath('unifont-16.0.02.bdf')
    font = BdfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes().replace(b'\r\n', b'\n') == save_path.read_bytes().replace(b'\nBITMAP\n', b'\nBITMAP \n')


def test_misaki_gothic(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('misaki', 'misaki_gothic.bdf')
    save_path = tmp_path.joinpath('misaki_gothic.bdf')
    font = BdfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes().replace(b'\r\n', b'\n') == save_path.read_bytes()


def test_misaki_gothic_2nd(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('misaki', 'misaki_gothic_2nd.bdf')
    save_path = tmp_path.joinpath('misaki_gothic_2nd.bdf')
    font = BdfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes().replace(b'\r\n', b'\n') == save_path.read_bytes()


def test_misaki_mincho(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('misaki', 'misaki_mincho.bdf')
    save_path = tmp_path.joinpath('misaki_mincho.bdf')
    font = BdfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes().replace(b'\r\n', b'\n') == save_path.read_bytes()
