import shutil
import statistics

from bdffont import BdfFont, BdfGlyph
from examples import build_dir


def main():
    outputs_dir = build_dir.joinpath('create')
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir(parents=True)

    font = BdfFont(
        point_size=16,
        resolution=(75, 75),
        bounding_box=(16, 16, 0, -2),
    )

    font.glyphs.append(BdfGlyph(
        name='A',
        encoding=65,
        scalable_width=(500, 0),
        device_width=(8, 0),
        bounding_box=(8, 16, 0, -2),
        bitmap=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    ))

    font.properties.foundry = 'Pixel Font Studio'
    font.properties.family_name = 'My Font'
    font.properties.weight_name = 'Medium'
    font.properties.slant = 'R'
    font.properties.setwidth_name = 'Normal'
    font.properties.add_style_name = 'Sans Serif'
    font.properties.pixel_size = font.point_size
    font.properties.point_size = font.point_size * 10
    font.properties.resolution_x = font.resolution_x
    font.properties.resolution_y = font.resolution_y
    font.properties.spacing = 'P'
    font.properties.average_width = round(statistics.fmean(glyph.device_width_x * 10 for glyph in font.glyphs))
    font.properties.charset_registry = 'ISO10646'
    font.properties.charset_encoding = '1'
    font.generate_name_as_xlfd()

    font.properties.default_char = -1
    font.properties.font_ascent = 14
    font.properties.font_descent = 2
    font.properties.x_height = 7
    font.properties.cap_height = 10
    font.properties.underline_position = -2
    font.properties.underline_thickness = 1

    font.properties.font_version = '1.0.0'
    font.properties.copyright = 'Copyright (c) TakWolf'

    font.save(outputs_dir.joinpath('my-font.bdf'))


if __name__ == '__main__':
    main()
