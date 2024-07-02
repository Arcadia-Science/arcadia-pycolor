import pytest

from arcadia_pycolor import HexCode
from arcadia_pycolor.hexcode import _is_hex_code

VALID_HEXCODES = [
    "#FFFFFF",
    "#FFFFFF",
    "#FFF",
    "#fff",
    "#001",
    "#000",
    "#000000",
    "#000001",
    "#FfFfFf",
    "#f90",
    "#ff9900",
    "#f0a2c3",
]

INVALID_HEXCODES = [
    "#ZZZZZZ",
    "#ZZZ",
    "#FF",
    "apples",
    "123456",
    "ffffff",
    "white",
    "",
    "#",
    "0",
    "F",
    0,
    0.5,
    None,
    "#0000",
]


@pytest.mark.parametrize(
    "hex_string, is_hex_code",
    [(hc, True) for hc in VALID_HEXCODES] + [(hc, False) for hc in INVALID_HEXCODES],
)
def test_is_hex_code(hex_string, is_hex_code):
    assert _is_hex_code(hex_string) == is_hex_code


@pytest.mark.parametrize(
    "hex_code",
    VALID_HEXCODES,
)
def test_valid_hexcode(hex_code):
    assert HexCode("a_hexcode", hex_code) == hex_code


@pytest.mark.parametrize(
    "hex_code",
    INVALID_HEXCODES,
)
def test_invalid_hexcode(hex_code):
    with pytest.raises((ValueError, TypeError)):
        HexCode("a_hexcode", hex_code)


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
        ("near-white", "#FFFFFE", [255, 255, 254]),
        ("near-black", "#000001", [0, 0, 1]),
        ("darkbrownish", "#001", [0, 0, 17]),
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
