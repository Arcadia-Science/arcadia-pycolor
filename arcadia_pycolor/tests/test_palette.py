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
def test_palette_from_hexcode_list(name, input, hex_codes):
    assert Palette(name, input).colors == hex_codes


@pytest.mark.parametrize(
    "name, invalid_input",
    [
        ("my_palette", [HexCode("white", "#FFFFFF"), "black"]),
        ("my_palette", [HexCode("white", "#FFFFFF"), 123456]),
        ("my_palette", [HexCode("white", "#FFFFFF"), 0.123456]),
    ],
)
def test_palette_from_hexcode_list_invalid_input(name, invalid_input):
    with pytest.raises(ValueError):
        Palette(name, invalid_input)


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


@pytest.mark.parametrize(
    "name, input, swatch",
    [
        (
            "my_palette",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            "\x1b[48;2;255;255;255m  \x1b[0m\x1b[38;2;255;255;255m white #FFFFFF\x1b[0m"
            + "\n\x1b[48;2;0;0;0m  \x1b[0m\x1b[38;2;0;0;0m black #000000\x1b[0m",
        )
    ],
)
def test_palette_repr(name, input, swatch):
    assert Palette(name, input).__repr__() == swatch


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


@pytest.mark.parametrize(
    "name, input, other, result",
    [
        (
            "my_palette",
            [HexCode("white", "#FFFFFF")],
            [HexCode("black", "#000000")],
            [
                HexCode("white", "#FFFFFF"),
                HexCode("black", "#000000"),
            ],
        )
    ],
)
def test_palette_add(name, input, other, result):
    assert (Palette(name, input) + Palette(name, other)).colors == result
