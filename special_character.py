#!/usr/bin/python3
"""
Created at 17:42:56 on dimanche 22-03-2020

@author: Étienne

Name:
-----
special_character.py

Description:
------------
Transform special character from Markdown to LaTeX.
It also convert the escape lines.
"""
import re


class SpecialCharacter2LaTeX():
    """
    A class to transform diverse character from Markdown to LaTeX.
    The given character are the one representing:
    "\ ` * _ { } [ ] ( ) # + - . !"
    It also handle double spaces at the end of lines to transform is in return line.

    Parameters:
    -----------
    text (str): The text in markdown format taht we want to transcript.

    Attributes:
    -----------
    text (str): The text in markdown format that we want to transcript.
    lines (str): The previous text split into a list of line.
    translation (str): The translation of 'text' into LaTeX.
    """

    def __init__(self, text):
        self.text = text
        self.translation = self.change_characters()

    def change_characters(self, text=None):
        # TODO: offer functionality all special character in LaTeX without bug
        # TODO: The main current problem is for backslashs and curly brackets
        if text is None:
            text = self.text
        # No need to translate '_', '{', '}', '#'
        # text = re.sub(re.escape('\\\\'), '\\\\textbackslash',
        #              text)  # Translate the backslashs.
        text = re.sub(re.escape('\`'), '`', text)  # Translate the accents.
        text = re.sub(re.escape('\*'), '*', text)  # Translate the stars.
        text = re.sub(re.escape('\['), '[',
                      text)  # Translate the left square brackets
        text = re.sub(re.escape('\]'), ']',
                      text)  # Translate the right square brackets
        text = re.sub(re.escape('\('), '(',
                      text)  # Translate the left round brackets
        text = re.sub(re.escape('\)'), ')',
                      text)  # Translate the right round brackets
        text = re.sub(re.escape('\+'), '+', text)  # Translate the pluses.
        text = re.sub(re.escape('\-'), '-', text)  # Translate the minuses.
        text = re.sub(re.escape('\.'), '.', text)  # Translate the points.
        text = re.sub(re.escape('\!'), '!',
                      text)  # Translate the exclamation marks.
        text = re.sub('%', '\\%', text)  # Translate the percents.
        text = re.sub('\\$', '\\$', text)  # Translate the percents.
        text = re.sub('&', '\\&', text)  # Translate the amperstand.
        # text = re.sub('{', '\\{', text)  # Translate the left curly brackets.
        # text = re.sub('}', '\\}', text)  # Translate the right curly brackets.

        text = re.sub('  $', '\\\\\\\\', text)  # Tranlate return to line.
        text = re.sub('  \\n', '\\\\\\\\', text)  # Tranlate return to line.
        return text


text = """This is a **text** with a bit of emphasis.
We have 4 \+ 2 = 3 \* \(3 \-1\)
This a B\#, not C% {Ok ?}, \[ Yes, I think so\]\!.
OK, This file\_name contains no & and no $."""
