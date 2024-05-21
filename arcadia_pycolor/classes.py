import matplotlib.colors as mcolors

from arcadia_pycolor.display import swatch


class HexCode(str):
    def __new__(cls, name: str, hex_code: str):
        """
        A HexCode object stores a color's name and HEX code.

        Args:
            name (str): the name of the color
            hex_code (str): the HEX code of the color
        """
        if not mcolors.is_color_like(hex_code):
            raise ValueError(f"Invalid HEX code: {hex_code}")

        obj = str.__new__(cls, hex_code)
        obj.name = name
        obj.hex_code = hex_code
        return obj

    def to_rgb(self):
        return [int(c * 255) for c in mcolors.to_rgb(self.hex_code)]

    def __repr__(self):
        return swatch(self)

    def __str__(self):
        return self.hex_code


class Palette:
    def __init__(self, name: str, colors: list[HexCode]):
        """
        A Palette object stores a collection of Color objects.

        Args:
            name (str): the name of the color palette
            colors (dict): a dictionary where the key is the color's name as a string
                and the value is the HEX code of the color as a string
            OR
            colors (list): a list of Color objects
        """
        self.name = name
        self.colors = colors

    def from_dict(self, colors: dict[str, str]):
        self.colors = [HexCode(name, hex_code) for name, hex_code in colors.items()]

    def __repr__(self):
        from arcadia_pycolor.display import swatch  # imported here to avoid circular import

        longest_name = max(len(color.name) for color in self.colors)

        return "\n".join([swatch(color, min_name_width=longest_name) for color in self.colors])

    def __add__(self, other):
        return Palette(
            name=f"{self.name}+{other.name}",
            colors=self.colors + other.colors,
        )
