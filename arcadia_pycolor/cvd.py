from typing import Any, Union, cast, overload

import matplotlib as mpl
import numpy as np
from colorspacious import cspace_convert  # type: ignore
from numpy.typing import NDArray

from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.hexcode import HexCode
from arcadia_pycolor.palette import Palette
from arcadia_pycolor.plot import plot_gradient_lightness

CVD_TYPES = {"d": "deuteranomaly", "p": "protanomaly", "t": "tritanomaly"}


def _make_cvd_dict(cvd_type: str, severity: int = 100) -> dict[str, str]:
    """
    Makes a dictionary for colorspacious to simulate color vision deficiency.

    Args:
        cvd_type (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """

    if cvd_type not in CVD_TYPES:
        raise ValueError(
            "Choose 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly."
        )

    clipped_severity = np.clip(severity, 0, 100)

    cvd_space = {"name": "sRGB1+CVD", "cvd_type": CVD_TYPES[cvd_type], "severity": clipped_severity}

    return cvd_space


@overload
def simulate_color(colors: HexCode, cvd_type: str = "d", severity: int = 100) -> HexCode: ...


@overload
def simulate_color(
    colors: list[HexCode], cvd_type: str = "d", severity: int = 100
) -> list[HexCode]: ...


def simulate_color(
    colors: Union[HexCode, list[HexCode]], cvd_type: str = "d", severity: int = 100
) -> Union[HexCode, list[HexCode]]:
    """
    Simulates color vision deficiency for a single HexCode or list of HexCodes.

    Args:
        colors (HexCode or list[HexCode]): colors to simulate color vision deficiency on.
        cvd_type (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_space = _make_cvd_dict(cvd_type=cvd_type, severity=severity)

    if not isinstance(colors, list):
        colors = [colors]

    returned_colors: list[HexCode] = []
    for color in colors:
        rgb_color = color.to_rgb()
        cvd_color_name = f"{color.name}_{cvd_type}"
        cvd_color = cast(NDArray[np.int64], cspace_convert(rgb_color, cvd_space, "sRGB1"))
        cvd_color = np.clip(cvd_color / 255, 0, 1)
        hex_code = mpl.colors.to_hex(cvd_color)  # type: ignore
        cvd_hexcode = HexCode(name=cvd_color_name, hex_code=hex_code)
        returned_colors.append(cvd_hexcode)

    if len(returned_colors) == 1:
        return returned_colors[0]
    return returned_colors


def display_all_color(color: HexCode, severity: int = 100) -> None:
    """
    Display all color vision deficiency types for a single HexCode.

    Args:
        color (HexCode): color to simulate color vision deficiency on.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_colors = [color] + [simulate_color(color, cvd_type, severity) for cvd_type in CVD_TYPES]
    for cvd_color in cvd_colors:
        print(cvd_color.swatch())


def simulate_palette(palette: Palette, cvd_type: str = "d", severity: int = 100) -> Palette:
    """
    Simulates color vision deficiency on a Palette.

    Args:
        palette (Palette): Palette object on which to simulate color vision deficiency.
        cvd_type (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_hex_colors = simulate_color(palette.colors, cvd_type=cvd_type, severity=severity)
    cvd_palette = Palette(f"{palette.name}_{cvd_type}", cvd_hex_colors)

    return cvd_palette


def display_all_palette(palette: Palette, severity: int = 100) -> None:
    """
    Display all color vision deficiency types for a Palette.

    Args:
        palette (Palette): Palette object on which to simulate color vision deficiency.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_palettes = [palette] + [
        simulate_palette(palette, cvd_type, severity) for cvd_type in CVD_TYPES
    ]
    for palette in cvd_palettes:
        print(palette.name)
        print(palette.swatch())


def simulate_gradient(gradient: Gradient, cvd_type: str = "d", severity: int = 100) -> Gradient:
    """
    Simulates color vision deficiency on a Gradient.

    Args:
        gradient (Gradient): the Gradient object to display
        cvd_type (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_hex_colors = simulate_color(gradient.colors, cvd_type=cvd_type, severity=severity)
    cvd_gradient = Gradient(f"{gradient.name}_{cvd_type}", cvd_hex_colors, gradient.values)

    return cvd_gradient


def display_all_gradient(gradient: Gradient, severity: int = 100) -> None:
    """
    Display all color vision deficiency types for a Gradient.

    Args:
        gradient (Gradient): the Gradient object to display
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_gradients = [gradient] + [
        simulate_gradient(gradient, cvd_type, severity) for cvd_type in CVD_TYPES
    ]
    for grad in cvd_gradients:
        print(grad.name)
        print(grad.swatch())


def display_all_gradient_lightness(gradient: Gradient, severity: int = 100, **kwargs: Any) -> None:
    plot_gradient_lightness(
        [gradient] + [simulate_gradient(gradient, cvd_type, severity) for cvd_type in CVD_TYPES],
        **kwargs,
    )
