import matplotlib.pyplot as plt

import arcadia_pycolor.colors as colors
import arcadia_pycolor.gradients as gradients
import arcadia_pycolor.palettes as palettes

### Sizing and spacing ###
# Units in inches when dpi is 72

# Padding to get ~30px padding around the figure.
FIGURE_PADDING = 0.41

# Common figure sizes for Arcadia Creative Cloud library templates.
FULL_W = (20.8333, 10.6161)
FULL_S = (10.2029, 9.3712)
THREEQ_W = (14.5833, 7.0833)
THREEQ_S = (7.0904, 6.6946)
HALF_S = (10.4167, 9.9928)

# Dictionary of common figure sizes.
FIGURE_SIZES = {
    "full_w": FULL_W,
    "full_s": FULL_S,
    "threeq_w": THREEQ_W,
    "threeq_s": THREEQ_S,
    "half_s": HALF_S,
}

### Fonts ###
# Font family to look for in the font folder.
FONT_FILTER = "Suisse"

DEFAULT_FONT = "Suisse Int'l"

# Font family to use for monospace fonts.
MONOSPACE_FONT = "Suisse Int'l Mono"


### rcParams ###
ARCADIA_RC_PARAMS = {
    # Fonts
    "font.family": "sans-serif",
    "font.size": 24,
    "font.serif": "Suisse Works",
    "font.sans-serif": "Suisse Int'l",
    "font.monospace": "Suisse Int'l Mono",
    "font.weight": "regular",
    # Figure
    "figure.titlesize": 26,
    "figure.titleweight": "medium",
    "figure.facecolor": colors.parchment,
    "figure.edgecolor": "none",
    "figure.frameon": False,
    "figure.dpi": 72,
    # Axes
    "axes.facecolor": "none",
    "axes.edgecolor": colors.black,
    "axes.linewidth": 1,
    "axes.grid": False,
    "axes.grid.axis": "both",
    "axes.grid.which": "major",
    "axes.prop_cycle": plt.cycler(color=palettes.accent_all_ordered.colors),
    "axes.titlesize": 24,
    "axes.titleweight": "medium",
    "axes.labelsize": 24,
    "axes.labelweight": "medium",
    "axes.labelcolor": colors.black,
    "axes.labelpad": 15,
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
    # Ticks
    "xtick.major.size": 15,
    "xtick.minor.size": 7.5,
    "xtick.major.width": 1,
    "xtick.minor.width": 1,
    "xtick.major.pad": 8,
    "xtick.minor.pad": 8,
    "xtick.color": colors.black,
    "xtick.labelsize": 24,
    "ytick.major.size": 15,
    "ytick.minor.size": 7.5,
    "ytick.major.width": 1,
    "ytick.minor.width": 1,
    "ytick.major.pad": 8,
    "ytick.minor.pad": 8,
    "ytick.color": colors.black,
    "ytick.labelsize": 24,
    # Legend
    "legend.loc": "best",
    "legend.frameon": False,
    "legend.title_fontsize": 26,
    "legend.fontsize": 24,
    "legend.framealpha": 0,
    "legend.borderpad": 0,
    "legend.borderaxespad": 0,
    "legend.facecolor": "none",
    "legend.edgecolor": "none",
    "legend.handlelength": 1,
    "legend.handleheight": 1.2,
    "legend.handletextpad": 0.4,
    # Lines
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
    # Markers
    "markers.fillstyle": "full",
    "pcolor.shading": "auto",
    # Patches
    "patch.linewidth": 0,
    "patch.facecolor": colors.aegean,
    "patch.edgecolor": colors.aegean,
    "patch.force_edgecolor": False,
    "patch.antialiased": True,
    # Saving figures
    "savefig.format": "pdf",
    "savefig.transparent": True,
    "savefig.pad_inches": FIGURE_PADDING,
    "savefig.dpi": 72,
    "pdf.fonttype": 42,
    "pdf.compression": 0,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "svg.image_inline": True,
    # Images
    "image.cmap": f"apc:{gradients.magma.name}",
    "image.aspect": "equal",
    "image.interpolation": "antialiased",
    "image.lut": 256,
    "image.origin": "upper",
    "image.resample": True,
    "image.composite_image": True,
}
