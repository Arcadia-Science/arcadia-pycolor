import matplotlib as mpl
import numpy as np
from colorspacious import cspace_convert

from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.hexcode import HexCode
from arcadia_pycolor.palette import Palette
from arcadia_pycolor.plot import plot_gradient_lightness


def _make_cvd_dict(form: str, severity: int = 100) -> dict:
    """
    Makes a dictionary for colorspacious to simulate color vision deficiency.

    Args:
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    forms = {"d": "deuteranomaly", "p": "protanomaly", "t": "tritanomaly"}

    if form not in forms:
        raise ValueError(
            "Choose 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly."
        )

    sev = np.clip(severity, 0, 100)

    # define a cvd space
    cvd_space = {"name": "sRGB1+CVD", "cvd_type": forms[form], "severity": sev}

    return cvd_space


def simulate_color(color: HexCode, form="d", severity=100) -> HexCode:
    """
    Simulates color vision deficiency on a single color.

    Args:
        color (HexCode): color to simulate color vision deficiency on.
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_space = _make_cvd_dict(form=form, severity=severity)
    rgb_color = color.to_rgb()

    cvd_color_name = f"{color.name}_{form}"
    cvd_rgb_color = np.clip(cspace_convert(rgb_color, cvd_space, "sRGB1"), 0, 255)
    cvd_rgb_color = np.clip(cvd_rgb_color / 255, 0, 1)
    cvd_hexcode = HexCode(name=cvd_color_name, hex_code=mpl.colors.to_hex(cvd_rgb_color))

    return cvd_hexcode


def simulate_color_all(color: HexCode, severity=100):
    """
    Simulates color vision deficiency on a single color.

    Args:
        color (HexCode): color to simulate color vision deficiency on.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_colors = [color] + [simulate_color(color, form, severity) for form in ["d", "p", "t"]]
    for cvd_color in cvd_colors:
        print(cvd_color.swatch())


def simulate_colors(colors: list[HexCode], form="d", severity=100) -> list:
    """
    Simulates color vision deficiency on a list of colors.

    Args:
        colors (list): list of colors to simulate color vision deficiency on.
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_hex_colors = [simulate_color(color, form=form, severity=severity) for color in colors]

    return cvd_hex_colors


def simulate_palette(palette: Palette, form="d", severity=100) -> list:
    """
    Simulates color vision deficiency on a list of colors.

    Args:
        colors (list): list of colors to simulate color vision deficiency on.
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_hex_colors = simulate_colors(palette.colors, form=form, severity=severity)
    cvd_palette = Palette(f"{palette.name}_{form}", cvd_hex_colors)

    return cvd_palette


def simulate_palette_all(palette: Palette, severity=100):
    """
    Simulates color vision deficiency on a list of colors.

    Args:
        colors (list): list of colors to simulate color vision deficiency on.
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_palettes = [palette] + [
        simulate_palette(palette, form, severity) for form in ["d", "p", "t"]
    ]
    for palette in cvd_palettes:
        print(palette.name)
        print(palette.swatch())


def simulate_gradient(gradient: Gradient, form="d", severity=100):
    """
    Simulates color vision deficiency on a gradient.

    Args:
        gradient (Gradient): the Gradient object to display
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_hex_colors = simulate_colors(gradient.colors, form=form, severity=severity)
    cvd_gradient = Gradient(f"{gradient.name}_{form}", cvd_hex_colors, gradient.values)

    return cvd_gradient


def simulate_gradient_all(gradient: Gradient, severity=100):
    """
    Simulates color vision deficiency on a gradient.

    Args:
        gradient (Gradient): the Gradient object to display
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_gradients = [gradient] + [
        simulate_gradient(gradient, form, severity) for form in ["d", "p", "t"]
    ]
    for grad in cvd_gradients:
        print(grad.name)
        print(grad.swatch())


def simulate_gradient_lightness(gradient: Gradient, severity: int = 100, **kwargs):
    plot_gradient_lightness(
        [gradient] + [simulate_gradient(gradient, form, severity) for form in ["d", "p", "t"]],
        **kwargs,
    )
