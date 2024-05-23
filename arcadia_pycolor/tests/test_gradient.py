import pytest

from arcadia_pycolor import HexCode, Palette


@pytest.mark.parametrize(
    "name, input, hex_codes",
    [
        (
            "my_palette",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        )
    ],
)
def test_palette(name, input, hex_codes):
    assert Palette(name, input).colors == hex_codes


@pytest.mark.parametrize(
    "name, input, hex_codes",
    [
        (
            "my_palette",
            {"white": "#FFFFFF", "black": "#000000"},
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        )
    ],
)
def test_palette_from_dict(name, input, hex_codes):
    assert Palette.from_dict(name, input).colors == hex_codes
