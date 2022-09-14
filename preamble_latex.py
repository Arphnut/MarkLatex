#!/usr/bin/python3
"""
Created at 15:36:26 on vendredi 06-12-2019

@author: Étienne

Name:
-----
latexPreamble.py

Description:
------------
A class to create a preamble in LaTeX.
"""


class Preamble2LaTeX():
    """
    This class create a preamble in Latex.
    It contains:
    - The document class with its options
    - The needed packages
    - The data for the title
    - All newtheorem, newcommand, and other useful commands.

    Parameters:
    -----------
    title (str): The title of the document.
    author (str): The author of the document.
    date (str): The date of the document.
    documentclass (dict): A dictionary containing the options and doctype of the document.
    packages (dict): A dictionary containing the packages and their options.

    Attributes:
    -----------
    title (str): The title of the document.
    author (str): The author of the document.
    date (str): The date of the document.
    documentclass (dict): A dictionary containing the options and doctype of the document.
    packages (dict): A dictionary containing the packages and their options.
    commands (str): The string already made of the commands needed in the document.
                    (to be changed to a dictionary of a class).
    """
    base_documentclass = {"options": ("a4paper", "11pt"), "doctype": "article"}
    base_packages = {"amsmath": None}

    def __init__(
            self,
            title=None,
            author=None,
            date="\\today",
            documentclass=base_documentclass,
            packages=base_packages,
    ):
        self._title = title
        self._author = author
        self._date = date
        self.documentclass = documentclass
        if packages is None:
            packages = dict()
        self._packages = packages
        self.commands = None
        self.to_latex = self.preamble2Latex()

    def __repr__(self):
        """
        Return the object of the class to print.
        """
        to_string = "An object of PreambleLatex\n"
        to_string += "Title: {}\nAuthor: {}\nDate: {}\n".format(
            self._title, self._author, self._date)
        to_string += "Document Class: {}\nPackages: {}\nCommand: {}".format(
            self.documentclass, self._packages, self._commands)
        return to_string

    def add_packages(self, package):
        """
        This function add a package to the packages list.

        Parameters:
        -----------
        package (str): A package is represented by it's name.
        """
        if type(package) == dict:
            for key in package.keys():
                self._packages[key] = package[key]
        elif type(package) == str:
            self._packages[package] = None
        else:
            raise TypeError("'package' should be of type dict or str.")

    def delete_packages(self, package):
        """
        This function delete a package from the list of all packages.

        Parameters:
        -----------
        package (str): A package is represented by it's name.
        """
        if package in self.packages:
            del self._packages[package]
        else:
            print(
                "{} was already not part of the used packages".format(package))

    def _get_packages(self):
        """
        We don't want the user to change the 'packages' attributes how he wants.
        Thus, we tell him he can't, and he should use self.add_packages and self.delete_packages
        """
        print(
            "You shouldn't play with this attributes directly.\n"
            "You should use the 'add_packages' and 'delete_packages' functions."
        )

    def _set_packages(self, packages):
        """
        Set the 'packages' attributes of the object.
        If 'packages' is a list of packages, it change the value of the attribute.
        If 'packages' is a single package (in the form of a string), it add it to the previous list
        of packages
        """
        if type(packages) == dict:
            packages_str = True
            for package in packages.keys():
                if type(package) != str:
                    packages_str = False
                    break
            if packages_str:
                self._packages = packages
            else:
                raise TypeError("All packages should be of type 'str'")
        elif type(packages) == str:
            print("Adding {} to the list of packages".format(packages))
            print(
                "Use an object of type 'dict' and not 'str' if you want to remove all the "
                "previous packages at the same time")
            self.add_packages(packages)
        else:
            raise TypeError("All packages should be of type 'str'")

    packages = property(_get_packages, _set_packages)

    def preamble2Latex(self):
        """
        Transform all the preamble into a Latex text.
        """
        to_latex = ""
        to_latex += self.documentclass2Latex()
        to_latex += self.package2Latex() + "\n"
        to_latex += self.title2Latex() + "\n"
        to_latex += self.command2Latex()
        return to_latex

    def documentclass2Latex(self):
        """
        Convert the "documentclass" attribute into a LaTeX code line.
        """
        to_string = "\\documentclass["
        for opt in self.documentclass['options']:
            to_string += "{}, ".format(opt)
        to_string = to_string[:-2]
        to_string += "]{{{}}}\n".format(self.documentclass['doctype'])
        return to_string

    def package2Latex(self):
        """
        Convert the "_packages" attributes into LaTeX code lines
        """
        to_string = ""
        for package in self._packages.keys():
            to_string += "\\usepackage"
            if self._packages[package] is not None:
                to_string += "[{}]".format(self._packages[package])
            to_string += "{{{}}}\n".format(package)
        return to_string

    def title2Latex(self):
        """
        Convert the title, author and date into LaTeX code lines.
        """
        to_string = ""
        if self._title is not None:
            to_string += "\\title{{{}}}\n".format(self._title)
        if self._author is not None:
            to_string += "\\author{{{}}}\n".format(self._author)
        if self._date is not None:
            to_string += "\\date{{{}}}\n".format(self._date)
        return to_string

    def command2Latex(self):
        """
        Convert the "commands" attribute into commands in a LaTeX document.

        TODO:
        -----
        So far, "_commands" is seen as an already well written command, because its too long
        to make something clean.
        It should instead be kept as a dictionary, or a class, to have a clean way of adding
        all the differents commands
        (newcommand, newtheorem (with plain style), and DeclarMathOperators).
        """
        if self.commands is None:
            return ""
        return self.commands
