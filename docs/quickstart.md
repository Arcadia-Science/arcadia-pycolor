# Quickstart guide

This notebook provides a quick introduction to the `arcadia_pycolor` package and how to use it to style Matplotlib and seaborn plots so that they comply with the Arcadia style guide.

For detailed documentation about the package and links to example plots, please refer to the [documentation README](docs/README.md).

## Install the `arcadia_pycolor` package
The `arcadia_pycolor` Python package should be installed using pip. If you are using conda environments, make sure you have the correct conda environment activated, then run the following command in your terminal:

```bash
pip install arcadia-pycolor
```

After this, the package can be imported in notebooks or scripts using the following command:

```python
import arcadia_pycolor as apc
```

## Set the default Matplotlib styles

The package provides a function called `apc.mpl.setup` that sets the default Matplotlib styles to match the Arcadia style guide. This function only needs to be called once, ideally at the beginning of the notebook or script. The styles will automatically apply to all plots in a notebook or script.

```python
import matplotlib.pyplot as plt
import seaborn as sns
import arcadia_pycolor as apc

# Call the `setup` function once, at the beginning of the notebook or script.
apc.mpl.setup()

# Matplotlib plots will now use the Arcadia style guide.
plt.plot([3, 1, 4, 1, 5])
plt.show()

# Seaborn plots will also use the Arcadia style guide.
sns.histplot([3, 1, 4, 1, 5])
plt.show()
```

### An aside about fonts
The Arcadia style guide uses the Suisse family of fonts. When `apc.mpl.setup` is called, it automatically configures Matplotlib to use these fonts. If they are not installed, Matplotlib will use its default fonts instead.

The Suisse fonts are proprietary. To install them, please refer to [the brand assets page on notion](https://www.notion.so/arcadiascience/Brand-assets-ec521e5b599c4a5f88c5fae3a8ac14b7#d1cbc8fc315b4d10a8fd4cc7d9eb8c3f) for instruction. Please do not share these fonts outside of Arcadia.

## Styling individual plots

Some aspects of the style guide can only be applied to individual plots. The `apc.mpl.style_plot` function can be used to apply these styles to a single plot. This function takes a Matplotlib `Axes` object as input.

```python
import matplotlib.pyplot as plt
import arcadia_pycolor as apc

apc.mpl.setup()

plt.plot([3, 1, 4, 1, 5])
apc.mpl.style_plot()
plt.show()
```

If an `Axes` object is not passed to `style_plot`, the function will style the current plot (internally, `style_plot` uses `plt.gca()` to get the current `Axes` object).

By default, the `style_plot` function capitalizes the x- and y-axis labels and styles the legend, if one exists. 

It also has a few optional arguments that can be used to customize the styling of the x- and y-axis tick labels:

- `monospaced_axes` sets the tick labels of the x- and/or y-axis to a monospaced font.
- `categorical_axes` adjusts the x- and/or y-axis styles to be more readable when the axis represents a categorical variable.
- `colorbar_exists` tells the function to style the colorbar, if one exists.

Check out [the documentation about styling plots](docs/style_usage.ipynb) for more information.

## Using Arcadia colors

The Arcadia style guide defines sets of colors, called "color palettes", that should be used in all figures. The `arcadia_pycolor` package provides easy access to individual colors by name as well as to pre-defined palettes and gradients. 

### Using individual colors

All of the individual named colors listed in the style guide are available as attributes of the main `apc` module. For example, to make scatter plots with specific named Arcadia colors:

```python
import matplotlib.pyplot as plt
import arcadia_pycolor as apc

plt.plot([1, 2, 3], [4, 5, 6], color=apc.aegean)
plt.plot([1, 2, 3], [4, 6, 8], color=apc.rose)
```

### Using color palettes

Individual colors are organized into groups called "palettes." The palettes themselves have names and are accessible as attributes of the `apc.palettes` module. For example, we can rewrite the previous example to use colors from the "primary" palette:

```python
plt.plot([1, 2, 3], [4, 5, 6], color=apc.palettes.primary.colors[0])
plt.plot([1, 2, 3], [4, 6, 8], color=apc.palettes.primary.colors[1])
```

To view a visual representation of all the colors in a palette, simply `print` the palette object:

```python
print(apc.palettes.primary)
```

This outputs a list of color swatches with the names and hex codes of the colors in the palette.

### Using color gradients

The Arcadia style guide also defines continuous color gradients that can be used in figures. These gradients are accessible as attributes of the `apc.gradients` module. To use a gradient in a Matplotlib or seaborn plot, you can convert it to a Matplotlib colormap using the `to_mpl_cmap` method. For example, to use the "blues" gradient in a heatmap:

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import arcadia_pycolor as apc

data = np.random.rand(10, 10)
sns.heatmap(data, cmap=apc.gradients.blues.to_mpl_cmap())
```

Just like palettes, gradients can be visualized by printing the gradient object:

```python
print(apc.gradients.blues)
```

For much more detail about how to use color palettes and gradients in your figures, please refer to [the documentation about using colors](docs/color_usage.ipynb).
