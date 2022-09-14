#!/usr/bin/python3
"""
Created at 10:40:38 on samedi 22-02-2020

@author: Étienne

Name:
-----
marklatex.py

Description:
------------
This is the main file of the marklatex module.
It contains the 'Markdown2LaTeX' class.
This class  will convert a file in markdown format to a file in LaTeX.
"""

from straight_lines import StraightLines2LaTeX
from effects import Effects2LaTeX
from images import Images2LaTeX
from links import Links2LaTeX
from preamble_latex import Preamble2LaTeX
from title import Title2LaTeX
from special_character import SpecialCharacter2LaTeX


def change_extension(filename, extension):
    return filename[:filename.rindex('.') + 1] + extension


class Markdown2LaTeX():
    """
    This class translate a whole markdown file from the markdown format to the LaTeX one.
    It can translate the titles, images, links, and multiple other things.
    """

    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as filer:
            self.markdown = filer.read()
        self.latex = ""  # self.translate()

    def translate(self):
        translation = self.markdown
        preamble = Preamble2LaTeX()
        title = Title2LaTeX(translation)
        straight_lines = StraightLines2LaTeX(title.translation)
        effects = Effects2LaTeX(straight_lines.translation)
        images = Images2LaTeX(effects.translation)
        preamble.add_packages(images.packages)
        links = Links2LaTeX(images.translation)
        special_character = SpecialCharacter2LaTeX(links.delete_reference())
        preamble.add_packages(links.packages)
        begin = preamble.preamble2Latex() + "\n\\begin{document}\n"
        end = "\n\\end{document}\n"
        return begin + special_character.translation + end

    def save(self, filename=None):
        latex = self.translate()
        if filename is None:
            filename = change_extension(self.filename, 'tex')
        with open(filename, 'w') as filew:
            filew.write(latex)
