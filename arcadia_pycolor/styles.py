import os
import platform
from importlib import resources as impresources
from pathlib import Path

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt

from . import mplstyles

_DARWIN_FONT_FOLDER = "~/Library/Fonts"
_FONT_FILTER = "Suisse"
_MPL_STYLESHEET = impresources.files(mplstyles) / "arcadia_2024.mplstyle"


# Units in inches when dpi is 72
SAVEFIG_PAD = 0.41
FULL_W = (20.8333, 10.6161)
FULL_S = (10.2029, 9.3712)
THREEQ_W = (14.5833, 7.0833)
THREEQ_S = (7.0904, 6.6946)
HALF_S = (10.4167, 9.9928)


def _load_colors():
    return


def _load_gradients():
    return


def _load_fonts(font_folder: str = None):
    if font_folder:
        font_dir = Path(font_folder)
    elif platform.system() == "Darwin":  # Darwin is the system name for macOS
        font_dir = Path(os.path.expanduser(_DARWIN_FONT_FOLDER))
    else:
        print("Unsupported system. Please specify the font folder manually.")
        raise NotImplementedError

    suisse_fonts = [i for i in os.listdir(font_dir) if _FONT_FILTER in i]

    if len(suisse_fonts) == 0:
        print(f"No {_FONT_FILTER} fonts found in {font_folder}.")
        print("Make sure you have fonts installed and try again.")
        raise FileNotFoundError

    for font in suisse_fonts:
        font_path = font_dir / font
        font_manager.fontManager.addfont(font_path)
        font_manager.FontProperties(fname=font_path)


def _load_styles(sheet: str = _MPL_STYLESHEET):
    plt.style.use(sheet)


def mpl_setup(mode: str = "all", font_folder: str = None):
    dispatch = {
        "fonts": lambda: _load_fonts(font_folder),
        "colors": _load_colors,
        "gradients": _load_gradients,
        "styles": _load_styles,
    }

    if mode == "all":
        for func in dispatch.values():
            func()
    elif mode in dispatch:
        dispatch[mode]()
    else:
        print(f"Invalid mode. Please choose from {", ".join(["all"] + dispatch.keys())}.")
