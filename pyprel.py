################################################################################
#                                                                              #
# pyprel                                                                       #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides elegant printing utilities in Python.                  #
#                                                                              #
# copyright (C) 2014 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
# REFERENCES                                                                   #
#                                                                              #
# - C. A. Brewer, M. Harrower ColorBrewer.org: An Online Tool for Selecting    #
#   Colour Schemes for Maps, The Cartographic Journal, 40 (1), 27--37          #
#   (01 June 2003)                                                             #
#                                                                              #
################################################################################

version = "2016-01-22T1521Z"

import subprocess
import textwrap

def smuggle(
    module_name = None,
    URL         = None
    ):
    if module_name is None:
        module_name = URL
    try:
        module = __import__(module_name)
        return module
    except:
        try:
            module_string = urllib.urlopen(URL).read()
            module = imp.new_module("module")
            exec module_string in module.__dict__
            return module
        except: 
            raise(
                Exception(
                    "module {module_name} import error".format(
                        module_name = module_name
                    )
                )
            )
            sys.exit()

def terminal_width():
    return int(
        subprocess.Popen(
            ["tput", "cols"],
            stdout = subprocess.PIPE
        ).communicate()[0].decode("utf-8").strip("\n")
    )

def center_string(
    text = None
    ):
    text_list = text.splitlines()
    _terminal_width = terminal_width()
    new_text = ""
    for line in text_list:
        width_of_text = len(line)
        padding_total = _terminal_width - width_of_text
        padding_left  = int(padding_total / 2)
        padding_right = padding_total - padding_left
        new_text =\
            new_text            +\
            padding_left * " "  +\
            line                +\
            padding_right * " " +\
            "\n"
    return new_text

def print_center(
    text = None
    ):
    print(center_string(text = text))

def dictionary_string(
    dictionary  = None,
    indentation = ""
    ):
    string = ""
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            string += "\n{indentation}{key}:".format(
                indentation = indentation,
                key         = key
            )
            string += dictionary_string(
                dictionary  = value,
                indentation = indentation + "  "
            )
        else:
            string += "\n" + indentation + "{key}: {value}".format(
                key   = key,
                value = value
            )
    return string

def print_dictionary(
    dictionary  = None,
    indentation = ""
    ):
    print(dictionary_string(
        dictionary  = dictionary,
        indentation = ""
    ))

def line_string(
    character = "-"
    ):
    _terminal_width = terminal_width()
    line = ""
    for column in range(0, _terminal_width):
        line += character
    return line

def print_line(
    character = "-"
    ):
    print(line_string(
        character = character
    ))

def render_banner(
    text = None,
    font = "slant"
    ):
    pyfiglet = smuggle(module_name = "pyfiglet")
    return pyfiglet.Figlet(font = font).renderText(text)

def render_segment_display(
    text = None
    ):
    segments = (
        {
            " _ ": "02356789",
            "   ": "14"
        },
        {
            "| |": "0",
            "  |": "17",
            " _|": "23",
            "|_|": "489",
            "|_ ": "56"
        },
        {
            "|_|": "068",
            "  |": "147",
            "|_ ": "2",
            " _|": "359"
        }
    )
    segment_display_render = ""
    for row in range(3):
        for character in text:
            for leds, digits in segments[row].items():
                if character in digits:
                    segment_display_render = segment_display_render + leds
        segment_display_render = segment_display_render + "\n"
    return segment_display_render

class Table:

    def __init__(
        self,
        contents                   = None,
        column_width               = None,
        table_width_requested      = None,
        hard_wrapping              = False,
        column_delimiter           = "|",
        row_delimiter              = "-"
        ):
        self.contents              = contents
        self.column_width          = column_width
        self.table_width_requested = table_width_requested
        self.column_delimiter      = column_delimiter
        self.hard_wrapping         = hard_wrapping
        self.number_of_columns     = len(contents[0])
        # Resolve the table dimensions.
        # If a column width is specified, that is given precidence. If a table
        # width is requested, a reasonable column width is derived from it. If
        # no column width is specified and no table width is requested, the
        # requested table width is set to the terminal width.
        if self.column_width is None:
            if self.table_width_requested is None:
                self.table_width_requested = terminal_width()
            self.column_width = (
                self.table_width_requested -\
                (self.number_of_columns + 1) * len(self.column_delimiter)
            ) / self.number_of_columns
        # line gets too long for one concatenation
        self.row_delimiter = self.column_delimiter
        self.row_delimiter +=\
            row_delimiter * (
                self.column_width * max([len(i) for i in self.contents]) +\
                (self.number_of_columns - 1) * len(self.column_delimiter)
            )
        self.row_delimiter +=\
            self.column_delimiter + "\n"

    def wrap_soft(self):
        # Wrap text regarding word boundaries.
        table_string = self.row_delimiter
        # Restructure the table contents to get soft wrapped content for each
        # cell.
        contents_wrapped = [
            [
                textwrap.wrap(column, self.column_width) for column in row
            ] for row in self.contents
        ]
        for row in contents_wrapped:
            for n in range(max([len(i) for i in row])):
                table_string += self.column_delimiter
                for column in row:
                    if n < len(column):
                        table_string += column[n].ljust(self.column_width)
                    else:
                        table_string += " " * self.column_width
                    table_string += self.column_delimiter
                table_string += "\n"
            table_string += self.row_delimiter
        return table_string

    def wrap_hard(self):
        # Wrap text disregarding word boundaries.
        table_string = self.row_delimiter
        for row in self.contents:
            max_wrap = (max([len(i) for i in row]) // self.column_width) + 1
            for r in range(max_wrap):
                table_string += self.column_delimiter
                for column in row:
                    start = r * self.column_width
                    end = (r + 1) * self.column_width
                    table_string +=\
                        column[start:end].ljust(self.column_width) +\
                        self.column_delimiter
                table_string += "\n"
            table_string += self.row_delimiter
        return table_string

    def __str__(self):
        if self.hard_wrapping is True:
            return self.wrap_hard()
        else:
            return self.wrap_soft()

def clamp(x): 
    return max(0, min(x, 255))

def RGB_to_HEX(RGB_tuple):
    # This function returns a HEX string given an RGB tuple.
    r = RGB_tuple[0]
    g = RGB_tuple[1]
    b = RGB_tuple[2]
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

def HEX_to_RGB(HEX_string):
    # This function returns an RGB tuple given a HEX string.
    HEX = HEX_string.lstrip("#")
    HEX_length = len(HEX)
    return tuple(
        int(HEX[i:i + HEX_length // 3], 16) for i in range(
            0,
            HEX_length,
            HEX_length // 3
        )
    )

def mean_color(colors_in_HEX):
    # This function returns a HEX string that represents the mean color of a
    # list of colors represented by HEX strings.
    colors_in_RGB = []
    for color_in_HEX in colors_in_HEX:
        colors_in_RGB.append(HEX_to_RGB(color_in_HEX))
    sum_r = 0
    sum_g = 0
    sum_b = 0
    for color_in_RGB in colors_in_RGB:
        sum_r += color_in_RGB[0]
        sum_g += color_in_RGB[1]
        sum_b += color_in_RGB[2]
    mean_r = sum_r / len(colors_in_RGB)
    mean_g = sum_g / len(colors_in_RGB)
    mean_b = sum_b / len(colors_in_RGB)
    return RGB_to_HEX((mean_r, mean_g, mean_b))

class Palette(list):

    def __init__(
        self,
        name        = None, # string name
        description = None, # string description
        colors      = None, # list of colors
        *args
        ):
        super(Palette, self).__init__(*args)
        self._name          = name
        self._description   = description
        self.extend(colors)

    def name(
        self
        ):
        return self._name

    def set_name(
        self,
        name = None
        ):
        self._name = name

    def description(
        self
        ):
        return self._description

    def set_description(
        self,
        description = None
        ):
        self._description = description

    def extend_palette(
        self,
        minimum_number_of_colors_needed = 15
        ):
        colors = self
        while len(colors) < minimum_number_of_colors_needed:
            for index in range(1, len(colors), 2):
                colors.insert(index, mean_color([colors[index - 1], colors[index]]))
        self = colors

    def save_image_of_palette(
        self,
        filename = "palette.png"
        ):
        save_image_of_palette(
            colors   = self,
            filename = filename
        )

def extend_palette(
    colors = None, # list of HEX string colors
    minimum_number_of_colors_needed = 15
    ):
    while len(colors) < minimum_number_of_colors_needed:
        for index in range(1, len(colors), 2):
            colors.insert(index, mean_color([colors[index - 1], colors[index]]))
    return colors

def save_image_of_palette(
    colors   = None, # list of HEX string colors
    filename = "palette.png"
    ):
    import numpy
    import Image
    scale_x = 200
    scale_y = 124
    data = numpy.zeros((1, len(colors), 3), dtype = numpy.uint8)
    index = -1
    for color in colors:
        index += 1
        color_RGB = HEX_to_RGB(color)
        data[0, index] = [color_RGB[0], color_RGB[1], color_RGB[2]]
    data = numpy.repeat(data, scale_x, axis=0)
    data = numpy.repeat(data, scale_y, axis=1)
    image = Image.fromarray(data)
    image.save(filename)

# Define color palettes.
palettes = []
palettes.append(Palette(
    name        = "palette1",
    description = "primary colors for white background",
    colors      = [
        "#fc0000",
        "#ffae3a",
        "#00ac00",
        "#6665ec",
        "#a9a9a9",
    ]
))
palettes.append(Palette(
    name        = "palette2",
    description = "ATLAS clarity",
    colors      = [
                  "#FEFEFE",
                  "#AACCFF",
                  "#649800",
                  "#9A33CC",
                  "#EE2200",
    ]
))
palettes.append(Palette(
    name        = "palette3",
    description = "ATLAS primary colors",
    colors      = [
                  "#005CFF",
                  "#FFBF00",
                  "#14B814",
                  "#FF0000",
                  "#00FFFF",
                  ]
))
palettes.append(Palette(
    name        = "palette4",
    description = "grayscale",
    colors      = [
                  "#E8E9EC",
                  "#A7AEB6",
                  "#6A747F",
                  "#383D43",
                  "#2A2C30",
                  ]
))
palettes.append(Palette(
    name        = "palette5",
    description = "dusk",
    colors      = [
                  "#F1E1BD",
                  "#EEBA85",
                  "#E18D76",
                  "#9C837E",
                  "#5B7887",
                  ]
))
palettes.append(Palette(
    name        = "palette6",
    description = "sunset",
    colors      = [
                  "#ED4964",
                  "#F69092",
                  "#CC3075",
                  "#5B217B",
                  "#441D54",
                  ]
))
palettes.append(Palette(
    name        = "palette7",
    description = "burnt",
    colors      = [
                  "#000000",
                  "#472718",
                  "#EB5656",
                  "#ECA558",
                  "#F2D773",
                  ]
))
palettes.append(Palette(
    name        = "palette8",
    description = "high contrast",
    colors      = [
                  "#140E11",
                  "#873387",
                  "#41C6D7",
                  "#ECD03E",
                  "#FEEAC6",
                  ]
))
palettes.append(Palette(
    name        = "palette9",
    description = "sequential blue green",
    colors      = [
                  "#f7fcfd",
                  "#e5f5f9",
                  "#ccece6",
                  "#99d8c9",
                  "#66c2a4",
                  "#41ae76",
                  "#238b45",
                  "#006d2c",
                  "#00441b",
                  ]
))
palettes.append(Palette(
    name        = "palette10",
    description = "sequential blue purple",
    colors      = [
                  "#f7fcfd",
                  "#e0ecf4",
                  "#bfd3e6",
                  "#9ebcda",
                  "#8c96c6",
                  "#8c6bb1",
                  "#88419d",
                  "#810f7c",
                  "#4d004b",
                  ]
))
palettes.append(Palette(
    name        = "palette11",
    description = "sequential green blue",
    colors      = [
                  "#f7fcf0",
                  "#e0f3db",
                  "#ccebc5",
                  "#a8ddb5",
                  "#7bccc4",
                  "#4eb3d3",
                  "#2b8cbe",
                  "#0868ac",
                  "#084081",
                  ]
))
palettes.append(Palette(
    name        = "palette12",
    description = "sequential orange red",
    colors      = [
                  "#fff7ec",
                  "#fee8c8",
                  "#fdd49e",
                  "#fdbb84",
                  "#fc8d59",
                  "#ef6548",
                  "#d7301f",
                  "#b30000",
                  "#7f0000",
                  ]
))
palettes.append(Palette(
    name        = "palette13",
    description = "sequential purple blue",
    colors      = [
                  "#fff7fb",
                  "#ece7f2",
                  "#d0d1e6",
                  "#a6bddb",
                  "#74a9cf",
                  "#3690c0",
                  "#0570b0",
                  "#045a8d",
                  "#023858",
                  ]
))
palettes.append(Palette(
    name        = "palette14",
    description = "sequential purple blue green",
    colors      = [
                  "#fff7fb",
                  "#ece2f0",
                  "#d0d1e6",
                  "#a6bddb",
                  "#67a9cf",
                  "#3690c0",
                  "#02818a",
                  "#016c59",
                  "#014636",
                  ]
))
palettes.append(Palette(
    name        = "palette16",
    description = "sequential purple red",
    colors      = [
                  "#f7f4f9",
                  "#e7e1ef",
                  "#d4b9da",
                  "#c994c7",
                  "#df65b0",
                  "#e7298a",
                  "#ce1256",
                  "#980043",
                  "#67001f",
                  ]
))
palettes.append(Palette(
    name        = "palette16",
    description = "sequential red purple",
    colors      = [
                  "#fff7f3",
                  "#fde0dd",
                  "#fcc5c0",
                  "#fa9fb5",
                  "#f768a1",
                  "#dd3497",
                  "#ae017e",
                  "#7a0177",
                  "#49006a",
                  ]
))
palettes.append(Palette(
    name        = "palette17",
    description = "sequential yellow green",
    colors      = [
                  "#ffffe5",
                  "#f7fcb9",
                  "#d9f0a3",
                  "#addd8e",
                  "#78c679",
                  "#41ab5d",
                  "#238443",
                  "#006837",
                  "#004529",
                  ]
))
palettes.append(Palette(
    name        = "palette18",
    description = "sequential yellow green blue",
    colors      = [
                  "#ffffd9",
                  "#edf8b1",
                  "#c7e9b4",
                  "#7fcdbb",
                  "#41b6c4",
                  "#1d91c0",
                  "#225ea8",
                  "#253494",
                  "#081d58",
                  ]
))
palettes.append(Palette(
    name        = "palette19",
    description = "yellow orange brown",
    colors      = [
                  "#ffffe5",
                  "#fff7bc",
                  "#fee391",
                  "#fec44f",
                  "#fe9929",
                  "#ec7014",
                  "#cc4c02",
                  "#993404",
                  "#662506",
                  ]
))
palettes.append(Palette(
    name        = "palette20",
    description = "sequential yellow orange red",
    colors      = [
                  "#ffffcc",
                  "#ffeda0",
                  "#fed976",
                  "#feb24c",
                  "#fd8d3c",
                  "#fc4e2a",
                  "#e31a1c",
                  "#bd0026",
                  "#800026",
                  ]
))
palettes.append(Palette(
    name        = "palette21",
    description = "qualitative Paired",
    colors      = [
                  "#a6cee3",
                  "#1f78b4",
                  "#b2df8a",
                  "#33a02c",
                  "#fb9a99",
                  "#e31a1c",
                  "#fdbf6f",
                  "#ff7f00",
                  "#cab2d6",
                  "#6a3d9a",
                  "#ffff99",
                  "#b15928",
                  ]
))
palettes.append(Palette(
    name        = "palette22",
    description = "qualitative Set3",
    colors      = [
                  "#8dd3c7",
                  "#ffffb3",
                  "#bebada",
                  "#fb8072",
                  "#80b1d3",
                  "#fdb462",
                  "#b3de69",
                  "#fccde5",
                  "#d9d9d9",
                  "#bc80bd",
                  "#ccebc5",
                  "#ffed6f",
                  ]
))

def save_images_of_palettes():
    for index, palette in enumerate(palettes):
        save_image_of_palette(
            colors   = palette,
            filename = "palette_{index}.png".format(index = index + 1)
        )

def access_palette(
    name = "palette1"
    ):
    for palette in palettes:
        if palette.name() == name:
            return palette
    return None
