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
tangerine = {'arcadia:tangerine': '#FFB984'}
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
# (tangerine and Marineblue are included, but are also Core colors)
lime = {'arcadia:lime': '#97CD78'}
vitalblue = {'arcadia:vitalblue': '#73B5E3'}
# tangerine = {'arcadia:tangerine': '#FFB984'}
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
carmine = {'arcadia:carmine': '#471122'}
depths = {'arcadia:depths': '#09473E'}
bluegrass = {'arcadia:bluegrass': '#458F99'}
yucca = {'arcadia:yucca': '#1E4812'}
pitaya = {'arcadia:pitaya': '#C74970'}
soil = {'arcadia:soil': '#4D2500'}
umber = {'arcadia:umber': '#A85E28'}

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

Core = lightgrey | shell | dawn | seafoam | tangerine | black | charcoal | marineblue | forest
Neutral = zephyr | paleazure | lichen | orchid | buff | bark | slate | crow

Accent = aegean | amber | seaweed | canary | aster | rose
Light = bluesky | dress | sage | oat | periwinkle | blossom

Accent_expanded = lime | vitalblue | tangerine | chateau | dragon | marineblue
Light_expanded = mint | wish | satin | taupe | mars | denim

Other = paper | brightgrey | taffy | pitaya | redwood | cocoa | umber | soil | yucca | bluegrass | depths | royal | grape | concord

#############################
## Aggregated Dictionaries ##
#############################
"""
These are the dictionaries that aggregate different combinations of the basic palettes.
"""
All = Core | Neutral | Accent | Light | Accent_expanded | Light_expanded | Other
Accent_full = Accent | Accent_expanded
Light_full = Light | Light_expanded
Accent_all = Accent | Accent_expanded | Light | Light_expanded

# this exists for backwards-compatibility with other dependent repos that use this variable
# just a temporary fix for now
arcadia_all = All

##########################
## Ordered Dictionaries ##
##########################
"""
These are the dictionaries with specifically-ordered colors.
The order of colors has been chosen to maximize distinguishability.
"""

Accent_ordered = aegean | amber | canary | lime | aster | rose | seaweed | dragon | vitalblue | chateau | marineblue | tangerine
Light_ordered = bluesky | dress | oat | sage | periwinkle | denim | taupe | mars | blossom | mint | wish | satin

Accent_all_ordered = Accent_ordered | Light_ordered

####################################
## Perceptually Uniform Gradients ##
####################################
"""
These gradients are similar to the gradients available for Matplotlib, Seaborn, and Plotly.
They have been modified to use colors that are harmonious with our brand palette.
The colors have also been optimized to be nearly-perceptually uniform based on lightness.
"""

viridis_v1 = {
    'color_dict': concord | aegean | lime | yellow,
    'values': [0, 0.49, 0.75, 1]
}

viridis = {
    'color_dict': concord | grape | aegean | lime | yellow,
     'values': [0, 0.23, 0.49, 0.77, 1]
}

magma = {
    'color_dict': black | grape | taffy | tangerine | oat,
    'values': [0, 0.38, 0.72, 0.9, 1]
}

cividis = {
    'color_dict': crow | forest | canary | satin,
    'values': [0, 0.39, 0.85, 1]
}

################################
## Strong Monocolor Gradients ##
################################

reds = {
    'color_dict': redwood | dragon | amber | paper,
    'values': [0.0, 0.43, 0.64, 1.0]
}
oranges = {
    'color_dict': soil | umber | tangerine | paper,
    'values': [0.0, 0.38, 0.8, 1.0]
}
yellows = {
    'color_dict': cocoa | canary | oat | paper,
    'values': [0.0, 0.76, 0.9, 1.0]
}
greens = {
    'color_dict': yucca | lime | paper,
    'values': [0, 0.7, 1]
}
teals = {
    'color_dict': depths | seaweed | paper,
    'values': [0, 0.42, 1]
}
blues = {
    'color_dict': concord | aegean | vitalblue | paper,
    'values': [0, 0.47, 0.66, 1.0]
}
purples = {
    'color_dict': royal | aster | wish | paper,
    'values': [0, 0.4, 0.74, 1.0]
}
magentas = {
    'color_dict': carmine | pitaya | rose | paper,
    'values': [0, 0.44, 0.73, 1]
}


############################
## Weak Bicolor Gradients ##
############################

aegeanamber = {
    'color_dict': aegean | paper | amber,
    'values': [0, 0.5, 1]
}
astercanary = {
    'color_dict': aster | paper | canary,
    'values': [0, 0.5, 1]
}
limerose = {
    'color_dict': lime | paper | rose,
    'values': [0, 0.5, 1]
}
seaweedtangerine = {
    'color_dict': seaweed | paper | tangerine,
    'values': [0, 0.5, 1]
}
seaweedrose = {
    'color_dict': seaweed | paper | rose,
    'values': [0, 0.5, 1]
}
limetangerine = {
    'color_dict': lime | paper | tangerine,
    'values': [0, 0.5, 1]
}

##############################
## Strong Bicolor Gradients ##
##############################

poppies = {
    'color_dict': concord | aegean | vitalblue | paper | amber | dragon | redwood,
    'values': [0, 0.235, 0.33, 0.5, 0.68, 0.785, 1.0]
}
pansies = {
    'color_dict': royal | aster | wish | paper | oat | canary | cocoa,
    'values': [0, 0.2, 0.37, 0.5, 0.55, 0.62, 1.0]
}
dahlias = {
    'color_dict': yucca | lime | paper | rose | pitaya | carmine,
    'values': [0, 0.35, 0.5, 0.635, 0.78, 1.0]
}
lilies = {
    'color_dict': depths | seaweed | paper | tangerine | umber | soil, 
    'values': [0.0, 0.21, 0.5, 0.6, 0.81, 1.0]
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
    'arcadia:All': All,
    'arcadia:Core': Core,
    'arcadia:Neutral': Neutral,
    'arcadia:Accent': Accent,
    'arcadia:AccentExpanded': Accent_expanded,
    'arcadia:AccentFull': Accent_full,
    'arcadia:AccentOrdered': Accent_ordered,
    'arcadia:Light': Light,
    'arcadia:LightExpanded': Light_expanded,
    'arcadia:LightFull': Light_full,
    'arcadia:LightOrdered': Light_ordered,
    'arcadia:AccentAll': Accent_all,
    'arcadia:AccentAllOrdered': Accent_all_ordered,
    'arcadia:Other': Other,
    'arcadia:AllOrdered': Accent_all_ordered
}

Gradient_dicts = {
    'arcadia:reds': reds,
    'arcadia:oranges': oranges,
    'arcadia:yellows': yellows,
    'arcadia:greens': greens,
    'arcadia:teals': teals,
    'arcadia:blues': blues,
    'arcadia:purples': purples,
    'arcadia:magentas': magentas,
    'arcadia:viridis': viridis,
    'arcadia:viridis_v1': viridis_v1,
    'arcadia:magma': magma,
    'arcadia:cividis': cividis,
    'arcadia:aegeanamber': aegeanamber,
    'arcadia:astercanary': astercanary,
    'arcadia:seaweedrose': seaweedrose,
    'arcadia:limerose': limerose,
    'arcadia:seaweedtangerine': seaweedtangerine,
    'arcadia:limetangerine': limetangerine,
    'arcadia:poppies': poppies,
    'arcadia:pansies': pansies,
    'arcadia:dahlias': dahlias,
    'arcadia:lilies': lilies
}

# collector for reverse gradients
Gradient_r_dicts = {}

# generate reverse gradients and add them as dictionary entries
for name, grad in Gradient_dicts.items():
    grad_r_name = name + '_r'
    grad_r = reverse_gradient(grad)
    Gradient_r_dicts[grad_r_name] = grad_r

Gradient_dicts = Gradient_dicts | Gradient_r_dicts

#############################################
## Palette and Gradient library generation ##
#############################################

# Collectors for Palette and Gradient objects
Palettes = {}
Gradients = {}

# Register each of the base palettes
for name, color_dict in Palette_dicts.items():
    pal = Palette(name, color_dict)
    Palettes[name] = pal

# Register each of the custom gradients
for name, data in Gradient_dicts.items():
    color_dict = data['color_dict']
    values = data['values']
    grad = Gradient(name, color_dict, values)
    Gradients[name] = grad

# Register paper-to-color gradient for each of the colors in the base palette
for color in All:
    if color == 'arcadia:paper':
        continue
    name = color + 's'
    color_dict = paper | {color: All[color]}
    color_grad = Gradient(name, color_dict)
    Gradients[name] = color_grad
    
    # add reverse single-color gradients to Gradients dictionary
    name_r = name + '_r'
    color_dict_r = {color: All[color]} | paper
    color_grad_r = Gradient(name_r, color_dict_r)
    Gradients[name_r] = color_grad_r

######################################
## Matplotlib registration function ##
######################################

def mpl_setup(mode = 'all'):
    '''
    Register Arcadia's colors from the arcadia_pycolor package for use with matplotlib.
    
    Args:
        mode (str): defaults to 'all', which does all of the following keywords.
            To use just one of the following, set mode to the corresponding keyword.
        - 'colors': registers the Arcadia named colors (e.g. 'arcadia:aegean') with matplotlib's named colors.
        - 'palettes': registers the Palettes as named matplotlib ListedColormaps.
        - 'gradients': registers the Gradients as named matplotlib LinearSegmentedColormaps.
        - 'stylesheets': sets the default stylesheet to Arcadia's basic style.
    '''
    if mode == 'colors' or mode == 'all':
        # Register each of the colors in arcadia:All
        Palettes['arcadia:All'].mpl_NamedColors_register()
        
    if mode == 'palettes' or mode == 'all':
        for pal in Palettes:
            Palettes[pal].mpl_ListedColormap_register()
    
    if mode == 'stylesheets' or mode == 'all':
        # find the upstream path to this file
        parent_path = Path(__file__).parent.resolve()
        plt.style.use(parent_path / "mplstyles/arcadia_basic.mplstyle")
    
    if mode == 'gradients' or mode == 'all':
        for grad in Gradients:
            # don't duplicate registration of reverse gradients
            if '_r' not in grad:
                Gradients[grad].mpl_LinearSegmentedColormap_register()
