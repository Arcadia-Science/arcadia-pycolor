import plotly.graph_objects as go
import plotly.io as pio

from arcadia_pycolor.style_defaults import ARCADIA_PLOTLY_TEMPLATE_LAYOUT


def setup() -> None:
    """Loads all Arcadia colors, fonts, styles, and colormaps into Plotly."""
    arcadia_template = go.layout.Template(layout=ARCADIA_PLOTLY_TEMPLATE_LAYOUT)
    pio.templates["arcadia"] = arcadia_template
    pio.templates.default = "arcadia"
