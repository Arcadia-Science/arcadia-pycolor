import pytest

from arcadia_pycolor import HexCode, Palette

from .test_hexcode import INVALID_HEXCODES


def test_palette_from_hexcode_list():
    hex_codes = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    assert Palette("my_palette", hex_codes).colors == hex_codes


@pytest.mark.parametrize(
    "invalid_input",
    INVALID_HEXCODES,
)
def test_palette_from_hexcode_list_invalid_input(invalid_input):
    with pytest.raises(ValueError):
        Palette("a", [invalid_input])


def test_palette_from_dict():
    hex_codes = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    assert (
        Palette.from_dict(
            "my_palette",
            {"white": "#FFFFFF", "black": "#000000"},
        ).colors
        == hex_codes
    )


def test_palette_repr():
    expected_swatch = "\x1b[48;2;255;255;255m  \x1b[0m\x1b[48;2;0;0;0m  \x1b[0m\n\x1b[48;2;255;255;255m  \x1b[0m\x1b[38;2;255;255;255m white #FFFFFF\x1b[0m\n\x1b[48;2;0;0;0m  \x1b[0m\x1b[38;2;0;0;0m black #000000\x1b[0m"  # noqa E501
    assert (
        Palette(
            "my_palette",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        ).__repr__()
        == expected_swatch
    )


@pytest.mark.parametrize(
    "name, input, longest_name_length",
    [
        (
            "my_palette",
            [HexCode("white", "#FFFFFF"), HexCode("tangerine", "#FFB984")],
            9,
        ),
        (
            "my_palette",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            5,
        ),
    ],
)
def test_get_longest_name_length(name, input, longest_name_length):
    assert Palette(name, input)._get_longest_name_length() == longest_name_length


def test_palette_add():
    p1 = [HexCode("white", "#FFFFFF")]
    p2 = [HexCode("black", "#000000")]
    result = p1 + p2
    assert (Palette("p1", p1) + Palette("p2", p2)).colors == result
    assert (Palette("p1", p1) + Palette("p2", p2)).name == "p1+p2"
