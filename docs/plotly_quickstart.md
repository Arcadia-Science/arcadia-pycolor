# Quickstart guide for Plotly

This notebook provides a quick introduction to the `arcadia_pycolor` Python package and how to use it to style Plotly plots so that they comply with the Arcadia style guide.

## Install the `arcadia_pycolor` package

The `arcadia_pycolor` package can be installed using pip. In a virtual environment of your choice, run the following command in your terminal:

```bash
pip install arcadia-pycolor
```

The package can then be imported in notebooks or scripts using the following command:

```python
import arcadia_pycolor as apc
```

## Set the default Plotly styles

The package provides a function called `apc.plotly.setup` that sets the default Plotly styles to match the Arcadia style guide. This function only needs to be called once, ideally at the beginning of the notebook or script. The styles it sets will automatically apply to all plots in the notebook or script.

```python
import plotly.express as px
import arcadia_pycolor as apc

# Call the `setup` function once, at the beginning of a notebook or script.
apc.plotly.setup()

# Plotly plots will now use the Arcadia style guide.
fig = px.line(x=[0, 1, 2, 3, 4], y=[3, 1, 4, 1, 5])
fig.show()
```

### A note about the Arcadia fonts

The Arcadia style guide uses the Suisse family of fonts. When `apc.plotly.setup` is called, it automatically configures Plotly to use these fonts. If they are not installed, Plotly will use its default fonts instead.

The Suisse fonts are proprietary. To install them, please refer to [the "brand assets" page](https://www.notion.so/arcadiascience/Brand-assets-ec521e5b599c4a5f88c5fae3a8ac14b7#d1cbc8fc315b4d10a8fd4cc7d9eb8c3f) on Notion for instructions. Please do not share these fonts outside of Arcadia.

## Styling individual plots

Some aspects of the style guide can only be applied to individual plots. The `apc.plotly.style_plot` function can be used to apply these styles to a single plot. This function takes a Plotly `Figure` object as input.

```python
import plotly.express as px
import arcadia_pycolor as apc

apc.plotly.setup()

fig = px.line(x=[0, 1, 2, 3, 4], y=[3, 1, 4, 1, 5])
apc.plotly.style_plot(fig, monospaced_axes="all")
fig.show()
```

The `style_plot` function can be used to customize the styling of the x- and y-axis tick labels:

- `monospaced_axes` sets the tick labels of the x- and/or y-axis to a monospaced font.
- `categorical_axes` adjusts the x- and/or y-axis styles to be more readable when the axis represents a categorical variable.
- `colorbar_exists` tells the function to style the colorbar, if one exists.

## Using Arcadia colors

The Arcadia style guide defines sets of colors called "color palettes" that should be used in all figures. The `arcadia_pycolor` package provides easy access to both individual colors and to pre-defined palettes and gradients.

### Using individual colors

All of the individual named colors listed in the style guide are available as attributes of the main `apc` module. For example, to create a line plot using the color "rose":

```python
import plotly.express as px
import arcadia_pycolor as apc

apc.plotly.setup()

fig = px.line(x=[0, 1, 2, 3, 4], y=[3, 1, 4, 1, 5])
fig.update_traces(line_color=apc.rose)
apc.plotly.style_plot(fig, monospaced_axes="all")
fig.show()
```

To visualize a particular color, simply type it in a Jupyter notebook cell:

```python
apc.aegean
```

When the cell is evaluated, it will output the name and hex code of the color alongside a swatch showing what the color looks like:

![aegean color swatch](images/aegean-swatch.png)

### Using color palettes

Individual colors are organized into groups called "palettes." The palettes themselves have names and are accessible as attributes of the `apc.palettes` module. For example, we can rewrite the previous example to use the first color in the "primary" palette:

```python
fig = px.line(x=[0, 1, 2, 3, 4], y=[3, 1, 4, 1, 5])
fig.update_traces(line_color=apc.apc.palettes.primary[0])
```

To see all of the colors in a palette, evaluate the palette object in a notebook cell:

```python
apc.palettes.primary
```

This outputs a list of color swatches with the names and hex codes of the colors in the palette:

![primary palette swatches](images/primary-palette.png)

### Using color gradients

The Arcadia style guide also defines continuous color gradients that can be used in plots like heatmaps. These gradients are accessible as attributes of the `apc.gradients` module.

To use a gradient in a Plotly plot, you can convert it to a Plotly colorscale using the `to_plotly_colorscale` method. For example, to use the "magma" gradient in a heatmap, check out the [heatmap examples](examples/heatmaps.ipynb).

Just like palettes, gradients can be visualized by evaluating a gradient object in a Jupyter notebook cell:

```python
apc.gradients.blues
```

This outputs a gradient swatch showing the colors in the gradient:

![blues gradient swatch](images/blues-gradient.png)
