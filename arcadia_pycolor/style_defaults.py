from textwrap import dedent
from typing import Literal

import matplotlib.pyplot as plt
import plotly.graph_objects as go

import arcadia_pycolor.colors as colors
import arcadia_pycolor.gradients as gradients
import arcadia_pycolor.palettes as palettes

# Units in inches when dpi is 72
BASE_DPI = 72
PRINT_DPI = 300

FIGURE_PADDING_PIXELS = 30
FIGURE_PADDING_INCHES = FIGURE_PADDING_PIXELS / BASE_DPI

# Common figure sizes for Arcadia Creative Cloud library templates.
FigureSize = Literal["full_wide", "float_wide", "half_square"]

# This dictionary contains figure sizes in inches WITHOUT padding for the transparent border.
# For example, the "full_wide" figure width is 13.33333333 inches, or 940 pixels at 72 DPI.
# They are used to set dimensions for matplotlib figures.
FIGURE_SIZES_IN_INCHES: dict[FigureSize, tuple[float, float]] = {
    "full_wide": (13.0555555556, 5.27777777),
    "float_wide": (8.19444444444, 5.27777777),
    "half_square": (5.97222222222, 5.97222222222),
}

# This dictionary contains full figure sizes in pixels WITH padding for the transparent border.
# For example, the "full_wide" figure width is 940 pixels plus 30 pixels of padding on each side.
# They are used to set dimensions for Plotly figures.
FIGURE_SIZES_IN_PIXELS: dict[FigureSize, tuple[int, int]] = {
    "full_wide": (1000, 420),
    "float_wide": (650, 420),
    "half_square": (490, 490),
}

# Font families.
FONT_FILTER = "Atkinson"
DEFAULT_FONT = "Atkinson Hyperlegible Next"
MONOSPACE_FONT = "Atkinson Hyperlegible Mono"

DEFAULT_FONT_PLOTLY = "AtkinsonHyperlegibleNext"
MONOSPACE_FONT_PLOTLY = "AtkinsonHyperlegibleMono"

# Font sizes.
TITLE_FONT_SIZE = 17  # Key title, legend title
AXIS_TITLE_FONT_SIZE = 15
BASE_FONT_SIZE = 15  # Axis label, key label, explanatory text
MONOSPACE_FONT_SIZE = 14.5  # Numbers

# Specifications for categorical axes.
CATEGORICAL_AXIS_TICKLENGTH = 0
CATEGORICAL_AXIS_TICKPADDING = 10

# Legend.
LEGEND_SEPARATOR_LINEWIDTH = 1.5

# Axes.
NUMERICAL_AXIS_TICKLENGTH = 5
NUMERICAL_AXIS_TICKPADDING = 5
LINEWEIGHT = 0.75

# Matplotlib runtime configuration parameters.
# API reference: https://matplotlib.org/stable/api/matplotlib_configuration_api.html.
ARCADIA_MATPLOTLIB_RC_PARAMS = {
    # Fonts.
    "font.family": "sans-serif",
    "font.size": BASE_FONT_SIZE,
    "font.sans-serif": "Atkinson Hyperlegible Next",
    "font.monospace": "Atkinson Hyperlegible Mono",
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
    "axes.titlesize": AXIS_TITLE_FONT_SIZE,
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

# Plotly template layout.
# API reference: https://plotly.com/python-api-reference/generated/plotly.graph_objects.layout.html.
PLOTLY_3D_AXIS_ATTRIBUTES = dict(
    linecolor="black",
    linewidth=1,
    showgrid=True,
    showline=True,
    ticks="outside",
    tickwidth=1,
    title=dict(
        font=dict(family=f"{DEFAULT_FONT_PLOTLY}-Medium", size=BASE_FONT_SIZE, color="black"),
    ),
)

ARCADIA_PLOTLY_TEMPLATE_LAYOUT = go.Layout(
    bargap=0.20,
    coloraxis=go.layout.Coloraxis(
        colorbar=go.layout.coloraxis.ColorBar(
            outlinecolor="white",
            thickness=15,
            ticks="outside",
            tickfont=dict(family=MONOSPACE_FONT_PLOTLY, size=MONOSPACE_FONT_SIZE),
            title=dict(
                font=dict(family=f"{DEFAULT_FONT_PLOTLY}-Medium", size=BASE_FONT_SIZE),
                side="right",
            ),
        ),
    ),
    colorscale=go.layout.Colorscale(
        sequential=gradients.magma.to_plotly_colorscale(),
        sequentialminus=gradients.magma.reverse().to_plotly_colorscale(),
        diverging=gradients.orange_sage.to_plotly_colorscale(),
    ),
    font=go.layout.Font(family=DEFAULT_FONT_PLOTLY, size=BASE_FONT_SIZE, color="black"),
    hoverlabel=go.layout.Hoverlabel(
        font_family=DEFAULT_FONT_PLOTLY,
        font_size=13,
    ),
    legend=go.layout.Legend(
        title=dict(
            font=dict(family=f"{DEFAULT_FONT_PLOTLY}-SemiBold", size=TITLE_FONT_SIZE, color="black")
        ),
        font=dict(family=DEFAULT_FONT_PLOTLY, size=BASE_FONT_SIZE, color="black"),
        indentation=-12,
        xanchor="right",
        x=1,
        yanchor="top",
        y=1,
    ),
    margin=go.layout.Margin(
        l=FIGURE_PADDING_PIXELS + 75,
        b=FIGURE_PADDING_PIXELS + 65,
        r=FIGURE_PADDING_PIXELS + 20,
        t=FIGURE_PADDING_PIXELS + 20,
    ),
    scene=go.layout.Scene(
        xaxis=go.layout.scene.XAxis(**PLOTLY_3D_AXIS_ATTRIBUTES),
        yaxis=go.layout.scene.YAxis(**PLOTLY_3D_AXIS_ATTRIBUTES),
        zaxis=go.layout.scene.ZAxis(**PLOTLY_3D_AXIS_ATTRIBUTES),
    ),
    title=go.layout.Title(
        font=dict(family=f"{DEFAULT_FONT_PLOTLY}-SemiBold", size=TITLE_FONT_SIZE, color="black"),
        automargin=True,
        yref="container",
    ),
    xaxis=go.layout.XAxis(
        automargin=True,
        linecolor="black",
        linewidth=1,
        showgrid=False,
        showline=True,
        ticklabelstandoff=2,
        ticks="outside",
        tickwidth=1,
        title=dict(
            font=dict(family=f"{DEFAULT_FONT_PLOTLY}-Medium", size=BASE_FONT_SIZE, color="black"),
            standoff=10,
        ),
        zerolinecolor="rgba(0,0,0,0)",
        zerolinewidth=0,
    ),
    yaxis=go.layout.YAxis(
        automargin=True,
        linecolor="black",
        linewidth=1,
        showgrid=False,
        showline=True,
        ticklabelstandoff=2,
        ticks="outside",
        tickwidth=1,
        title=dict(
            font=dict(family=f"{DEFAULT_FONT_PLOTLY}-Medium", size=BASE_FONT_SIZE, color="black"),
            standoff=10,
        ),
        zerolinecolor="rgba(0,0,0,0)",
        zerolinewidth=0,
    ),
)

PLOTLY_HTML_EXPORT_CSS = dedent(
    """
    @font-face {
      font-family: "AtkinsonHyperlegibleNext";
      src: url("https://fonts.gstatic.com/s/atkinsonhyperlegiblenext/v7/NaP4cYPdHfdVxJw0IfIP0lvYFqijb-UxCtm5_wdGscKFt4tOOfV4ZmW37LQhtA.ttf")
        format("truetype");
      font-weight: normal;
      font-style: normal;
    }

    @font-face {
      font-family: "AtkinsonHyperlegibleNext-Medium";
      src: url("https://fonts.gstatic.com/s/atkinsonhyperlegiblenext/v7/NaP4cYPdHfdVxJw0IfIP0lvYFqijb-UxCtm5_wdGscKFt4tOOfV4ZmW33rQhtA.ttf")
        format("truetype");
      font-weight: normal;
      font-style: normal;
    }

    @font-face {
      font-family: "AtkinsonHyperlegibleNext-SemiBold";
      src: url("https://fonts.gstatic.com/s/atkinsonhyperlegiblenext/v7/NaP4cYPdHfdVxJw0IfIP0lvYFqijb-UxCtm5_wdGscKFt4tOOfV4ZmW3MrMhtA.ttf")
        format("truetype");
      font-weight: normal;
      font-style: normal;
    }

    @font-face {
      font-family: "AtkinsonHyperlegibleMono";
      src: url("https://fonts.gstatic.com/s/atkinsonhyperlegiblemono/v8/tssNAoFBci4C4gvhPXrt3wjT1MqSzhA4t7IIcncBiyihrK15gZ4k_SaZHNeiDQ.ttf")
        format("truetype");
      font-weight: normal;
      font-style: normal;
    }
    """
)
