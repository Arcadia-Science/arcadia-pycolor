import sys
from pathlib import Path

import colorir as cl
import matplotlib.pyplot as plt

from .classes import Gradient, Palette
from .functions import reverse_gradient

#######################
## Individual Colors ##
#######################
"""
Each color is provided as a dictionary with the color name and HEX code.
"""

_ALL_COLORS = {
    # Core colors
    "lightgrey": "#EBEDE8",
    "shell": "#EDE0D6",
    "dawn": "#F8F4F1",
    "seafoam": "#F9FCF0",
    "tangerine": "#FFB984",
    "black": "#09090A",
    "charcoal": "#484B50",
    "marineblue": "#8A99AD",
    "forest": "#596F74",
    # Neutral colors
    "zephyr": "#F4FBFF",
    "paleazure": "#F7F9FD",
    "lichen": "#F7FBEF",
    "orchid": "#FFFDF7",
    "buff": "#FFFBF8",
    "bark": "#8F8885",
    "slate": "#43413F",
    "crow": "#292928",
    # Accent colors
    "aegean": "#5088C5",
    "amber": "#F28360",
    "seaweed": "#3B9886",
    "canary": "#F7B846",
    "aster": "#7A77AB",
    "rose": "#F898AE",
    # Light accent colors
    "bluesky": "#C6E7F4",
    "dress": "#F8C5C1",
    "sage": "#B5BEA4",
    "oat": "#F5E4BE",
    "periwinkle": "#DCBFFC",
    "blossom": "#F5CBE4",
    # Accent expanded colors
    "lime": "#97CD78",
    "vitalblue": "#73B5E3",
    # tangerine is included in both Core and Accent
    "chateau": "#BAB0A8",
    "dragon": "#C85152",
    # marineblue is included in both Core and Accent
    # Light accent expanded colors
    "mint": "#D1EADF",
    "wish": "#BABEE0",
    "satin": "#F1E8DA",
    "taupe": "#DAD3C7",
    "mars": "#DA9085",
    "denim": "#B6C8D4",
    # Other Arcadia colors
    "concord": "#341E60",
    "grape": "#5A4596",
    "taffy": "#E87485",
    "brightgrey": "#EAEAEA",
    "paper": "#FCFCFC",
    "redwood": "#52180A",
    "cocoa": "#4D2C03",
    "royal": "#3F2D5C",
    "carmine": "#471122",
    "depths": "#09473E",
    "bluegrass": "#458F99",
    "yucca": "#1E4812",
    "pitaya": "#C74970",
    "soil": "#4D2500",
    "umber": "#A85E28",
    # Other named colors
    "w": "#FFFFFF",
    "r": "#FF0000",
    "g": "#00FF00",
    "b": "#0000FF",
    "c": "#00FFFF",
    "m": "#FF00FF",
    "y": "#FFFF00",
    "k": "#000000",
}

ALL = cl.Palette(**_ALL_COLORS)

# Possibly unwisely programmatically adds color names to namespace.
# This allows for direct access to colors by name.
# For example, apc.aegean will return the color "#5088C5".
_this_module = sys.modules[__name__]
for name, color in ALL._color_dict.items():
    setattr(_this_module, name, color)


def _assemble_palette(color_names: list) -> dict:
    return cl.Palette({name: _ALL_COLORS[name] for name in color_names})


###############################
## Base Palette Dictionaries ##
###############################
"""
These are the dictionaries collecting the basic palettes.
"""

CORE = _assemble_palette(
    [
        "lightgrey",
        "shell",
        "dawn",
        "seafoam",
        "tangerine",
        "black",
        "charcoal",
        "marineblue",
        "forest",
    ]
)

NEUTRAL = _assemble_palette(
    [
        "zephyr",
        "paleazure",
        "lichen",
        "orchid",
        "buff",
        "bark",
        "slate",
        "crow",
    ]
)

ACCENT = _assemble_palette(
    [
        "aegean",
        "amber",
        "seaweed",
        "canary",
        "aster",
        "rose",
    ]
)

LIGHT = _assemble_palette(
    [
        "bluesky",
        "dress",
        "sage",
        "oat",
        "periwinkle",
        "blossom",
    ]
)

ACCENT_EXPANDED = _assemble_palette(
    [
        "lime",
        "vitalblue",
        "tangerine",
        "chateau",
        "dragon",
        "marineblue",
    ]
)

LIGHT_EXPANDED = _assemble_palette(
    [
        "mint",
        "wish",
        "satin",
        "taupe",
        "mars",
        "denim",
    ]
)

OTHER = _assemble_palette(
    [
        "paper",
        "brightgrey",
        "taffy",
        "pitaya",
        "redwood",
        "cocoa",
        "umber",
        "soil",
        "yucca",
        "bluegrass",
        "depths",
        "royal",
        "grape",
        "concord",
    ]
)

#############################
## Aggregated Dictionaries ##
#############################
"""
These are the dictionaries that aggregate different combinations of the basic palettes.
"""
ACCENT_FULL = ACCENT + ACCENT_EXPANDED
LIGHT_FULL = LIGHT + LIGHT_EXPANDED
ACCENT_ALL = ACCENT + ACCENT_EXPANDED + LIGHT + LIGHT_EXPANDED

##########################
## Ordered Dictionaries ##
##########################
"""
These are the dictionaries with specifically-ordered colors.
The order of colors has been chosen to maximize distinguishability.
"""

ACCENT_ORDERED = _assemble_palette(
    [
        "aegean",
        "amber",
        "canary",
        "lime",
        "aster",
        "rose",
        "seaweed",
        "dragon",
        "vitalblue",
        "chateau",
        "marineblue",
        "tangerine",
    ]
)

LIGHT_ORDERED = _assemble_palette(
    [
        "bluesky",
        "dress",
        "oat",
        "sage",
        "periwinkle",
        "denim",
        "taupe",
        "mars",
        "blossom",
        "mint",
        "wish",
        "satin",
    ]
)

ACCENT_ALL_ORDERED = ACCENT_ORDERED | LIGHT_ORDERED

####################################
## Perceptually Uniform Gradients ##
####################################
"""
These gradients are similar to the gradients available for Matplotlib, Seaborn, and Plotly.
They have been modified to use colors that are harmonious with our brand palette.
The colors have also been optimized to be nearly-perceptually uniform based on lightness.
"""

VIRIDIS = {
    "color_dict": _assemble_palette(
        [
            "concord",
            "grape",
            "aegean",
            "lime",
            "y",
        ]
    ),
    "values": [0, 0.23, 0.49, 0.77, 1],
}

MAGMA = {
    "color_dict": _assemble_palette(
        [
            "black",
            "grape",
            "taffy",
            "tangerine",
            "oat",
        ]
    ),
    "values": [0, 0.38, 0.72, 0.9, 1],
}

CIVIDIS = {
    "color_dict": _assemble_palette(
        [
            "crow",
            "forest",
            "canary",
            "satin",
        ]
    ),
    "values": [0, 0.39, 0.85, 1],
}

################################
## Strong Monocolor Gradients ##
################################

REDS = {
    "color_dict": _assemble_palette(
        [
            "redwood",
            "dragon",
            "amber",
            "paper",
        ]
    ),
    "values": [0.0, 0.43, 0.64, 1.0],
}

ORANGES = {
    "color_dict": _assemble_palette(
        [
            "soil",
            "umber",
            "tangerine",
            "paper",
        ]
    ),
    "values": [0.0, 0.38, 0.8, 1.0],
}

YELLOWS = {
    "color_dict": _assemble_palette(
        [
            "cocoa",
            "canary",
            "oat",
            "paper",
        ]
    ),
    "values": [0.0, 0.76, 0.9, 1.0],
}

GREENS = {
    "color_dict": _assemble_palette(
        [
            "yucca",
            "lime",
            "paper",
        ]
    ),
    "values": [0, 0.7, 1],
}

TEALS = {
    "color_dict": _assemble_palette(
        [
            "depths",
            "seaweed",
            "paper",
        ]
    ),
    "values": [0, 0.42, 1],
}

BLUES = {
    "color_dict": _assemble_palette(
        [
            "concord",
            "aegean",
            "vitalblue",
            "paper",
        ]
    ),
    "values": [0, 0.47, 0.66, 1.0],
}

PURPLES = {
    "color_dict": _assemble_palette(
        [
            "royal",
            "aster",
            "wish",
            "paper",
        ]
    ),
    "values": [0, 0.4, 0.74, 1.0],
}

MAGENTAS = {
    "color_dict": _assemble_palette(
        [
            "carmine",
            "pitaya",
            "rose",
            "paper",
        ]
    ),
    "values": [0, 0.44, 0.73, 1],
}

############################
## Weak Bicolor Gradients ##
############################

AEGEANAMBER = {
    "color_dict": _assemble_palette(
        [
            "aegean",
            "paper",
            "amber",
        ]
    ),
    "values": [0, 0.5, 1],
}

ASTERCANARY = {
    "color_dict": _assemble_palette(
        [
            "aster",
            "paper",
            "canary",
        ]
    ),
    "values": [0, 0.5, 1],
}

LIMEROSE = {
    "color_dict": _assemble_palette(
        [
            "lime",
            "paper",
            "rose",
        ]
    ),
    "values": [0, 0.5, 1],
}

SEAWEEDTANGERINE = {
    "color_dict": _assemble_palette(
        [
            "seaweed",
            "paper",
            "tangerine",
        ]
    ),
    "values": [0, 0.5, 1],
}


##############################
## Strong Bicolor Gradients ##
##############################

POPPIES = {
    "color_dict": _assemble_palette(
        [
            "concord",
            "aegean",
            "vitalblue",
            "paper",
            "amber",
            "dragon",
            "redwood",
        ]
    ),
    "values": [0, 0.235, 0.33, 0.5, 0.68, 0.785, 1.0],
}

PANSIES = {
    "color_dict": _assemble_palette(
        [
            "royal",
            "aster",
            "wish",
            "paper",
            "oat",
            "canary",
            "cocoa",
        ]
    ),
    "values": [0, 0.2, 0.37, 0.5, 0.55, 0.62, 1.0],
}

DAHLIAS = {
    "color_dict": _assemble_palette(
        [
            "yucca",
            "lime",
            "paper",
            "rose",
            "pitaya",
            "carmine",
        ]
    ),
    "values": [0, 0.35, 0.5, 0.635, 0.78, 1.0],
}

LILIES = {
    "color_dict": _assemble_palette(
        [
            "depths",
            "seaweed",
            "paper",
            "tangerine",
            "umber",
            "soil",
        ]
    ),
    "values": [0.0, 0.21, 0.5, 0.6, 0.81, 1.0],
}

################
## Collectors ##
################
"""
These dictionary aggregate all other color dictionaries in the package.

They are accessible within the package namespace as:
    arcadia_pycolor.Palette_dicts
    arcadia_pycolor.Gradient_dicts
or, if using the apc alias:
    apc.Palette_dicts
    apc.Gradient_dicts
"""

Palettes = {
    "apc:All": ALL,
    "apc:Core": CORE,
    "apc:Neutral": NEUTRAL,
    "apc:Accent": ACCENT,
    "apc:AccentExpanded": ACCENT_EXPANDED,
    "apc:AccentFull": ACCENT_FULL,
    "apc:AccentOrdered": ACCENT_ORDERED,
    "apc:Light": LIGHT,
    "apc:LightExpanded": LIGHT_EXPANDED,
    "apc:LightFull": LIGHT_FULL,
    "apc:LightOrdered": LIGHT_ORDERED,
    "apc:AccentAll": ACCENT_ALL,
    "apc:AccentAllOrdered": ACCENT_ALL_ORDERED,
    "apc:Other": OTHER,
}

GRADIENT_DICTS = {
    "apc:reds": REDS,
    "apc:oranges": ORANGES,
    "apc:yellows": YELLOWS,
    "apc:greens": GREENS,
    "apc:teals": TEALS,
    "apc:blues": BLUES,
    "apc:purples": PURPLES,
    "apc:magentas": MAGENTAS,
    "apc:viridis": VIRIDIS,
    "apc:magma": MAGMA,
    "apc:cividis": CIVIDIS,
    "apc:aegeanamber": AEGEANAMBER,
    "apc:astercanary": ASTERCANARY,
    "apc:limerose": LIMEROSE,
    "apc:seaweedtangerine": SEAWEEDTANGERINE,
    "apc:poppies": POPPIES,
    "apc:pansies": PANSIES,
    "apc:dahlias": DAHLIAS,
    "apc:lilies": LILIES,
}

# collector for reverse gradients
_GRADIENT_R_DICTS = {}

# generate reverse gradients and add them as dictionary entries
for name, grad in GRADIENT_DICTS.items():
    grad_r_name = name + "_r"
    grad_r = reverse_gradient(grad)
    _GRADIENT_R_DICTS[grad_r_name] = grad_r

GRADIENT_DICTS = GRADIENT_DICTS | _GRADIENT_R_DICTS

#############################################
## Palette and Gradient library generation ##
#############################################

# Collectors for Palette and Gradient objects
Palettes = {}
Gradients = {}

# Register each of the base palettes
for name, color_dict in PALETTE_DICTS.items():
    pal = Palette(name, color_dict)
    Palettes[name] = pal

# Register each of the custom gradients
for name, data in GRADIENT_DICTS.items():
    color_dict = data["color_dict"]
    values = data["values"]
    grad = Gradient(name, color_dict, values)
    Gradients[name] = grad

# Register paper-to-color gradient for each of the colors in the base palette
for color in ALL:
    if color == "paper":
        continue
    name = f"apc:{color}s"
    color_dict = {"apc:paper": ALL["paper"]} | {f"apc:{color}": ALL[color]}
    color_grad = Gradient(name, color_dict)
    Gradients[name] = color_grad

    # add reverse single-color gradients to Gradients dictionary
    name_r = f"{name}_r"
    color_dict_r = {f"apc:{color}": ALL[color]} | {"apc:paper": ALL["paper"]}
    color_grad_r = Gradient(name_r, color_dict_r)
    Gradients[name_r] = color_grad_r

######################################
## Matplotlib registration function ##
######################################


def mpl_setup(mode="all"):
    """
    Register Arcadia's colors from the arcadia_pycolor package for use with matplotlib.

    Args:
        mode (str): defaults to 'all', which does all of the following keywords.
            To use just one of the following, set mode to the corresponding keyword.
        'colors': registers the Arcadia named colors (e.g. 'apc:aegean')
            with matplotlib's named colors.
        'palettes': registers the Palettes as named matplotlib ListedColormaps.
        'gradients': registers the Gradients as named matplotlib LinearSegmentedColormaps.
        'stylesheets': sets the default stylesheet to Arcadia's basic style.
    """
    if mode == "colors" or mode == "all":
        # Register each of the colors in apc:All
        Palettes["apc:All"].mpl_NamedColors_register()

    if mode == "palettes" or mode == "all":
        for pal in Palettes:
            Palettes[pal].mpl_ListedColormap_register()

    if mode == "stylesheets" or mode == "all":
        # find the upstream path to this file
        parent_path = Path(__file__).parent.resolve()
        plt.style.use(parent_path / "mplstyles/arcadia_basic.mplstyle")

    if mode == "gradients" or mode == "all":
        for grad in Gradients:
            # don't duplicate registration of reverse gradients
            if "_r" not in grad:
                Gradients[grad].mpl_LinearSegmentedColormap_register()
