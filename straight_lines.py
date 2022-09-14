#!/usr/bin/python3
"""
Created at 20:26:32 on mercredi 11-12-2019

@author: Étienne

Name:
-----
straight_lines.py

Description:
------------
Transform the line from the markdown format into lines in LaTeX code.
"""


class StraightLines2LaTeX():
    """
    A class to transform the line from the markdown format into lines in LaTeX code.
    It first detect in the markdown code where there is such line.
    Then it transform it into a \\hrule for LaTeX to understand

    Parameters:
    -----------
    text (str): The text in markdown format taht we want to transcript.

    Attributes:
    -----------
    text (str): The text in markdown format that we want to transcript.
    lines (str): The previous text split into a list of line.
    straight_lines (list): A list containing the indices of the lines with a straight line.
    translation (str): The translation of 'text' into LaTeX.
    """

    def __init__(self, text):
        self.text = text
        self.lines = text.split('\n')
        self.straight_lines = []
        self.translation = self.lines_2_latex()

    def detect_lines(self, text=None):
        """
        Detect the lines containing straight line in markdown format in the text
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        self.straight_lines = []
        for ind, line in enumerate(lines):
            if line and not line.strip(' _'):
                self.straight_lines.append(ind)
            if line and (not line.strip(' -') or not line.strip(' *')):
                if ind > 0 and not lines[ind - 1]:
                    self.straight_lines.append(ind)

    def translate_lines(self, text=None):
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        processed_lines = []
        for ind, line in enumerate(lines):
            if ind in self.straight_lines:
                if ind > 0:
                    add_lines = processed_lines[-1] + "\\\\"
                    del processed_lines[-1]
                    processed_lines.append(add_lines)
                processed_lines.append("\\hrule")
            else:
                processed_lines.append(line)
        return processed_lines

    def lines_2_latex(self, text=None):
        self.detect_lines(text)
        processed_lines = self.translate_lines(text)
        return '\n'.join(processed_lines)
