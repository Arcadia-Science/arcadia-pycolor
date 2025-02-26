import matplotlib.pyplot as plt

import arcadia_pycolor.colors as colors
import arcadia_pycolor.gradients as gradients
import arcadia_pycolor.palettes as palettes

### SIZING AND SPACING ###

# Units in inches when dpi is 72
BASE_DPI = 72
PRINT_DPI = 300

FIGURE_PADDING_PIXELS = 20
FIGURE_PADDING_INCHES = FIGURE_PADDING_PIXELS / BASE_DPI

# Common figure sizes for Arcadia Creative Cloud library templates.
FULL_WIDE = (13.33333, 5.27777)
FULL_SQUARE = (6.52777, 6.52777)
FLOAT_WIDE = (9.16667, 5.27777)
FLOAT_SQUARE = (4.44444, 4.44444)
HALF_SQUARE = (6.38888, 6.38888)

# Dictionary of common figure sizes.
FIGURE_SIZES: dict[str, tuple[float, float]] = {
    "full_wide": FULL_WIDE,
    "full_square": FULL_SQUARE,
    "float_wide": FLOAT_WIDE,
    "float_square": FLOAT_SQUARE,
    "half_square": HALF_SQUARE,
}

### FONTS ###

# Font family to look for in the font folder.
FONT_FILTER = "Suisse"
DEFAULT_FONT = "Suisse Int'l"

# Base font size for text.
BASE_FONT_SIZE = 15
TITLE_FONT_SIZE = 16

# Font family to use for monospace fonts.
MONOSPACE_FONT = "Suisse Int'l Mono"
MONOSPACE_FONT_SIZE = 14.5

# Specifications for categorical axes.
CATEGORICAL_AXIS_TICKLENGTH = 0
CATEGORICAL_AXIS_TICKPADDING = 10

### LEGEND ###

LEGEND_SEPARATOR_LINEWIDTH = 1.5

### AXES ###

NUMERICAL_AXIS_TICKLENGTH = 5
NUMERICAL_AXIS_TICKPADDING = 5
LINEWEIGHT = 0.75

### MATPLOTLIB RUNTIME CONFIGURATION PARAMETERS ###

ARCADIA_RC_PARAMS = {
    # Fonts.
    "font.family": "sans-serif",
    "font.size": BASE_FONT_SIZE,
    "font.serif": "Suisse Works",
    "font.sans-serif": "Suisse Int'l",
    "font.monospace": "Suisse Int'l Mono",
    "font.weight": "regular",
    # Figure.
    "figure.titlesize": TITLE_FONT_SIZE,
    "figure.titleweight": "medium",
    "figure.facecolor": colors.white,
    "figure.edgecolor": "none",
    "figure.frameon": False,
    "figure.dpi": BASE_DPI,
    # Axes.
    "axes.facecolor": "none",
    "axes.edgecolor": colors.black,
    "axes.linewidth": LINEWEIGHT,
    "axes.grid": False,
    "axes.grid.axis": "both",
    "axes.grid.which": "major",
    "axes.prop_cycle": plt.cycler(color=palettes.all_ordered.colors),  # type: ignore
    "axes.titlesize": TITLE_FONT_SIZE + 2,
    "axes.titleweight": "medium",
    "axes.titlepad": 16,
    "axes.labelsize": BASE_FONT_SIZE,
    "axes.labelweight": "medium",
    "axes.labelcolor": colors.black,
    "axes.labelpad": 10,
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.xmargin": 0.04,
    "axes.ymargin": 0.04,
    "axes.zmargin": 0.04,
    "axes.autolimit_mode": "data",
    "polaraxes.grid": True,
    "axes3d.grid": True,
    # Ticks.
    "xtick.major.size": NUMERICAL_AXIS_TICKLENGTH,
    "xtick.minor.size": NUMERICAL_AXIS_TICKLENGTH / 2,
    "xtick.major.width": LINEWEIGHT,
    "xtick.minor.width": LINEWEIGHT,
    "xtick.major.pad": NUMERICAL_AXIS_TICKPADDING,
    "xtick.minor.pad": NUMERICAL_AXIS_TICKPADDING,
    "xtick.color": colors.black,
    "xtick.labelsize": BASE_FONT_SIZE,
    "ytick.major.size": NUMERICAL_AXIS_TICKLENGTH,
    "ytick.minor.size": NUMERICAL_AXIS_TICKLENGTH / 2,
    "ytick.major.width": LINEWEIGHT,
    "ytick.minor.width": LINEWEIGHT,
    "ytick.major.pad": NUMERICAL_AXIS_TICKPADDING,
    "ytick.minor.pad": NUMERICAL_AXIS_TICKPADDING,
    "ytick.color": colors.black,
    "ytick.labelsize": BASE_FONT_SIZE,
    # Legend.
    "legend.loc": "best",
    "legend.frameon": False,
    "legend.title_fontsize": TITLE_FONT_SIZE,
    "legend.fontsize": BASE_FONT_SIZE,
    "legend.framealpha": 0,
    "legend.borderpad": 0,
    "legend.borderaxespad": 0,
    "legend.facecolor": "none",
    "legend.edgecolor": "none",
    "legend.handlelength": 1,
    "legend.handleheight": 1.2,
    "legend.handletextpad": 0.4,
    # Lines.
    "lines.linewidth": 2,
    "lines.linestyle": "-",
    "lines.color": colors.aegean,
    "lines.marker": "none",
    "lines.markerfacecolor": "auto",
    "lines.markeredgecolor": "auto",
    "lines.markeredgewidth": 0,
    "lines.markersize": 6,
    "lines.antialiased": True,
    "lines.dash_joinstyle": "round",
    "lines.dash_capstyle": "butt",
    "lines.solid_joinstyle": "round",
    "lines.solid_capstyle": "round",
    # Markers.
    "markers.fillstyle": "full",
    "pcolor.shading": "auto",
    # Patches.
    "patch.linewidth": 0,  # Removes edge on patches.
    "patch.facecolor": colors.aegean,
    "patch.edgecolor": colors.aegean,
    "patch.force_edgecolor": False,
    "patch.antialiased": True,
    # Saving figures.
    "savefig.format": "pdf",
    "savefig.transparent": True,
    "savefig.pad_inches": FIGURE_PADDING_INCHES,
    "savefig.dpi": BASE_DPI,
    "pdf.fonttype": 42,
    "pdf.compression": 0,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "svg.image_inline": True,
    # Images.
    "image.cmap": f"apc:{gradients.magma.name}",
    "image.aspect": "equal",
    "image.interpolation": "antialiased",
    "image.lut": 256,
    "image.origin": "upper",
    "image.resample": True,
    "image.composite_image": True,
}
