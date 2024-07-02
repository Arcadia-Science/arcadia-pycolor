import numpy as np
import pytest

from arcadia_pycolor import Gradient, HexCode

from .test_hexcode import INVALID_HEXCODES


@pytest.mark.parametrize(
    "values",
    [
        [0, 1],
        None,
    ],
)
def test_gradient_from_hexcode_list(values):
    colors = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    assert Gradient("some-gradient", colors, values).colors == colors


@pytest.mark.parametrize(
    "values",
    [
        [0, 2],
        [-1, 0],
        [0, 1.1],
        [0.25, 0.5],
        [],
        [0],
        [1],
        [np.nan],
        [None],
        ["0", "1"],
    ],
)
def test_gradient_from_hexcode_list_invalid_values(values):
    with pytest.raises(ValueError):
        Gradient("gradient", [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")], values)


@pytest.mark.parametrize(
    "colors, values",
    [
        (
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            [0, 0.5, 1],
        ),
        (
            [HexCode("white", "#FFFFFF"), HexCode("gray", "#CCCCCC"), HexCode("black", "#000000")],
            [0, 1],
        ),
    ],
)
def test_gradient_from_hexcode_list_with_wrong_number_of_values(colors, values):
    with pytest.raises(ValueError):
        Gradient("some_gradient", colors, values)


@pytest.mark.parametrize(
    "invalid_color",
    INVALID_HEXCODES,
)
def test_gradient_from_hexcode_list_invalid_input(invalid_color):
    with pytest.raises(ValueError):
        Gradient("some-gradient", [HexCode("black", "#000000"), invalid_color], [0, 1])


@pytest.mark.parametrize(
    "values",
    [
        [0, 1],
        None,
    ],
)
def test_gradient_from_dict(values):
    assert Gradient.from_dict(
        "some_gradient",
        {"white": "#FFFFFF", "black": "#000000"},
        values,
    ).colors == [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]


def test_gradient_swatch():
    expected_swatch = "\x1b[48;2;255;255;255m \x1b[0m\x1b[48;2;243;243;243m \x1b[0m\x1b[48;2;231;231;231m \x1b[0m\x1b[48;2;219;219;219m \x1b[0m\x1b[48;2;207;207;207m \x1b[0m\x1b[48;2;195;195;195m \x1b[0m\x1b[48;2;182;182;182m \x1b[0m\x1b[48;2;170;170;170m \x1b[0m\x1b[48;2;158;158;158m \x1b[0m\x1b[48;2;146;146;146m \x1b[0m\x1b[48;2;134;134;134m \x1b[0m\x1b[48;2;121;121;121m \x1b[0m\x1b[48;2;109;109;109m \x1b[0m\x1b[48;2;97;97;97m \x1b[0m\x1b[48;2;85;85;85m \x1b[0m\x1b[48;2;73;73;73m \x1b[0m\x1b[48;2;60;60;60m \x1b[0m\x1b[48;2;48;48;48m \x1b[0m\x1b[48;2;36;36;36m \x1b[0m\x1b[48;2;24;24;24m \x1b[0m\x1b[48;2;12;12;12m \x1b[0m"  # noqa: E501

    assert (
        Gradient(
            "some_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            [0, 1],
        ).swatch()
        == expected_swatch
    )


def test_gradient_swatch_steps():
    expected_swatch = "\x1b[48;2;255;255;255m \x1b[0m\x1b[48;2;204;204;204m \x1b[0m\x1b[48;2;153;153;153m \x1b[0m\x1b[48;2;102;102;102m \x1b[0m\x1b[48;2;51;51;51m \x1b[0m"  # noqa: E501
    assert (
        Gradient(
            "some_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        ).swatch(5)
        == expected_swatch
    )


@pytest.mark.parametrize(
    "name, colors, swatch",
    [
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            "\x1b[48;2;255;255;255m \x1b[0m\x1b[48;2;243;243;243m \x1b[0m\x1b[48;2;231;231;231m \x1b[0m\x1b[48;2;219;219;219m \x1b[0m\x1b[48;2;207;207;207m \x1b[0m\x1b[48;2;195;195;195m \x1b[0m\x1b[48;2;182;182;182m \x1b[0m\x1b[48;2;170;170;170m \x1b[0m\x1b[48;2;158;158;158m \x1b[0m\x1b[48;2;146;146;146m \x1b[0m\x1b[48;2;134;134;134m \x1b[0m\x1b[48;2;121;121;121m \x1b[0m\x1b[48;2;109;109;109m \x1b[0m\x1b[48;2;97;97;97m \x1b[0m\x1b[48;2;85;85;85m \x1b[0m\x1b[48;2;73;73;73m \x1b[0m\x1b[48;2;60;60;60m \x1b[0m\x1b[48;2;48;48;48m \x1b[0m\x1b[48;2;36;36;36m \x1b[0m\x1b[48;2;24;24;24m \x1b[0m\x1b[48;2;12;12;12m \x1b[0m\n\x1b[48;2;255;255;255m  \x1b[0m\x1b[38;2;255;255;255m white #FFFFFF\x1b[0m 0.0\n\x1b[48;2;0;0;0m  \x1b[0m\x1b[38;2;0;0;0m black #000000\x1b[0m 1.0",  # noqa: E501
        )
    ],
)
def test_gradient_swatch_repr(name, colors, swatch):
    assert Gradient(name, colors).__repr__() == swatch
