import pytest

from arcadia_pycolor import Gradient, HexCode


@pytest.mark.parametrize(
    "name, colors, values, hex_codes",
    [
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            [0, 1],
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        ),
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            None,
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        ),
    ],
)
def test_gradient_from_hexcode_list(name, colors, values, hex_codes):
    assert Gradient(name, colors, values).colors == hex_codes


@pytest.mark.parametrize(
    "name, colors, values",
    [
        ("my_gradient", [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")], [0, 2]),
        ("my_gradient", [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")], [-1, 0]),
        ("my_gradient", [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")], [0, 1.1]),
        ("my_gradient", [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")], [0.25, 0.5]),
    ],
)
def test_gradient_from_hexcode_list_invalid_values(name, colors, values):
    with pytest.raises(ValueError):
        Gradient(name, colors, values)


@pytest.mark.parametrize(
    "name, colors, values",
    [
        ("my_gradient", [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")], [0, 0.5, 1]),
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("grey", "#CCCCCC"), HexCode("black", "#000000")],
            [0, 1],
        ),
    ],
)
def test_gradient_from_hexcode_list_invalid_length(name, colors, values):
    with pytest.raises(ValueError):
        Gradient(name, colors, values)


@pytest.mark.parametrize(
    "name, invalid_input",
    [
        ("my_gradient", [HexCode("white", "#FFFFFF"), "black"]),
        ("my_gradient", [HexCode("white", "#FFFFFF"), 123456]),
        ("my_gradient", [HexCode("white", "#FFFFFF"), 0.123456]),
    ],
)
def test_gradient_from_hexcode_list_invalid_input(name, invalid_input):
    with pytest.raises(ValueError):
        Gradient(name, invalid_input)


@pytest.mark.parametrize(
    "name, colors, values, hex_codes",
    [
        (
            "my_gradient",
            {"white": "#FFFFFF", "black": "#000000"},
            [0, 1],
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        )
    ],
)
def test_gradient_from_dict(name, colors, values, hex_codes):
    assert Gradient.from_dict(name, colors, values).colors == hex_codes


@pytest.mark.parametrize(
    "name, colors, values, swatch",
    [
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            [0, 1],
            "\x1b[48;2;255;255;255m \x1b[0m\x1b[48;2;243;243;243m \x1b[0m\x1b[48;2;231;231;231m \x1b[0m\x1b[48;2;219;219;219m \x1b[0m\x1b[48;2;207;207;207m \x1b[0m\x1b[48;2;195;195;195m \x1b[0m\x1b[48;2;182;182;182m \x1b[0m\x1b[48;2;170;170;170m \x1b[0m\x1b[48;2;158;158;158m \x1b[0m\x1b[48;2;146;146;146m \x1b[0m\x1b[48;2;134;134;134m \x1b[0m\x1b[48;2;121;121;121m \x1b[0m\x1b[48;2;109;109;109m \x1b[0m\x1b[48;2;97;97;97m \x1b[0m\x1b[48;2;85;85;85m \x1b[0m\x1b[48;2;73;73;73m \x1b[0m\x1b[48;2;60;60;60m \x1b[0m\x1b[48;2;48;48;48m \x1b[0m\x1b[48;2;36;36;36m \x1b[0m\x1b[48;2;24;24;24m \x1b[0m\x1b[48;2;12;12;12m \x1b[0m",  # noqa: E501
        )
    ],
)
def test_gradient_repr(name, colors, values, swatch):
    assert Gradient(name, colors, values).swatch() == swatch


@pytest.mark.parametrize(
    "name, colors, steps, swatch",
    [
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            5,
            "\x1b[48;2;255;255;255m \x1b[0m\x1b[48;2;204;204;204m \x1b[0m\x1b[48;2;153;153;153m \x1b[0m\x1b[48;2;102;102;102m \x1b[0m\x1b[48;2;51;51;51m \x1b[0m",  # noqa: E501
        )
    ],
)
def test_gradient_swatch_steps(name, colors, steps, swatch):
    assert Gradient(name, colors).swatch(steps) == swatch


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
