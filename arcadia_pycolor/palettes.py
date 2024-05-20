from .classes_new import Palette
from .colors_new import (
    aegean,
    amber,
    aster,
    bark,
    black,
    blossom,
    blue,
    bluegrass,
    bluesky,
    brightgrey,
    buff,
    canary,
    carmine,
    charcoal,
    chateau,
    cocoa,
    concord,
    crow,
    cyan,
    dawn,
    denim,
    depths,
    dragon,
    dress,
    forest,
    grape,
    green,
    lichen,
    lightgrey,
    lime,
    magenta,
    marineblue,
    mars,
    mint,
    oat,
    orchid,
    paleazure,
    paper,
    periwinkle,
    pitaya,
    pitch,
    red,
    redwood,
    rose,
    royal,
    sage,
    satin,
    seafoam,
    seaweed,
    shell,
    slate,
    soil,
    taffy,
    tangerine,
    taupe,
    umber,
    vitalblue,
    white,
    wish,
    yellow,
    yucca,
    zephyr,
)

core = Palette(
    "Core",
    [lightgrey, shell, dawn, seafoam, tangerine, pitch, charcoal, marineblue, forest],
)

neutral = Palette("Neutral", [zephyr, paleazure, lichen, orchid, buff, bark, slate, crow])

accent = Palette(
    "Accent",
    [aegean, amber, seaweed, canary, aster, rose],
)

light_accent = Palette(
    "LightAccent",
    [bluesky, dress, sage, oat, periwinkle, blossom],
)

# tangerine and marineblue are included in both the core and accent expanded palettes.
accent_expanded = Palette(
    "AccentExpanded",
    [lime, vitalblue, tangerine, chateau, marineblue, dragon],
)

light_accent_expanded = Palette("LightAccentExpanded", [mint, wish, satin, taupe, mars, denim])

other = Palette(
    "Other",
    [
        concord,
        grape,
        taffy,
        brightgrey,
        paper,
        redwood,
        cocoa,
        royal,
        carmine,
        depths,
        bluegrass,
        yucca,
        pitaya,
        soil,
        umber,
    ],
)

named = Palette(
    "Named",
    [white, red, green, blue, cyan, magenta, yellow, black],
)

# All palettes
all = (
    core + neutral + accent + light_accent + accent_expanded + light_accent_expanded + other + named
)
all.rename("All")
