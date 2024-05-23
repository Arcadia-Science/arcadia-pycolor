import pytest

from arcadia_pycolor import HexCode
from arcadia_pycolor.classes import _is_hex_code


@pytest.mark.parametrize(
    "hex_string, is_hex_code",
    [
        ("#FFFFFF", True),
        ("#FFFFFF", True),
        ("#FFF", True),
        ("#fff", True),
        ("#ZZZZZZ", False),
        ("#ZZZ", False),
        ("#FF", False),
        ("apples", False),
        ("123456", False),
        ("ffffff", False),
        ("white", False),
    ],
)
def test_is_hex_code(hex_string, is_hex_code):
    assert _is_hex_code(hex_string) == is_hex_code


@pytest.mark.parametrize(
    "name, hex_code",
    [
        ("white", "#FFFFFF"),
        ("white", "#ffffff"),
        ("white", "#FFF"),
        ("white", "#fff"),
    ],
)
def test_valid_hexcode(name, hex_code):
    assert HexCode(name, hex_code) == hex_code


@pytest.mark.parametrize(
    "name, hex_code",
    [
        ("white", "#ZZZZZZ"),
        ("white", "#ZZZ"),
        ("white", "#FF"),
        ("white", "apples"),
        ("white", "123456"),
        ("white", "ffffff"),
        ("white", "white"),
    ],
)
def test_invalid_hexcode(name, hex_code):
    with pytest.raises(ValueError):
        HexCode(name, hex_code)


@pytest.mark.parametrize(
    "name, hex_code, swatch",
    [
        (
            "white",
            "#FFFFFF",
            "\x1b[48;2;255;255;255m  \x1b[0m\x1b[38;2;255;255;255m white #FFFFFF\x1b[0m",
        ),
        (
            "aegean",
            "#5088C5",
            "\x1b[48;2;80;136;197m  \x1b[0m\x1b[38;2;80;136;197m aegean #5088C5\x1b[0m",
        ),
    ],
)
def test_hexcode_swatch(name, hex_code, swatch):
    assert HexCode(name, hex_code).swatch() == swatch


@pytest.mark.parametrize(
    "name, hex_code, swatch",
    [
        (
            "white",
            "#FFFFFF",
            "\x1b[48;2;255;255;255m  \x1b[0m\x1b[38;2;255;255;255m white #FFFFFF\x1b[0m",
        ),
        (
            "aegean",
            "#5088C5",
            "\x1b[48;2;80;136;197m  \x1b[0m\x1b[38;2;80;136;197m aegean #5088C5\x1b[0m",
        ),
    ],
)
def test_hexcode_repr(name, hex_code, swatch):
    assert HexCode(name, hex_code).__repr__() == swatch


@pytest.mark.parametrize(
    "name, hex_code, width, min_name_width, swatch",
    [
        (
            "white",
            "#FFFFFF",
            2,
            None,
            "\x1b[48;2;255;255;255m  \x1b[0m\x1b[38;2;255;255;255m white #FFFFFF\x1b[0m",
        ),
        (
            "aegean",
            "#5088C5",
            3,
            10,
            "\x1b[48;2;80;136;197m   \x1b[0m\x1b[38;2;80;136;197m aegean     #5088C5\x1b[0m",
        ),
    ],
)
def test_hexcode_swatch_widths(name, hex_code, width, min_name_width, swatch):
    hexcode = HexCode(name, hex_code)
    assert hexcode.swatch(width, min_name_width) == swatch


@pytest.mark.parametrize(
    "name, hex_code, rgb",
    [
        ("white", "#FFFFFF", [255, 255, 255]),
        ("aegean", "#5088C5", [80, 136, 197]),
    ],
)
def test_hexcode_to_rgb(name, hex_code, rgb):
    assert HexCode(name, hex_code).to_rgb() == rgb


@pytest.mark.parametrize(
    "name, hex_code",
    [
        ("white", "#FFFFFF"),
        ("aegean", "#5088C5"),
    ],
)
def test_hexcode_string(name, hex_code):
    assert str(HexCode(name, hex_code)) == hex_code
