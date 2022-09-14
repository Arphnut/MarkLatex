#!/usr/bin/python3
"""
Created at 16:31:31 on dimanche 09-02-2020

@author: Étienne

Name:
-----
links.py

Description:
------------
Translate links from the markdown to LaTeX
"""

import re


class Links2LaTeX():
    """
    A class to convert the links from the markdown format to LaTeX code.

    Parameters:
    -----------
    text (str): The text in markdown format, that we want to transcript into LaTeX.

    Attributes:
    -----------
    text (str): The text in markdown format, that we want to transcript into LaTeX.
    lines (str): The previous 'text' variable, split into a list of line.
    links (dict): A dictionary containing information about the links in the text.
    reference (dict): A dictionary containing information about the reference to some links.
    translation (str): The translation of 'text' into LaTeX.
    """

    def __init__(self, text):
        self.text = text
        self.lines = text.split('\n')
        self.links = dict()
        self.reference = dict()
        self.ind_reference = []
        self.packages = dict()
        self.translation = self.links_2_latex(self.text)

    def detect_direct_links(self, text=None):
        """
        This function detext the lines containing links.
        It adds all the links to the self.links object,
        and all reference to liks to the self.reference object.

        Remark:
        -------
        All images should already be removed from the file !!!
        Otherwise, images will be dealt as links.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        find_paren = re.compile("\[.+\]\(.+\)")
        self.links = dict()
        for ind, line in enumerate(lines):
            for link in find_paren.findall(line):
                if '!' + link not in line:
                    find_description = re.compile('\[.*?\]')
                    find_link = re.compile('\(.*?\)')
                    description = find_description.findall(link)[0][1:-1]
                    link_name = find_link.findall(link)[0][1:-1]
                    self.links[ind] = ('direct', description, link_name)

    def detect_referenced_link(self, text=None):
        """
        This function detext the lines containing links.
        It adds all the links to the self.links object,
        and all reference to liks to the self.reference object.

        Remark:
        -------
        All images should already be removed from the file !!!
        Otherwise, images will be dealt as links.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        find_brace = re.compile("\[.+?\]\[.+?\]")
        self.links = dict()
        for ind, line in enumerate(lines):
            for link in find_brace.findall(line):
                if '!' + link not in line:
                    find_link = re.compile('\[.*?\]')
                    description, reference_name = find_link.findall(link)
                    description = description[1:-1]
                    reference_name = reference_name[1:-1]
                    self.links[ind] = self.links.setdefault(
                        ind, []) + [('reference', description, reference_name)]

    def detect_reference(self, text=None):
        """
        This function detext the lines containing links.
        It adds all the links to the self.links object,
        and all reference to liks to the self.reference object.

        Remark:
        -------
        All images should already be removed from the file !!!
        Otherwise, images will be dealt as links.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        find_colon = re.compile("^\[.+\]:")
        self.reference = dict()
        self.ind_reference = []
        for ind in range(len(lines)):
            line = lines[ind]
            if find_colon.findall(line):
                line_no_space = re.sub(" ", "", line)
                ind_location = line_no_space.index(":")
                location = line_no_space[ind_location + 1:]
                self.reference[find_colon.findall(line)[0][1:-2]] = location
                self.ind_reference.append(ind)

    def translate_direct_links(self, text=None):
        """
        Translate the text from markdown to LaTeX.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        processed_lines = []
        if self.links:
            self.packages['hyperref'] = None
        for ind, line in enumerate(lines):
            if ind in self.links:
                link = self.links[ind]
                if link[0] == 'direct':
                    processed_lines.append(
                        re.sub(
                            r'\[{}\]\({}\)'.format(link[1], link[2]),
                            r'\\href{{{0}}}{{{1}}}'.format(link[2],
                                                           link[1]), line))
            else:
                processed_lines.append(line)
        return processed_lines

    def translate_referenced_links(self, text=None):
        """
        Translate the text from markdown to LaTeX.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        processed_lines = []
        if self.links:
            self.packages['hyperref'] = None
        for ind, line in enumerate(lines):
            if ind in self.links:
                for link in self.links[ind]:
                    if link[0] == 'reference':
                        if link[2] not in self.reference:
                            raise ValueError(
                                "{} is not in the set of possible references".
                                format(link[2]))
                        link_ref, link_name = self.reference[link[2]], link[1]
                        line = re.sub(
                            r'\[{}\]\[{}\]'.format(link[1], link[2]),
                            r'\\href{{{0}}}{{{1}}}'.format(
                                link_ref, link_name), line)
                processed_lines.append(line)

            else:
                processed_lines.append(line)
        return processed_lines

    def links_2_latex(self, text=None):
        self.detect_direct_links(text)
        translation = '\n'.join(self.translate_direct_links(text))
        self.detect_referenced_link(translation)
        self.detect_reference(translation)
        translation = self.translate_referenced_links(translation)
        return '\n'.join(translation)

    def delete_reference(self, text=None):
        self.detect_reference(text)
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        for ind in sorted(self.ind_reference)[::-1]:
            del lines[ind]
        return '\n'.join(lines)
