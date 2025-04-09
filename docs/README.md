# Documentation

This directory contains the documentation for the `arcadia_pycolor` package.

## Quickstart guide

If you are new to using the package, we recommend starting with the quickstart guide for [Matplotlib](mpl_quickstart.md) or [Plotly](plotly_quickstart.md). Each provides a quick introduction to `arcadia_pycolor` and how to use it to style plots so that they comply with the Arcadia style guide.

## Detailed documentation

- [color_usage.ipynb](color_usage.ipynb): This notebook explains how to use the built-in color palettes and gradients and how to modify them to create your own custom color palettes and gradients.

- [style_usage.ipynb](style_usage.ipynb): This notebook explains in more detail how the package sets the default styles for Matplotlib and how to use the `style_plot` function to apply the Arcadia style guide to individual plots. It also explains additional features of the `apc.mpl` module, like pre-defined figure sizes and a way to save figures with the correct resolution.

- [color_vision_deficiency_tools.ipynb](color_vision_deficiency_tools.ipynb): This notebook explains how to use the color vision deficiency tools in the package to simulate color vision deficiencies in your plots. These tools are for testing the accessibility of your plots to people with color vision deficiencies. They are primarly intended for expert users and graphic designers.

## Examples

The [examples](examples/) directory contains examples of some common plot types that demonstrate how to use the package to style Matplotlib, Seaborn, and Plotly plots.
