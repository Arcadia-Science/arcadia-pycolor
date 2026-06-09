---
name: arcadia-pycolor
description: >-
  Style Matplotlib, seaborn, and Plotly figures to comply with Arcadia Science's
  visual style guide using the arcadia_pycolor (imported as apc) package. Use
  when creating, styling, theming, recoloring, or exporting scientific figures,
  charts, or plots in a Python project that imports arcadia_pycolor / apc, or
  whenever the user wants Arcadia-branded colors, palettes, gradients, fonts
  (Atkinson Hyperlegible), or panel sizes for figures — including requests like
  "make this plot match Arcadia style", "use the Arcadia color palette", "apply
  apc styling", or "save this figure for print/web", even if the package is not
  named explicitly. Covers apc.mpl.setup/style_plot/save_figure, the apc.plotly
  equivalents, named colors (apc.aegean), palettes, gradients/colormaps
  ("apc:..."), and color-vision-deficiency checks.
metadata:
  source: arcadia-pycolor (Arcadia Science)
  style-guide: 2026 Arcadia Style Guide
---

# arcadia-pycolor (apc)

`arcadia_pycolor` styles **Matplotlib**, **seaborn**, and **Plotly** figures to match Arcadia's style guide. Always import as `apc`:

```python
import arcadia_pycolor as apc
```

If the package isn't installed: `pip install arcadia-pycolor` (requires `matplotlib>=3.7,!=3.8.0`, `plotly>=6`, Python `>=3.9`).

## The core workflow

Three steps, in this order. Steps 2 and 3 are the ones that are easy to forget.

1. **`apc.<backend>.setup()` once** per script/notebook, before plotting. Loads fonts, colors, gradients/colormaps, and the global theme.
2. **Plot normally** using Arcadia colors/palettes/gradients (see below).
3. **`apc.<backend>.style_plot(...)` per Axes/Figure**, *after* plotting, to apply the styles that can only be set on an individual plot (label capitalization, legend styling, monospaced numeric ticks, categorical axes).
4. **`apc.<backend>.save_figure(...)`** to export at an Arcadia panel size.

`<backend>` is `mpl` (Matplotlib/seaborn) or `plotly`.

### Matplotlib / seaborn

```python
import matplotlib.pyplot as plt
import arcadia_pycolor as apc

apc.mpl.setup()                          # once, at the top

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6], color=apc.aegean)
ax.set_xlabel("time")                    # lowercase is fine; style_plot capitalizes it
ax.set_ylabel("signal")

apc.mpl.style_plot(ax, monospaced_axes="both")   # numeric axes -> monospaced font
apc.mpl.save_figure("fig1", size="float", filetypes=["pdf", "svg"])
```

### Plotly

```python
import plotly.express as px
import arcadia_pycolor as apc

apc.plotly.setup()                       # once, at the top

fig = px.line(x=[0, 1, 2, 3], y=[3, 1, 4, 1])
fig.update_traces(line_color=apc.rose)
apc.plotly.style_plot(fig, monospaced_axes="all")
apc.plotly.save_figure(fig, "fig1.pdf", size="float")
```

## Colors

Every named color is an attribute of the top-level module and is a `HexCode` (a `str` subclass), so pass it directly anywhere a color is expected:

```python
apc.aegean          # "#5088C5"  — primary blue
ax.scatter(x, y, color=apc.amber)
```

- **Primary / secondary** colors → data and illustrated elements.
- **Neutrals** (e.g. `apc.gray`, `apc.charcoal`) → supporting elements.
- **Text** should only be `apc.black`, `apc.white`, or `apc.charcoal`.

Display a color in a notebook by evaluating it (`apc.aegean`) to see a swatch. Full named-color list: [references/colors.md](references/colors.md).

## Palettes

Ordered groups of colors in `apc.palettes`. Index, slice, iterate, and concatenate them:

```python
apc.palettes.primary[0]          # first color (a HexCode)
apc.palettes.primary[:3]         # a new Palette
for c in apc.palettes.secondary: ...
```

Pick the palette that matches the *number of categories* and intent (the style guide's suggested combinations). Common choices: `primary`, `secondary`, `primary_ordered`, `all_ordered` (the default Matplotlib color cycle after `setup()`), and the monochromatic `*_shades` palettes (e.g. `blue_shades`) for ordered/related categories. See [references/colors.md](references/colors.md) for the full list and contents.

## Gradients (continuous colormaps)

`apc.gradients.<name>` for heatmaps, density plots, and continuous color mapping. Use a **diverging** gradient only when the data has a meaningful midpoint.

```python
import seaborn as sns

# Matplotlib/seaborn: convert to a colormap, OR use the registered "apc:" name after setup()
sns.heatmap(data, cmap=apc.gradients.blues.to_mpl_cmap())
sns.heatmap(data, cmap="apc:blues")        # equivalent; "apc:blues_r" for reversed

# Plotly:
import plotly.graph_objects as go
go.Heatmap(z=data, colorscale=apc.gradients.magma.to_plotly_colorscale())
```

Perceptually-uniform: `magma` (default), `viridis`, `verde`, `sunset`, `wine`, `lisafrank`. Monocolor: `reds`, `oranges`, `greens`, `sages`, `blues`, `purples`. Diverging (bicolor): `orange_sage`, `red_blue`, `purple_green`. Also map raw values to colors with `gradient.map_values(values)`.

## Fonts

The style guide uses **Atkinson Hyperlegible Next** (text) and **Atkinson Hyperlegible Mono** (numbers). `setup()` loads them automatically. If they aren't installed, the call prints a warning and falls back to default fonts — install both families from [Google Fonts](https://fonts.google.com/?query=atkinson+hyperlegible) to fix this.

## Exporting figures

`save_figure` exports at Arcadia Creative Cloud panel sizes. `size` must be one of `"full_wide"` (1000 px), `"float"` (650 px), or `"half_square"` (490 px).

```python
apc.mpl.save_figure("plot", size="full_wide", filetypes=["pdf", "svg"], context="print")
apc.plotly.save_figure(fig, "plot.svg", size="float")
```

- Matplotlib `context`: `"web"` (72 dpi, default) or `"print"` (300 dpi).
- Prefer **SVG** or **PDF** for figures that will be edited in Adobe Illustrator. The Matplotlib SVG export is automatically patched so Illustrator renders the fonts.

## Checking color-vision-deficiency (CVD) safety

```python
apc.cvd.display_all_palette(apc.palettes.primary)   # show deuter/protan/tritanomaly
apc.cvd.simulate_gradient(apc.gradients.blues, cvd_type="d")
```

Use these to confirm a palette/gradient stays distinguishable. Full API: [references/api.md](references/api.md).

## Gotchas

- **Call `setup()` exactly once, before plotting; call `style_plot()` after plotting** on each Axes (Matplotlib) or Figure (Plotly). Skipping `style_plot` leaves labels uncapitalized and numeric ticks in the wrong font.
- **`"apc:<name>"` colormap/color strings only resolve after `setup()`** has run.
- **Use named colors, never hardcoded hex.** The library's hex values are the source of truth for code and match the printed 2026 guide; referencing `apc.<name>` always stays correct.
- **`monospaced_axes` is for numeric axes** (numbers use the mono font per the guide); **`categorical_axes` is for category axes** (removes ticks, adjusts padding). In Plotly, `monospaced_axes` also adds thousands separators to numeric ticks.
- **Axis selector values differ by backend.** Matplotlib `style_plot`: `"x"`, `"y"`, `"both"`, `"all"`, `None`. Plotly `style_plot`: `"x"`, `"y"`, `"z"`, `"xy"`, `"yz"`, `"xz"`, `"xyz"`, `"all"`, `None`, plus `row`/`col` for subplots.
- **Capitalization only applies to all-lowercase strings** — pre-capitalized or acronym labels are left untouched, so write labels in lowercase and let `style_plot` handle them.
- **Defaults after `setup()`:** the color cycle is `palettes.all_ordered` and the default image colormap is `magma`.
- **Avoid `matplotlib==3.8.0`** (a `LinearSegmentedColormap` bug); the package pins around it.

## Reference files

- [references/colors.md](references/colors.md) — every named color, palette, and gradient with hex codes and contents.
- [references/api.md](references/api.md) — full function/method reference for `apc.mpl`, `apc.plotly`, `apc.cvd`, `apc.plot`, and the `HexCode` / `Palette` / `Gradient` classes.
