# API reference

Signatures and behavior for the functions and classes in `arcadia_pycolor` (`apc`). Read this when you need an argument you don't remember or a less-common helper.

## `apc.mpl` — Matplotlib / seaborn

### Setup and global styling

- `setup(font_dirpath=None)` — Load colors, fonts, colormaps, and the global theme. Call once before plotting. `font_dirpath` overrides where fonts are searched.
- `load_colors()` / `load_fonts(font_dirpath=None)` / `load_colormaps()` / `load_styles()` — the individual steps `setup()` runs; rarely needed directly.

### Per-plot styling

- `style_plot(axes=None, monospaced_axes=None, categorical_axes=None, colorbar_exists=False)` — Main per-Axes styler. Capitalizes axis labels, styles the legend if present.
  - `axes`: an `Axes`; defaults to `plt.gca()`.
  - `monospaced_axes`: `"x"`, `"y"`, `"both"`, `"all"`, or `None`. Sets numeric tick labels to the mono font.
  - `categorical_axes`: `"x"`, `"y"`, `"both"`, `"all"`, or `None`. Removes ticks and adjusts padding for category axes; also capitalizes those tick labels.
  - `colorbar_exists`: `True` to also set colorbar tick labels to the mono font.

### Saving

- `save_figure(filepath, size, filetypes=None, context="web", **savefig_kwargs)`
  - `size`: `"full_wide"`, `"float"`, or `"half_square"`.
  - `filetypes`: list of extensions (e.g. `["pdf", "svg"]`); if `None`, inferred from `filepath`'s suffix.
  - `context`: `"web"` (72 dpi) or `"print"` (300 dpi).
  - SVG output is auto-patched so Adobe Illustrator renders Atkinson fonts.
- `get_figure_dimensions(size) -> (width, height)` — figure size in inches minus padding.

### Lower-level helpers (usually called via `style_plot`)

- Fonts: `set_ticklabel_font`, `set_xticklabel_font`, `set_yticklabel_font`, `set_ticklabel_monospaced`, `set_xticklabel_monospaced`, `set_yticklabel_monospaced`.
- Capitalization: `capitalize_ticklabels`, `capitalize_xticklabels`, `capitalize_yticklabels`, `capitalize_axislabels`, `capitalize_xlabel`, `capitalize_ylabel`.
- Categorical axes: `set_axes_categorical`, `set_xaxis_categorical`, `set_yaxis_categorical`.
- Legend: `style_legend(legend)`, `capitalize_legend_text(legend)`, `add_legend_line(legend)`, `justify_legend_text(legend)`.
- Misc: `add_commas_to_axis_tick_labels(axis)`, `set_colorbar_ticklabel_monospaced`.

Each `set_*`/`capitalize_*` axes helper takes `axes=None` (defaults to current Axes).

## `apc.plotly` — Plotly

Imported from `arcadia_pycolor.plotly_utils`; access as `apc.plotly`.

### Setup and styling

- `setup()` — Register and activate the Arcadia Plotly template (`pio.templates.default`).
- `style_plot(fig, monospaced_axes=None, categorical_axes=None, row=None, col=None)`
  - `monospaced_axes` / `categorical_axes` accept: `"x"`, `"y"`, `"z"`, `"xy"`, `"yz"`, `"xz"`, `"xyz"`, `"all"`, or `None`.
  - `monospaced_axes` also adds thousands separators to numeric ticks.
  - `row`/`col` target a specific subplot.
- `get_arcadia_styles() -> dict` — the template layout as a dict.

### Sizing and saving

- `set_figure_dimensions(fig, size)` — set width/height to a panel size.
- `save_figure(fig, filepath, size, filetypes=None, **write_image_kwargs)` — export at a panel size with margins removed (re-add margins in Illustrator). Valid types: png, jpg, jpeg, webp, svg, pdf.
- `export_to_html(fig, filepath)` — HTML export with Atkinson fonts embedded from Google Fonts (3D figures fall back to default Plotly fonts).

### Lower-level helpers (per-axis, all accept `row`/`col`)

- Fonts: `set_ticklabel_font`, `set_{x,y,z}ticklabel_font`, `set_ticklabel_monospaced`, `set_{x,y,z}ticklabel_monospaced`, `set_colorbar_ticklabel_monospaced`.
- Capitalization: `capitalize_ticklabels`, `capitalize_{x,y,z}ticklabels`, `capitalize_axislabels`, `capitalize_{x,y,z}label`, `capitalize_colorbar_label`, `capitalize_legend_title`, `capitalize_legend_entries`, `style_legend(fig)`.
- Categorical: `set_axes_categorical`, `set_{x,y,z}axis_categorical`.
- Commas: `add_commas_to_axis_tick_labels`, `add_commas_to_{x,y,z}axis_ticklabels`.
- Hiding: `hide_ticks`, `hide_{x,y,z}axis_ticks`, `hide_axis_lines`, `hide_{x,y,z}axis_line`.

## `apc.cvd` — Color-vision-deficiency simulation

`cvd_type` is `"d"` (deuteranomaly), `"p"` (protanomaly), or `"t"` (tritanomaly); `severity` is `0`–`100`.

- `simulate_color(colors, cvd_type="d", severity=100)` — a `HexCode` or list of them.
- `simulate_palette(palette, cvd_type="d", severity=100) -> Palette`.
- `simulate_gradient(gradient, cvd_type="d", severity=100) -> Gradient`.
- `display_all_color(color, severity=100)` — print swatches for all CVD types.
- `display_all_palette(palette, severity=100)`.
- `display_all_gradient(gradient, severity=100)`.
- `display_all_gradient_lightness(gradient, severity=100, **kwargs)`.

## `apc.plot` — Inspection utilities

- `plot_gradient_lightness(gradients, title=None, steps=100, figsize=(4,4), return_fig=False, ...)` — plot lightness (L*) of one or more gradients to assess perceptual uniformity.
- `display_all_gradients()` / `display_all_palettes()` — print every gradient/palette swatch.

## `apc.HexCode` (a `str` subclass)

`HexCode(name, hex_code)`. Usable anywhere a color string is expected.

- `.name`, `.hex_code` — attributes.
- `.to_rgb() -> [int, int, int]`.
- `.to_cam02ucs() -> [J, a, b]` (lightness + chromaticity).
- `.swatch(width=2, min_name_width=None) -> str` — colored terminal swatch.

## `apc.Palette`

`Palette(name, colors)`; `Palette.from_dict(name, {color_name: hex})`.

- Sequence behavior: `len()`, iteration, `palette[i]` (→ `HexCode`), `palette[a:b]` (→ `Palette`).
- `+` concatenates two palettes.
- `.reverse() -> Palette`.
- `.swatch() -> str`; evaluating a palette in a notebook prints all swatches.
- `.to_mpl_cmap() -> ListedColormap`.

## `apc.Gradient`

`Gradient(name, colors, values=None)` where `values` are anchor positions in `[0, 1]` (must start at 0 and end at 1; same length as `colors`). `Gradient.from_dict(...)` also exists.

- `.anchor_colors`, `.anchor_values`, `.num_anchors`.
- `.to_mpl_cmap() -> LinearSegmentedColormap`.
- `.to_plotly_colorscale() -> list[(pos, hex)]` (256 steps).
- `.reverse() -> Gradient`.
- `.resample_as_palette(steps=5) -> Palette` — discrete sample of the gradient.
- `.map_values(values, min_value=None, max_value=None) -> list[HexCode]` — map data to colors.
- `.interpolate_lightness() -> Gradient` — re-space anchors by lightness (needs ≥3 anchors, monotonic lightness).
- `+` concatenates gradients (deduplicates a shared boundary color).

## `apc.style_defaults` — Constants

- `FigureSize` literals and sizes: `FIGURE_SIZES_IN_INCHES`, `FIGURE_SIZES_IN_PIXELS` (`full_wide` 1000×420, `float` 650×420, `half_square` 490×490 px including padding).
- DPI: `BASE_DPI` (72), `PRINT_DPI` (300). Padding: `FIGURE_PADDING_PIXELS` (30).
- Fonts: `DEFAULT_FONT` ("Atkinson Hyperlegible Next"), `MONOSPACE_FONT` ("Atkinson Hyperlegible Mono"), and Plotly font-stack strings.
- `ARCADIA_MATPLOTLIB_RC_PARAMS`, `ARCADIA_PLOTLY_TEMPLATE_LAYOUT` — the full theme objects.
