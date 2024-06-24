import arcadia_pycolor.colors as colors
from arcadia_pycolor.palette import Palette

core = Palette(
    "Core",
    [
        colors.lightgrey,
        colors.shell,
        colors.dawn,
        colors.seafoam,
        colors.tangerine,
        colors.pitch,
        colors.charcoal,
        colors.marineblue,
        colors.forest,
    ],
)

neutral = Palette(
    "Neutral",
    [
        colors.zephyr,
        colors.paleazure,
        colors.lichen,
        colors.orchid,
        colors.buff,
        colors.bark,
        colors.slate,
        colors.crow,
    ],
)

accent = Palette(
    "Accent",
    [colors.aegean, colors.amber, colors.seaweed, colors.canary, colors.aster, colors.rose],
)

light_accent = Palette(
    "LightAccent",
    [colors.bluesky, colors.dress, colors.sage, colors.oat, colors.periwinkle, colors.blossom],
)

# tangerine and marineblue are included in both the core and accent expanded palettes.
accent_expanded = Palette(
    "AccentExpanded",
    [
        colors.lime,
        colors.vitalblue,
        colors.tangerine,
        colors.chateau,
        colors.marineblue,
        colors.dragon,
    ],
)

light_accent_expanded = Palette(
    "LightAccentExpanded",
    [colors.mint, colors.wish, colors.satin, colors.taupe, colors.mars, colors.denim],
)

accent_ordered = Palette(
    "AccentOrdered",
    [
        colors.aegean,
        colors.amber,
        colors.canary,
        colors.lime,
        colors.aster,
        colors.rose,
        colors.seaweed,
        colors.dragon,
        colors.vitalblue,
        colors.chateau,
        colors.marineblue,
        colors.tangerine,
    ],
)

light_ordered = Palette(
    "LightOrdered",
    [
        colors.bluesky,
        colors.dress,
        colors.oat,
        colors.sage,
        colors.periwinkle,
        colors.denim,
        colors.taupe,
        colors.mars,
        colors.blossom,
        colors.mint,
        colors.wish,
        colors.satin,
    ],
)

accent_all_ordered = accent_ordered + light_ordered
accent_all_ordered.name = "AccentAllOrdered"


other = Palette(
    "Other",
    [
        colors.concord,
        colors.grape,
        colors.taffy,
        colors.brightgrey,
        colors.paper,
        colors.redwood,
        colors.cocoa,
        colors.royal,
        colors.carmine,
        colors.depths,
        colors.bluegrass,
        colors.yucca,
        colors.pitaya,
        colors.soil,
        colors.umber,
        colors.parchment,
    ],
)

named = Palette(
    "Named",
    [
        colors.white,
        colors.red,
        colors.green,
        colors.blue,
        colors.cyan,
        colors.magenta,
        colors.yellow,
        colors.black,
    ],
)

# All palettes
all = (
    core + neutral + accent + light_accent + accent_expanded + light_accent_expanded + other + named
)
all.name = "All"

all_palettes = [obj for obj in globals().values() if isinstance(obj, Palette)]
