# Colors, palettes, and gradients

All hex values below are the library's authoritative values (`arcadia_pycolor.colors`), matching the printed 2026 style guide. Always reference colors by name (`apc.<name>`) rather than hardcoding hex.

## Named colors

Access as `apc.<name>` (e.g. `apc.aegean`). Each is a `HexCode`, usable directly as a color argument.

### Primary (use for data / illustrated elements)

| Name | Hex | | Name | Hex |
|------|-----|---|------|-----|
| `aegean` | #5088C5 | | `vital` | #73B5E3 |
| `amber` | #F28360 | | `tangerine` | #FFB883 |
| `seaweed` | #3B9886 | | `lime` | #97CD78 |
| `canary` | #F7B846 | | `dragon` | #C85152 |
| `aster` | #7A77AB | | `oat` | #F5E4BE |
| `rose` | #F898AE | | `wish` | #BABEE0 |

### Secondary (use for data / illustrated elements)

| Name | Hex | | Name | Hex |
|------|-----|---|------|-----|
| `sky` | #C6E7F4 | | `sage` | #B5BEA4 |
| `dress` | #F8C5C1 | | `marine` | #8A99AD |
| `taupe` | #DBD1C3 | | `mars` | #DA9085 |
| `denim` | #B6C8D4 | | `shell` | #EDE0D6 |

### Neutral (use for supporting elements; text only in black/white/charcoal)

| Name | Hex | | Name | Hex |
|------|-----|---|------|-----|
| `gray` | #EBEDE8 | | `charcoal` | #484B50 |
| `chateau` | #B9AFA7 | | `crow` | #292928 |
| `bark` | #8F8885 | | `forest` | #596F74 |
| `slate` | #43413F | | `pitch` | #09090A |

### Background (use as background fills)

| Name | Hex | | Name | Hex |
|------|-----|---|------|-----|
| `parchment` | #FEF7F1 | | `lichen` | #F7FBEF |
| `zephyr` | #F4FBFE | | `dawn` | #F8F4F1 |

### Shades and additional colors

`lapis` #2B66A2, `dusk` #094468, `cinnabar` #9E3F41, `melon` #FFCFAF, `sun` #FFD364, `mustard` #D68D22, `umber` #A85E28, `iris` #DCDFEF, `tanzanite` #54448C, `glass` #C3E2DB, `teal` #6FBCAD, `asparagus` #2A6B5E, `depths` #09473E, `putty` #FFE3D4, `candy` #E2718F, `azalea` #C04C70, `stone` #EDE6DA, `mud` #635C5A, `ice` #E6EAED, `dove` #CAD4DB, `cloud` #ABBAC4, `steel` #687787, `fern` #47784A, `edamame` #C1E1AE, `matcha` #71AC5A, `yucca` #1E4812.

### Gradient anchor colors

`concord` #341E60, `heather` #A96789, `tumbleweed` #E9A482, `wheat` #F5DFB2, `shire` #4E7F72, `topaz` #FFCC7B, `space` #282A49, `butter` #FFFDBD, `terracotta` #964222, `blush` #FFF3F4, `lilac` #6862AB, `ghost` #FCF7FF, `redwood` #52180A.

### Other / generic

`brightgray` #EAEAEA, `paper` #FCFCFC, `soil` #4D2500, `blossom` #F4CAE3, `mint` #D1EADF, plus pure `white`, `black`, `red`, `green`, `blue`, `cyan`, `magenta`, `yellow`.

## Palettes

Access as `apc.palettes.<name>`. Each is a `Palette` (index, slice, iterate, `+`). List all in a notebook with `apc.plot.display_all_palettes()`.

| Palette | Colors (in order) |
|---------|-------------------|
| `primary` | aegean, amber, seaweed, canary, aster, rose, vital, tangerine, lime, dragon, oat, wish |
| `secondary` | sky, dress, taupe, denim, sage, marine, mars, shell |
| `neutral` | gray, chateau, bark, slate, charcoal, crow, forest, pitch |
| `background` | parchment, zephyr, lichen, dawn |
| `primary_ordered` | aegean, amber, canary, lime, aster, rose, seaweed, dragon, vital, tangerine, oat, wish |
| `secondary_ordered` | sky, dress, taupe, sage, denim, mars, shell, marine |
| `all_ordered` | primary_ordered + secondary_ordered — **the default Matplotlib color cycle after `setup()`** |
| `blue_shades` | dusk, lapis, aegean, vital, sky |
| `red_shades` | cinnabar, dragon, amber, tangerine, melon |
| `yellow_shades` | umber, mustard, canary, sun, oat |
| `purple_shades` | concord, tanzanite, aster, wish, iris |
| `teal_shades` | depths, asparagus, seaweed, teal, glass |
| `pink_shades` | azalea, candy, rose, dress, putty |
| `green_shades` | yucca, fern, matcha, lime, edamame |
| `warm_gray_shades` | mud, bark, chateau, taupe, stone |
| `cool_gray_shades` | steel, marine, cloud, dove, ice |
| `all_colors` | every catalogued color |

**Choosing a palette:** use `primary`/`secondary` (or the `_ordered` variants) for distinct categorical groups; use a single `*_shades` palette for ordered/sequential categories or to emphasize one element within a group. Match the number of colors you take to the number of categories.

## Gradients

Access as `apc.gradients.<name>`. Each is a `Gradient`. Convert with `.to_mpl_cmap()` / `.to_plotly_colorscale()`, or after `setup()` reference by string `"apc:<name>"` (and `"apc:<name>_r"` for reversed). List all with `apc.plot.display_all_gradients()`.

| Type | Gradients | Use for |
|------|-----------|---------|
| Perceptually uniform (sequential) | `magma` (default), `viridis`, `verde`, `sunset`, `wine`, `lisafrank` | heatmaps, continuous values |
| Monocolor (sequential) | `reds`, `oranges`, `greens`, `sages`, `blues`, `purples` | lines/dots that support one primary color |
| Diverging (bicolor) | `orange_sage`, `red_blue`, `purple_green` | data with a meaningful midpoint |

Inspect gradient uniformity with `apc.plot.plot_gradient_lightness([apc.gradients.magma, ...])`.
