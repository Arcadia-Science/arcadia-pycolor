from pathlib import Path
import matplotlib.pyplot as plt
from .functions import reverse_gradient
from .classes import Palette, Gradient

#######################
## Individual Colors ##
#######################
"""
Each color is provided as a dictionary with the color name and HEX code.
"""

# Core colors
lightgrey = {'arcadia:lightgrey': '#EBEDE8'}
shell = {'arcadia:shell': '#EDE0D6'}
dawn = {'arcadia:dawn': '#F8F4F1'}
seafoam = {'arcadia:seafoam': '#F9FCF0'}
orange = {'arcadia:orange': '#FFB984'}
black = {'arcadia:black': '#09090A'}
charcoal = {'arcadia:charcoal': '#484B50'}
marineblue = {'arcadia:marineblue': '#8A99AD'}
forest = {'arcadia:forest': '#596F74'}

# Neutral colors
zephyr = {'arcadia:zephyr': '#F4FBFF'}
paleazure = {'arcadia:paleazure': '#F7F9FD'}
lichen = {'arcadia:lichen': '#F7FBEF'}
orchid = {'arcadia:orchid': '#FFFDF7'}
buff = {'arcadia:buff': '#FFFBF8'}
bark = {'arcadia:bark': '#8F8885'}
slate = {'arcadia:slate': '#43413F'}
crow = {'arcadia:crow': '#292928'}

# Accent colors
aegean = {'arcadia:aegean': '#5088C5'}
amber = {'arcadia:amber': '#F28360'}
seaweed = {'arcadia:seaweed': '#3B9886'}
canary = {'arcadia:canary': '#F7B846'}
aster = {'arcadia:aster': '#7A77AB'}
rose = {'arcadia:rose': '#F898AE'}

# Light accent colors
bluesky = {'arcadia:bluesky': '#C6E7F4'}
dress = {'arcadia:dress': '#F8C5C1'}
sage = {'arcadia:sage': '#B5BEA4'}
oat = {'arcadia:oat': '#F5E4BE'}
periwinkle = {'arcadia:periwinkle': '#DCBFFC'}
blossom = {'arcadia:blossom': '#F5CBE4'}

# Accent expanded colors
# (Orange and Marineblue are included, but are also Core colors)
lime = {'arcadia:lime': '#97CD78'}
vitalblue = {'arcadia:vitalblue': '#73B5E3'}
# orange = {'arcadia:orange': '#FFB984'}
chateau = {'arcadia:chateau': '#BAB0A8'}
dragon = {'arcadia:dragon': '#C85152'}
# marineblue = {'arcadia:marineblue': '#8A99AD'}

# Light accent expanded colors
mint = {'arcadia:mint': '#D1EADF'}
wish = {'arcadia:wish': '#BABEE0'}
satin = {'arcadia:satin': '#F1E8DA'}
taupe = {'arcadia:taupe': '#DAD3C7'}
mars = {'arcadia:mars': '#DA9085'}
denim = {'arcadia:denim': '#B6C8D4'}

# Other Arcadia colors
concord = {'arcadia:concord': '#341E60'}
grape = {'arcadia:grape': '#5A4596'}
taffy = {'arcadia:taffy': '#E87485'}
brightgrey = {'arcadia:brightgrey': '#EAEAEA'}
paper = {'arcadia:paper': '#FCFCFC'}
redwood = {'arcadia:redwood': '#52180A'}
cocoa = {'arcadia:cocoa': '#4D2C03'}
royal = {'arcadia:royal': '#3F2D5C'}
pitaya = {'arcadia:pitaya': '#4A0F45'}
depths = {'arcadia:depths': '#093345'}

# Other named colors
white = {'white': '#FFFFFF'}
red = {'red': '#FF0000'}
green = {'green': '#00FF00'}
blue = {'blue': '#0000FF'}
yellow = {'yellow': '#FFFF00'}
cyan = {'cyan': '#00FFFF'}
magenta = {'magenta': '#FF00FF'}

###############################
## Base Palette Dictionaries ##
###############################
"""
These are the dictionaries collecting the basic palettes.
"""

arcadia_Core = lightgrey | shell | dawn | seafoam | orange | black | charcoal | marineblue | forest
arcadia_Neutral = zephyr | paleazure | lichen | orchid | buff | bark | slate | crow

arcadia_Accent = aegean | amber | seaweed | canary | aster | rose
arcadia_Light = bluesky | dress | sage | oat | periwinkle | blossom

arcadia_Accent_expanded = lime | vitalblue | orange | chateau | dragon | marineblue
arcadia_Light_expanded = mint | wish | satin | taupe | mars | denim

arcadia_Other = concord | grape | taffy | brightgrey | paper | redwood | cocoa | royal

#############################
## Aggregated Dictionaries ##
#############################
"""
These are the dictionaries that aggregate different combinations of the basic palettes.
"""
arcadia_All = arcadia_Core | arcadia_Neutral | arcadia_Accent | arcadia_Light | arcadia_Accent_expanded | arcadia_Light_expanded | arcadia_Other
arcadia_Accent_full = arcadia_Accent | arcadia_Accent_expanded
arcadia_Light_full = arcadia_Light | arcadia_Light_expanded
arcadia_Accent_all = arcadia_Accent | arcadia_Accent_expanded | arcadia_Light | arcadia_Light_expanded

# this exists for backwards-compatibility with other dependent repos that use this variable
# just a temporary fix for now
arcadia_all = arcadia_All

##########################
## Ordered Dictionaries ##
##########################
"""
These are the dictionaries with specifically-ordered colors.
The order of colors has been chosen to maximize distinguishability.
"""

arcadia_Accent_ordered = aegean | amber | canary | lime | aster | rose | seaweed | dragon | vitalblue | chateau | marineblue | orange
arcadia_Light_ordered = bluesky | dress | oat | sage | periwinkle | denim | taupe | mars | blossom | mint | wish | satin

arcadia_Accent_all_ordered = arcadia_Accent_ordered | arcadia_Light_ordered

####################################
## Perceptually Uniform Gradients ##
####################################
"""
These gradients are similar to the gradients available for Matplotlib, Seaborn, and Plotly.
They have been modified to use colors that are harmonious with our brand palette.
The colors have also been optimized to be nearly-perceptually uniform based on lightness.
"""

arcadia_viridis = {
    'color_dict': concord | aegean | lime | yellow,
    'values': [0, 0.49, 0.75, 1]
}

arcadia_magma = {
    'color_dict': black | grape | taffy | orange | oat,
    'values': [0, 0.38, 0.72, 0.9, 1]
}

arcadia_cividis = {
    'color_dict': crow | forest | canary | satin,
    'values': [0, 0.39, 0.85, 1]
}

############################
## Weak Bicolor Gradients ##
############################

arcadia_aegeanamber = {
    'color_dict': aegean | paper | amber,
    'values': [0, 0.5, 1]
}
arcadia_astercanary = {
    'color_dict': aster | paper | canary,
    'values': [0, 0.5, 1]
}
arcadia_seaweedrose = {
    'color_dict': seaweed | paper | rose,
    'values': [0, 0.5, 1]
}

##############################
## Strong Bicolor Gradients ##
##############################

arcadia_poppies = {
    'color_dict': concord | aegean | vitalblue | paper | dress | amber | dragon | redwood,
    'values': [0, 0.26, 0.35, 0.5, 0.6, 0.7, 0.8, 1]
}

arcadia_pansies = {
    'color_dict': royal | aster | wish | paper | oat | canary | cocoa,
    'values': [0, 0.21, 0.39, 0.5, 0.55, 0.64, 1]
}

arcadia_dahlias = {
    'color_dict': depths | seaweed | paper | rose | dragon | pitaya,
    'values': [0, 0.25, 0.5, 0.63, 0.77, 1]
}

################
## Collectors ##
################
"""
These dictionary aggregate all other color dictionaries in the package.

They are accessible within the package namespace as:
    arcadia_pycolor.Palette_dicts
    arcadia_pycolor.Gradient_dicts
or, if using the apc alias:
    apc.Palette_dicts
    apc.Gradient_dicts
"""

Palette_dicts = {
    'arcadia:All': arcadia_All,
    'arcadia:Core': arcadia_Core,
    'arcadia:Neutral': arcadia_Neutral,
    'arcadia:Accent': arcadia_Accent,
    'arcadia:AccentExpanded': arcadia_Accent_expanded,
    'arcadia:AccentFull': arcadia_Accent_full,
    'arcadia:AccentOrdered': arcadia_Accent_ordered,
    'arcadia:Light': arcadia_Light,
    'arcadia:LightExpanded': arcadia_Light_expanded,
    'arcadia:LightFull': arcadia_Light_full,
    'arcadia:LightOrdered': arcadia_Light_ordered,
    'arcadia:AccentAll': arcadia_Accent_all,
    'arcadia:AccentAllOrdered': arcadia_Accent_all_ordered,
    'arcadia:Other': arcadia_Other,
    'arcadia:AllOrdered': arcadia_Accent_all_ordered
}

Gradient_dicts = {
    'arcadia:viridis': arcadia_viridis,
    'arcadia:magma': arcadia_magma,
    'arcadia:cividis': arcadia_cividis,
    'arcadia:aegeanamber': arcadia_aegeanamber,
    'arcadia:astercanary': arcadia_astercanary,
    'arcadia:seaweedrose': arcadia_seaweedrose,
    'arcadia:poppies': arcadia_poppies,
    'arcadia:pansies': arcadia_pansies,
    'arcadia:dahlias': arcadia_dahlias
}

Gradient_r_dicts = {}

for name, grad in Gradient_dicts.items():
    grad_r_name = name + '_r'
    grad_r = reverse_gradient(grad)
    Gradient_r_dicts[grad_r_name] = grad_r

Gradient_dicts = Gradient_dicts | Gradient_r_dicts

###################################
## Matplotlib Color Registration ##
###################################

# Collectors for Palette and Gradient objects
Palettes = {}
Gradients = {}

# Register each of the base palettes
for name, color_dict in Palette_dicts.items():
    pal = Palette(name, color_dict)
    pal.mpl_ListedColormap_register()
    Palettes[name] = pal
    
# Register each of the colors in arcadia:All
Palettes['arcadia:All'].mpl_NamedColors_register()

# Register each of the custom gradients
for name, data in Gradient_dicts.items():
    color_dict = data['color_dict']
    values = data['values']
    grad = Gradient(name, color_dict, values)
    grad.mpl_LinearSegmentedColormap_register()
    Gradients[name] = grad

# Register paper-to-color gradient for each of the colors in the base palette
for color in arcadia_All:
    if color == 'arcadia:paper':
        continue
    name = color + 's'
    color_dict = paper | {color: arcadia_All[color]}
    color_grad = Gradient(name, color_dict)
    color_grad.mpl_LinearSegmentedColormap_register()
    Gradients[name] = color_grad
    
    # add reverse single-color gradients to Gradients dictionary
    name_r = name + '_r'
    color_dict_r = {color: arcadia_All[color]} | paper
    color_grad_r = Gradient(name_r, color_dict_r)
    Gradients[name_r] = color_grad_r

#################
## Stylesheets ##
#################
"""
Auto-loads the Arcadia Basic style for matplotlib.
"""

parent_path = Path(__file__).parent.resolve()
plt.style.use(parent_path / "mplstyles/arcadia_basic.mplstyle")
