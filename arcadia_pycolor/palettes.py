import arcadia_pycolor.colors as colors
from arcadia_pycolor.palette import Palette

primary = Palette(
    "Primary",
    [
        colors.aegean,
        colors.amber,
        colors.seaweed,
        colors.canary,
        colors.aster,
        colors.rose,
        colors.vital,
        colors.tangerine,
        colors.lime,
        colors.dragon,
        colors.oat,
        colors.wish,
    ],
)

secondary = Palette(
    "Secondary",
    [
        colors.sky,
        colors.dress,
        colors.taupe,
        colors.denim,
        colors.sage,
        colors.marine,
        colors.mars,
        colors.shell,
    ],
)

neutral = Palette(
    "Neutral",
    [
        colors.gray,
        colors.chateau,
        colors.bark,
        colors.slate,
        colors.charcoal,
        colors.crow,
        colors.forest,
        colors.pitch,
    ],
)

background = Palette(
    "Background",
    [colors.parchment, colors.zephyr, colors.lichen, colors.dawn],
)

primary_ordered = Palette(
    "PrimaryOrdered",
    [
        colors.aegean,
        colors.amber,
        colors.canary,
        colors.lime,
        colors.aster,
        colors.rose,
        colors.seaweed,
        colors.dragon,
        colors.vital,
        colors.tangerine,
        colors.oat,
        colors.wish,
    ],
)

secondary_ordered = Palette(
    "SecondaryOrdered",
    [
        colors.sky,
        colors.dress,
        colors.taupe,
        colors.sage,
        colors.denim,
        colors.mars,
        colors.shell,
        colors.marine,
    ],
)

all_ordered = primary_ordered + secondary_ordered
all_ordered.name = "AllOrdered"

blue_shades = Palette(
    "BlueShades",
    [colors.dusk, colors.lapis, colors.aegean, colors.vital, colors.sky],
)

red_shades = Palette(
    "RedShades",
    [colors.cinnabar, colors.dragon, colors.amber, colors.tangerine, colors.melon],
)

yellow_shades = Palette(
    "YellowShades",
    [colors.umber, colors.mustard, colors.canary, colors.sun, colors.oat],
)

purple_shades = Palette(
    "PurpleShades",
    [colors.concord, colors.tanzanite, colors.aster, colors.wish, colors.iris],
)

teal_shades = Palette(
    "TealShades",
    [colors.depths, colors.asparagus, colors.seaweed, colors.teal, colors.glass],
)

pink_shades = Palette(
    "PinkShades",
    [colors.azalea, colors.candy, colors.rose, colors.dress, colors.putty],
)

warm_gray_shades = Palette(
    "WarmGrayShades",
    [colors.mud, colors.bark, colors.chateau, colors.taupe, colors.stone],
)

cool_gray_shades = Palette(
    "CoolGrayShades",
    [colors.steel, colors.marine, colors.cloud, colors.dove, colors.ice],
)

green_shades = Palette(
    "GreenShades",
    [colors.yucca, colors.fern, colors.matcha, colors.lime, colors.edamame],
)

other = Palette(
    "Other",
    [
        colors.concord,
        colors.brightgray,
        colors.paper,
        colors.redwood,
        colors.depths,
        colors.soil,
        colors.umber,
        colors.parchment,
        colors.heather,
        colors.tumbleweed,
        colors.wheat,
        colors.shire,
        colors.topaz,
        colors.space,
        colors.butter,
        colors.terracotta,
        colors.blush,
        colors.lilac,
        colors.ghost,
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
all_colors = primary + secondary + neutral + background + other + named
shades = (
    blue_shades
    + red_shades
    + yellow_shades
    + purple_shades
    + teal_shades
    + pink_shades
    + warm_gray_shades
    + cool_gray_shades
    + green_shades
)
all_colors = all_colors + Palette(
    name="Shades", colors=[color for color in shades.colors if color not in all_colors.colors]
)
all_colors.name = "AllColors"


all_palettes = [obj for obj in globals().values() if isinstance(obj, Palette)]
