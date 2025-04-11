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


def test_palette_add():
    p1 = [HexCode("white", "#FFFFFF")]
    p2 = [HexCode("black", "#000000")]
    result = p1 + p2
    assert (Palette("p1", p1) + Palette("p2", p2)).colors == result
    assert (Palette("p1", p1) + Palette("p2", p2)).name == "p1+p2"


def test_palette_length():
    """Test that a Palette has the expected length."""
    palette = Palette("test_palette", [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")])
    assert len(palette) == 2


def test_palette_iteration():
    """Test that a Palette can be iterated over."""
    colors = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    palette = Palette("test_palette", colors)

    for i, color in enumerate(palette):
        assert color == colors[i]

    assert [color for color in palette] == ["#FFFFFF", "#000000"]


def test_palette_indexing():
    """Test that a Palette can be indexed."""
    colors = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    palette = Palette("test_palette", colors)

    assert palette[0] == colors[0]
    assert palette[1] == colors[1]

    assert palette[-1] == colors[-1]

    with pytest.raises(IndexError):
        palette[2]


def test_palette_slicing():
    """Test that a Palette can be sliced."""
    colors = [HexCode("white", "#FFFFFF"), HexCode("gray", "#CCCCCC"), HexCode("black", "#000000")]
    palette = Palette("test_palette", colors)

    sliced = palette[0:2]
    assert isinstance(sliced, Palette)
    assert sliced.name == "test_palette_slice"
    assert len(sliced) == 2
    assert sliced.colors == colors[0:2]

    sliced = palette[-2:]
    assert len(sliced) == 2
    assert sliced.colors == colors[-2:]

    sliced = palette[::2]
    assert len(sliced) == 2
    assert sliced.colors == [colors[0], colors[2]]

    palette = Palette("test", colors)
    assert palette.reverse().colors == palette[::-1].colors
