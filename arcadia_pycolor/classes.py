import json
import random

import matplotlib as mpl

from .functions import (
    display_palette,
    display_palette_interactive,
    extend_colors,
    plot_color_gradients,
    plot_color_lightness,
    print_color,
    simulate_cvd,
)

__all__ = ["Palette", "Gradient"]


class Palette:
    def __init__(self, name: str, color_dict: dict):
        """
        A Palette object stores a collection of colors
        and converts it between different data structures.
        The object also allows for a variety of plotting methods to visualize the contained colors.

        Args:
            name (str): the name of the color palette
            color_dict (dict): a dictionary where the key is the color's name as a string
                and the value is the HEX code of the color as a string.
        """
        self.dict = color_dict
        self.name = name

        # directly store each color as an attribute of the palette
        for nickname in self.nicknames:
            # colons are not acceptable characters when using the dot operator;
            # replace these with underscores
            key = nickname.replace(":", "_") if ":" in nickname else nickname
            setattr(self, key, self.dict[nickname])

    def __repr__(self):
        """
        Returns the string representation of the color dictionary as a JSON-formatted dictionary.
        """
        return json.dumps(self.dict, indent=2)

    def __call__(self):
        """
        Calling the object as a function makes it display the color palette as an image.
        """
        self.display()

    def __len__(self):
        """
        Returns the length of the color dictionary
        """
        return len(self.dict)

    @property
    def nicknames(self):
        """
        Returns the list of color names.
        """
        return list(self.dict.keys())

    @property
    def list(self):
        """
        Returns the list of colors.
        """
        return self.colors

    @property
    def colors(self):
        """
        Returns the list of color hex values.
        """
        return list(self.dict.values())

    @property
    def nested_list(self):
        """
        Returns the color nickname - color HEX pairs as a nested list.
        """
        return [[self.nicknames[i], self.colors[i]] for i in range(len(self.dict))]

    @property
    def tuple_list(self):
        """
        Returns the color nickname - color HEX pairs as list of tuples.
        """
        return [(self.nicknames[i], self.colors[i]) for i in range(len(self.dict))]

    @property
    def mpl_ListedColormap(self):
        """
        Returns the palette as a matplotlib ListedColormap object.
        """
        return mpl.colors.ListedColormap(self.colors, name=self.name)

    @property
    def mpl_ListedColormap_r(self):
        """
        Returns the reverse-ordered palette as a matplotlib ListedColormap object.
        """
        return self.mpl_ListedColormap.reversed()

    def colors_cvd(self, form="d"):
        """
        Returns a color vision deficient version of the colors in the palette.
        """
        return simulate_cvd(self.colors, form=form)

    def mpl_ListedColormap_cvd(self, form="d"):
        """
        Returns a color vision deficient version of the colors in the palette
            as a matplotlib ListedColormap object.
        """
        return mpl.colors.ListedColormap(self.colors_cvd(form), name=self.name + "_" + form)

    def mpl_ListedColormap_cvd_r(self, form="d"):
        """
        Returns a color vision deficient version of the colors in the palette
            as a matplotlib ListedColormap object.
        """
        return self.mpl_ListedColormap_cvd(form).reversed()

    def sample(self, number: int, fmt="list"):
        """
        Randomly samples the color dictionary, returning the data in the desired format.

        Args:
            number (int): number of random colors to return.
            fmt (str): 'list', 'dict', 'nested_list', or 'tuple_list'
        """
        if number > len(self):
            raise Exception(
                f"Requested {number} colors but there are only {len(self)} in this palette."
            )

        if fmt == "list":
            return random.choices(self.colors, number)
        elif fmt == "dict":
            return {choice: self.dict[choice] for choice in random.choices(self.nicknames, number)}
        elif fmt == "nested_list":
            return [
                [choice, self.dict[choice]] for choice in random.choices(self.nicknames, number)
            ]
        elif fmt == "tuple_list":
            return [
                (choice, self.dict[choice]) for choice in random.choices(self.nicknames, number)
            ]
        else:
            raise Exception(f"{fmt} is not a valid format option.")

    def extend(self, keys: list, *args, **kwargs):
        """
        Extends the colors in the dictionary based on a list of keys.
        If the number of colors is less than the number of keys, adds more colors to the list
        that are darker or lighter than the existing colors.

        Args:
            keys (list): list of keys to use for extension
            how (str): 'lighten' or 'darken', defaults to 'lighten'
            steps (list of float): a list of amounts to darken or lighten the color list

        Returns:
            list of original colors plus additional lighter or darker colors generated from the
            original colors, up to the length of the keys.
        """

        return extend_colors(self.colors, len(keys), *args, **kwargs)

    def cmap(self, keys: list, extend=True, *args, **kwargs):
        """
        Generates a colormap dictionary based on a list of keys.

        For each color in the palette, assigns it to one of the keys.
        If there are insufficient colors for the number of keys, tries to extend the colors
        to produce more (darkening them by default).

        Args:
            keys (list): list of keys to assign colors to
            extend (bool): whether to extend the colors if there are not enough, defaults to True
        """
        if len(keys) > len(self.colors) and not extend:
            raise ValueError(
                f"Not enough colors ({len(self.colors)}) for {len(keys)} keys.\
                    Set extend = True to override."
            )
        elif len(keys) > len(self.colors):
            return dict(zip(keys, self.extend(keys, *args, **kwargs)))
        else:
            return dict(zip(keys, self.colors[: len(keys)]))

    def mpl_ListedColormap_register(self):
        """
        Registers the matplotlib ListedColormap object (and its reverse)
        into the list of named matplotlib ListedColormaps.
        """
        if self.name not in mpl.colormaps.keys():
            mpl.colormaps.register(cmap=self.mpl_ListedColormap)
            mpl.colormaps.register(cmap=self.mpl_ListedColormap_r)

            for form in ["d", "p", "t"]:
                mpl.colormaps.register(cmap=self.mpl_ListedColormap_cvd(form))
                mpl.colormaps.register(cmap=self.mpl_ListedColormap_cvd_r(form))

    def mpl_NamedColors_register(self):
        """
        Registers each individual color contained in the Palette
        to the list of matplotlib named colors.
        """
        mpl.cm.colors.get_named_colors_mapping().update(self.dict)

    def print(self):
        """
        Uses print_color to display the color and its HEX as a text output.
        """
        print_color(self.dict)

    def display(self):
        """
        Uses display_palette to display the colors in the palette.
        """
        display_palette(
            [
                {
                    "name": self.name,
                    "length": len(self.dict),
                    "cmap": self.mpl_ListedColormap,
                }
            ]
        )

    def display_r(self):
        """
        Uses display_palette to display the colors in the reversed palette.
        """
        display_palette(
            [
                {
                    "name": self.name,
                    "length": len(self.dict),
                    "cmap": self.mpl_ListedColormap_r,
                }
            ]
        )

    def display_cvd(self, form="d"):
        """
        Uses display_palette to display the colors in the reversed palette.
        """
        display_palette(
            [
                {
                    "name": self.name + "_" + form,
                    "length": len(self.dict),
                    "cmap": self.mpl_ListedColormap_cvd(form=form),
                }
            ]
        )

    def display_interactive(self):
        """
        Uses display_palette_interactive to display an interactive
            hover-over version of the palette.
        """
        display_palette_interactive({self.name: self.dict})


class Gradient(Palette):
    def __init__(self, name: str, color_dict: dict, values: list = None):
        """
        A Gradient object stores a collection of colors
            and converts it between different data structures.
        In addition to storing colors, it also stores the values,
            or the relative position of each color along the gradient.
        The object also allows for a variety of plotting methods to visualize the contained colors.

        Args:
            name (str): the name of the color palette
            color_dict (dict): a dictionary where the key is the color's name as a string
                and the value is the HEX code of the color as a string
            values (list): a list of positions between 0 and 1 for each of the colors in
            the gradient. If this is left empty, the color positions will be assigned uniformly.
        """

        super().__init__(name, color_dict)

        # Checks to make sure the gradient has at least two colors
        if len(color_dict) < 2:
            raise ValueError("A gradient must include at least 2 distinct colors.")

        if isinstance(values, str):
            raise ValueError("Values should be a list of floats.")

        # if there are no values passed, generates color positions uniformly
        if values is None:
            fraction = 1 / (len(color_dict) - 1)
            values_passed = [i * fraction for i in range(len(color_dict))]
        # otherwise, checks to make sure the colors and values are of equivalent length
        elif len(values) != len(color_dict):
            raise ValueError("Number of values must be equal to number of color_dict entries.")
        elif max(values) != 1 or min(values) != 0:
            raise ValueError("Values must be bounded by and include 0 and 1.")
        else:
            values_passed = values

        self.values = values_passed

    def __repr__(self):
        """
        Returns the string representation of the color dictionary
        and values as a JSON-formatted dictionary.
        """
        out_json = {"color_dict": self.dict, "values": self.values}
        return json.dumps(out_json, indent=2)

    @property
    def grad_dict(self):
        """
        Returns a dictionary where the key is the position along the gradient
        and the value is the color at that position.
        """
        return dict(zip(self.values, self.colors))

    @property
    def grad_nested_list(self):
        """
        Returns a nested list of pairs of value - color relationships.
        """
        return [[self.values[i], self.colors[i]] for i in range(len(self.dict))]

    @property
    def grad_tuple_list(self):
        """
        Returns a list of tuples of value - color relationships.
        """
        return [(self.values[i], self.colors[i]) for i in range(len(self.dict))]

    def grad_nested_list_cvd(self, form="d"):
        """
        Returns a nested list of pairs of value - color relationships.
        """
        return [[self.values[i], self.colors_cvd(form=form)[i]] for i in range(len(self.dict))]

    def grad_tuple_list_cvd(self, form="d"):
        """
        Returns a nested list of pairs of value - color relationships.
        """
        return [(self.values[i], self.colors_cvd(form=form)[i]) for i in range(len(self.dict))]

    @property
    def mpl_LinearSegmentedColormap(self):
        """
        Returns the gradient as a matplotlib LinearSegmentedColormap object.
        """
        return mpl.colors.LinearSegmentedColormap.from_list(self.name, self.grad_tuple_list)

    def mpl_LinearSegmentedColormap_cvd(self, form="d"):
        """
        Returns the gradient as a matplotlib LinearSegmentedColormap object.
        """
        return mpl.colors.LinearSegmentedColormap.from_list(
            self.name + "_" + form, self.grad_tuple_list_cvd(form=form)
        )

    @property
    def mpl_LinearSegmentedColormap_r(self):
        """
        Returns the reverse-ordered gradient as a matplotlib LinearSegmentedColormap object.
        """
        return self.mpl_LinearSegmentedColormap.reversed()

    def mpl_LinearSegmentedColormap_cvd_r(self, form="d"):
        """
        Returns the gradient as a matplotlib LinearSegmentedColormap object.
        """
        return self.mpl_LinearSegmentedColormap_cvd(form).reversed()

    def mpl_LinearSegmentedColormap_register(self):
        """
        Registers the matplotlib LinearSegmentedColormap object (and its reverse) into the list of
        named matplotlib LinearSegmentedColormaps.
        """
        if self.name not in mpl.colormaps.keys():
            mpl.colormaps.register(cmap=self.mpl_LinearSegmentedColormap)
            mpl.colormaps.register(cmap=self.mpl_LinearSegmentedColormap_r)

            for form in ["d", "p", "t"]:
                mpl.colormaps.register(cmap=self.mpl_LinearSegmentedColormap_cvd(form))
                mpl.colormaps.register(cmap=self.mpl_LinearSegmentedColormap_cvd_r(form))

    def display(self, length=9):
        """
        Uses display_palette to display the gradient with a number of steps equal to length.

        Args:
            length (int): number of steps to show.
        """
        display_palette(
            [
                {
                    "name": self.name,
                    "length": length,
                    "cmap": self.mpl_LinearSegmentedColormap,
                }
            ]
        )

    def display_r(self, length=9):
        """
        Uses display_palette to display the reversed gradient
        with a number of steps equal to length.

        Args:
            length (int): number of steps to show.
        """
        display_palette(
            [
                {
                    "name": self.name,
                    "length": length,
                    "cmap": self.mpl_LinearSegmentedColormap_r,
                }
            ]
        )

    def display_cvd(self, form="d", length=9):
        """
        Uses display_palette to display the reversed gradient
        with a number of steps equal to length.

        Args:
            length (int): number of steps to show.
        """
        display_palette(
            [
                {
                    "name": self.name + "_" + form,
                    "length": length,
                    "cmap": self.mpl_LinearSegmentedColormap_cvd(form),
                }
            ]
        )

    def plot_gradient(self, figsize=(5, 0.5), *args, **kwargs):
        """
        Uses plot_color_gradient to display the gradient in both color and black and white.

        Args:
            figsize (tuple): width, height of the resulting plot.
        """
        plot_color_gradients(
            {self.name: self.mpl_LinearSegmentedColormap},
            figsize=figsize,
            **kwargs,
        )

    def plot_gradient_cvd(self, form="d", figsize=(5, 0.5), *args, **kwargs):
        """
        Uses plot_color_gradient to display the gradient in both color and black and white.

        Args:
            figsize (tuple): width, height of the resulting plot.
        """
        plot_color_gradients(
            {self.name + "_" + form: self.mpl_LinearSegmentedColormap_cvd(form)},
            figsize=figsize,
            **kwargs,
        )

    def plot_lightness(
        self,
        cmap_type="",
        tickrotation=0,
        markersize=100,
        figsize=(3, 2),
        *args,
        **kwargs,
    ):
        """
        Uses plot_color_lightness to display the lightness of the colors along the gradient.

        Args:
            cmap_type (str): if set to 'linear', puts the name of the colormap
                at the end of the color line
            tickrotation (int): rotation of text label for colormap
            markersize (int): the size of markers to use for plotting the line
            figsize (tuple): width, height of the resulting plot.
        """
        plot_color_lightness(
            {self.name: self.mpl_LinearSegmentedColormap},
            cmap_type=cmap_type,
            tickrotation=tickrotation,
            markersize=markersize,
            figsize=figsize,
            **kwargs,
        )

    def plot_lightness_cvd(
        self,
        form="d",
        cmap_type="",
        tickrotation=0,
        markersize=100,
        figsize=(3, 2),
        *args,
        **kwargs,
    ):
        """
        Uses plot_color_lightness to display the lightness of the colors along the gradient.

        Args:
            cmap_type (str): if set to 'linear', puts the name of the colormap
                at the end of the color line
            tickrotation (int): rotation of text label for colormap
            markersize (int): the size of markers to use for plotting the line
            figsize (tuple): width, height of the resulting plot.
        """
        plot_color_lightness(
            {self.name + "_" + form: self.mpl_LinearSegmentedColormap_cvd(form)},
            cmap_type=cmap_type,
            tickrotation=tickrotation,
            markersize=markersize,
            figsize=figsize,
            **kwargs,
        )
