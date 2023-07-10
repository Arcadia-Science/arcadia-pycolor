import random
import matplotlib as mpl
from .functions import print_color, display_palette, display_palette_interactive, extend_colors, plot_color_gradients, plot_color_lightness
import json

__all__ = ['Palette', 'Gradient']

class Palette(object):
    def __init__(self, name: str, color_dict: dict):
        self.dict = color_dict
        self.name = name
        
        # directly store each color as an attribute of the palette
        for nickname in self.nicknames:
            key = nickname.replace(':', '_') if ':' in nickname else nickname
            setattr(self, key, self.dict[nickname])
    
    def __call__(self):
        return self.dict
    
    def __len__(self):
        return len(self.dict)
        
    @property
    def nicknames(self):
        return list(self.dict.keys())
    
    @property
    def colors(self):
        return list(self.dict.values())
    
    @property
    def nested_list(self):
        return [[self.nicknames[i], self.colors[i]] for i in range(len(self.dict))]
    
    @property
    def tuple_list(self):
        return [(self.nicknames[i], self.colors[i]) for i in range(len(self.dict))]
    
    @property
    def mpl_ListedColormap(self):
        return mpl.colors.ListedColormap(self.colors, name = self.name)
    
    @property
    def mpl_ListedColormap_r(self):
        return self.mpl_ListedColormap.reversed()
    
    def sample(self, number: int, fmt = 'list'):
        if number > len(self):
            raise Exception(f'Requested {number} colors but there are only {len(self)} in this palette.')
        
        if how == 'list':
            return random.choices(self.colors, number)
        elif how == 'dict':
            return {choice: self.dict[choice] for choice in random.choices(self.nicknames, number)}
        elif how == 'nested_list':
            return [[choice, self.dict[choice]] for choice in random.choices(self.nicknames, number)]
        elif how == 'tuple_list':
            return [(choice, self.dict[choice]) for choice in random.choices(self.nicknames, number)]
        else:
            raise Exception(f'{fmt} is not a valid format option.')
            
    def extend(self, keys: list, *args, **kwargs):
        return extend_colors(self.colors, len(keys), *args, **kwargs)
            
    def cmap(self, keys: list, extend = True, *args, **kwargs):
        if len(keys) > len(self.colors) and not extend:
            raise ValueError(f'Not enough colors ({len(self.colors)}) for {len(keys)} keys. Set extend = True to override.')
        elif len(keys) > len(self.colors):
            return dict(zip(keys, self.extend(keys, *args, **kwargs)))
        else:
            return dict(zip(keys, self.colors[:len(keys)]))
    
    def mpl_ListedColormap_register(self, name = None):
        if self.name not in mpl.colormaps.keys():
            mpl.colormaps.register(cmap=self.mpl_ListedColormap)
            mpl.colormaps.register(cmap=self.mpl_ListedColormap_r)
        
    def mpl_NamedColors_register(self):
        mpl.cm.colors.get_named_colors_mapping().update(self.dict)
        
    def print(self):
        print_color(self.dict)
        
    def display(self):
        display_palette([{'name': self.name, 'length': len(self.dict), 'cmap': self.mpl_ListedColormap}])
        
    def display_r(self):
        display_palette([{'name': self.name, 'length':  len(self.dict), 'cmap': self.mpl_ListedColormap_r}])
        
    def display_interactive(self):
        display_palette_interactive({self.name: self.dict})

    def __repr__(self):
        return json.dumps(self.dict, indent = 2)
    
    def __call__(self):
        self.display()

class Gradient(Palette):
    def __init__(self, name: str, color_dict: dict, values = []):
        super().__init__(name, color_dict)
        
        if len(color_dict) < 2:
            raise ValueError('A gradient must include at least 2 distinct colors.')
        
        if len(values) == 0:
            fraction = 1 / (len(color_dict) - 1)
            values_passed = [i * fraction for i in range(len(color_dict))]
        elif len(values) != len(color_dict):
            raise ValueError('Number of values must be equal to number of color_dict entries.')
        else:
            values_passed = values
        
        self.values = values_passed
    
    @property
    def grad_dict(self):
        return dict(zip(self.values, self.colors))
    
    @property
    def grad_nested_list(self):
        return [[self.values[i], self.colors[i]] for i in range(len(self.dict))]
    
    @property
    def grad_tuple_list(self):
        return [(self.values[i], self.colors[i]) for i in range(len(self.dict))]
    
    @property
    def mpl_LinearSegmentedColormap(self):
        return mpl.colors.LinearSegmentedColormap.from_list(self.name, self.grad_tuple_list)
    
    @property
    def mpl_LinearSegmentedColormap_r(self):
        return self.mpl_LinearSegmentedColormap.reversed()
    
    def mpl_LinearSegmentedColormap_register(self):
        if self.name not in mpl.colormaps.keys():
            mpl.colormaps.register(cmap=self.mpl_LinearSegmentedColormap)
            mpl.colormaps.register(cmap=self.mpl_LinearSegmentedColormap_r)
    
    def display(self, length = 10):
        display_palette([{'name': self.name, 'length': length, 'cmap': self.mpl_LinearSegmentedColormap}])
        
    def display_r(self, length = 10):
        display_palette([{'name': self.name, 'length': length, 'cmap': self.mpl_LinearSegmentedColormap_r}])
    
    def plot_gradient(self, figsize = (5, 0.5), *args, **kwargs):
        plot_color_gradients({self.name: self.mpl_LinearSegmentedColormap}, figsize = figsize, *args, **kwargs)
    
    def plot_lightness(self, cmap_type = '', tickrotation = 0, markersize = 100, figsize = (3, 2), *args, **kwargs):
        plot_color_lightness({self.name: self.mpl_LinearSegmentedColormap}, cmap_type = cmap_type, tickrotation = tickrotation, markersize = markersize, figsize = figsize, *args, **kwargs)
    
    def __repr__(self):
        out_json = {'color_dict': self.dict, 'values': self.values}
        return json.dumps(out_json, indent = 2)
