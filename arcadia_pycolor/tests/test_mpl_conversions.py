import pytest

from arcadia_pycolor import Gradient, HexCode, Palette


def test_palette_to_cmap():
    hex_codes = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    assert Palette("my_palette", hex_codes).to_mpl_cmap().colors == hex_codes  # type: ignore


def test_palette_name():
    hex_codes = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    assert (
        Palette.from_dict("my_palette", {"white": "#FFFFFF", "black": "#000000"})
        .to_mpl_cmap()
        .colors  # type: ignore
        == hex_codes
    )


@pytest.mark.parametrize(
    "values",
    [
        [0, 1],
        None,
    ],
)
def test_gradient_to_linear_cmap(values):
    grad = Gradient(
        "my_gradient",
        [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        values,
    ).to_mpl_cmap()
    assert grad(0) == (1.0, 1.0, 1.0, 1.0)


@pytest.mark.parametrize(
    "values",
    [
        [0, 1],
        None,
    ],
)
def test_gradient_name(values):
    name = "my_gradient"
    grad = Gradient(
        name,
        [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        values,
    ).to_mpl_cmap()
    assert grad.name == name
