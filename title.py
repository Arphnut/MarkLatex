"""
Created at 12:44:37 on mercredi 11-12-2019

@author: Étienne

Name:
-----
title.py

Description:
------------
Convert a title from the Markdown format to LaTeX
"""


class Title2LaTeX():
    """
    Detect the use of titles un a file written in markdown format.
    Then it can translate them into LaTeX code.
    This class is done only to detect the titles.

    Attributes:
    -----------
    text (str): The text in markdown format that we want to transcript into LaTeX.

    Parameters:
    -----------
    text (str): The text in markdown format that we want to transcript into LaTeX.
    lines (str): The previous text split into a list of line.
    titles (dict): A dictionary containing information about the different titles in the text.
    translation (str): The translation of 'text' into LaTeX.
    """

    def __init__(self, text):
        self.text = text
        self.lines = text.split('\n')
        self.titles = dict()
        self.translation = self.title_2_latex()

    list_conversion = ['Huge', 'huge', 'LARGE', 'Large', 'large', 'normalsize']

    @staticmethod
    def count_hashtag(line):
        """
        Count the number of hashtags in the beginning of the line
        """
        nb = 0
        length = len(line)
        while nb < length and line[nb] == '#':
            nb += 1
        return nb

    def detect_title(self, text=None):
        """
        Detect the titles in the text, with their level.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        self.titles = dict()
        for ind, line in enumerate(lines):
            nb_hash = self.count_hashtag(line)
            if 0 < nb_hash <= 6:
                # If there is between 1 and 6 hashtag, it is a title
                self.titles[ind] = (nb_hash, 'hashtag')
            elif line and not line.strip(' ='):
                # If there is only space and equal sign, it is a title
                self.titles[ind] = (0, 'hyphen')
            elif line and not line.strip(' -'):
                # If there is only space and hyphen, it is a title
                self.titles[ind] = (1, 'hyphen')

    def translate_title(self, text=None):
        """
        Translate the titles in the text from markdown format to LaTeX format.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        processed_lines = []
        for ind, line in enumerate(lines):
            if ind in self.titles:  # If we have a tilte
                if self.titles[ind][1] == 'hashtag':
                    # If it is using a hashtag, we make the text big enough, and bold it
                    nb_hashtag = self.titles[ind][0]
                    line = line[nb_hashtag:]
                    line = "\\textbf{\\" + self.list_conversion[
                        nb_hashtag] + "{" + line + "}}"
                elif self.titles[ind][
                        1] == 'hyphen' and ind - 1 not in self.titles and ind >= 1:
                    # If it is using sign in the following lines, make the previous line big enough
                    # and bold it, plus we delete the line.
                    del processed_lines[-1]
                    line = lines[ind - 1]
                    line = "\\textbf{\\" + self.list_conversion[
                        self.titles[ind][0]] + "{" + line + "}}\\\\"
            processed_lines.append(line)
        return processed_lines

    def title_2_latex(self, text=None):
        self.detect_title(text)
        processed_lines = self.translate_title(text)
        return '\n'.join(processed_lines)
