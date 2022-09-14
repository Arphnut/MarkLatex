#!/usr/bin/python3
"""
Created at 11:29:22 on lundi 09-12-2019

@author: Étienne

Name:
-----
effects.py

Description:
------------
This files treat of all the different effects that can be found in markdown text.
nIt then give elements to transform them into LaTeX code.
"""


class Effects2LaTeX():
    """
    Detect the effects in a file written in the markdown format.
    Then it can translate them into a LaTeX code.
    This class is only to detect the italic and bold effect.

    Attributes:
    -----------
    text (str): A text. We would like to detext the different effects in this text.

    Parameters:
    -----------
    text (str): A text. We would like to detext the different effects in this text.
    effects (dict): a dictionnary containing the placement of the different effects in the text.
    translation (str): The translation in LaTeX of the markdown format.
    """

    def __init__(self, text):
        self.text = text
        self.effects = {'bold': [], 'italic': []}
        self.translation = self.effects_2_latex()

    def detect_bold(self, text=None):
        """
        Detect boldness in the markdown format (** or __ not preceded by a backslash).
        """
        if text is None:
            text = self.text
        list_bold = []
        ind = 0
        length = len(text)
        while ind < length - 1:
            letter = text[ind:ind + 2]
            if letter == '**' or letter == '__':
                # If we got to asterisks in a row
                try:
                    if text[ind - 1] == '\\':
                        # We do nothing if the first one is preceded by a backslash
                        ind += 1
                        continue
                except IndexError:
                    pass
                # Else these asterisks denote the beginning or the end of a bold section.
                list_bold.append(ind)
            ind += 1

        nb_bold = len(list_bold)
        assert (nb_bold % 2 == 0)  # We check if every bold section is closed
        self.effects['bold'] = []
        for i in range(nb_bold // 2):
            self.effects['bold'].append(
                [list_bold[2 * i], list_bold[2 * i + 1]])

    def detect_italic(self, text=None):
        """
        Detect italic in the markdown format (* or _ not preceded by a backslash).
        """
        if text is None:
            text = self.text
        list_italic = []
        ind = 0
        length = len(text)
        while ind < length:
            letter = text[ind]
            if letter == '*' or letter == '_':
                # If we got to asterisks in a row
                try:
                    if text[ind - 1] == '\\':
                        # We do nothing if the first one is preceded by a backslash
                        ind += 1
                        continue
                    if text[ind + 1] == letter:
                        # In the case we haven't already changed all the bold section,
                        # there may still be some of them. We dont want to count them as italic one
                        ind += 2
                        continue
                except IndexError:
                    pass
                # Else these asterisks denote the beginning or the end of an italic section.
                list_italic.append(ind)
            ind += 1

        nb_italic = len(list_italic)
        assert (nb_italic % 2 == 0
                )  # We check if every italic section is closed
        self.effects['italic'] = []
        for i in range(nb_italic // 2):
            self.effects['italic'].append(
                [list_italic[2 * i], list_italic[2 * i + 1]])

    def translate_bold(self, text=None, ret=False):
        """
        translate the bold format from markdown into the one for LaTeX.

        Parameters:
        -----------
        text (str): The text to translate. If None, we use 'self.text'
        ret (boolean): If True, return the text, else, change self.translation accordingly.
        """
        if text is None:
            text = self.text

        list_bold = self.effects['bold']
        nb_bold = len(list_bold)  # The number of bold section
        piece_text = []
        for i in range(nb_bold):
            piece_text.append(text[list_bold[i][0]:list_bold[i][1] + 2])
        for i, el in enumerate(piece_text):
            piece_text[i] = "\\textbf{" + el[2:-2] + "}"

        translation = text[0:list_bold[0][0]]
        for i in range(nb_bold - 1):
            translation += piece_text[i]
            translation += text[list_bold[i][1] + 2:list_bold[i + 1][0]]
        translation += piece_text[-1]
        translation += text[list_bold[-1][1] + 2:]

        if ret:
            return translation
        self.translation = translation

    def translate_italic(self, text=None, ret=False, verify_bold=True):
        """
        translate the italic format from markdown into the one for LaTeX.

        Parameters:
        -----------
        text (str): The text to translate. If None, we use 'self.text'
        ret (boolean): If True, return the text, else, change self.translation accordingly.
        verify_bold (boolean): Verify if the bold already has been translated
                              (otherwise, the algorithm won't work).
        """
        if text is None:
            text = self.text
        translation = ""

        if verify_bold:
            list_bold = self.effects['bold']
            self.detect_bold(text)
            if len(self.effects['bold']) > 0:
                self.effects['bold'] = list_bold
                raise AssertionError(
                    "There should be no more bold in the markdown text at this point"
                )
            self.effects['bold'] = list_bold

        list_italic = self.effects['italic']
        nb_italic = len(list_italic)  # The number of italic section
        piece_text = []
        for i in range(nb_italic):
            piece_text.append(text[list_italic[i][0]:list_italic[i][1] + 1])
        for i, el in enumerate(piece_text):
            piece_text[i] = "\\textit{" + el[1:-1] + "}"

        translation = text[0:list_italic[0][0]]
        for i in range(nb_italic - 1):
            translation += piece_text[i]
            translation += text[list_italic[i][1] + 1:list_italic[i + 1][0]]
        translation += piece_text[-1]
        translation += text[list_italic[-1][1] + 1:]

        if ret:
            return translation
        self.translation = translation

    def effects_2_latex(self):
        """
        Find the position of the effects, and transform them into LaTeX code.
        """
        self.detect_bold()
        semi_translation = self.translate_bold(ret=True)
        self.detect_italic(semi_translation)
        return self.translate_italic(semi_translation, ret=True)
