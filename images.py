#!/usr/bin/python3
"""
Created at 20:26:32 on mercredi 11-12-2019

@author: Étienne

Name:
-----
images.py

Description:
------------
Translate images from the markdown format to LaTeX
"""

import re
import urllib3 as url


class Images2LaTeX():
    """
    A class to convert the images from the markdown format to LaTeX code.

    Parameters:
    -----------
    text (str): The text in markdown format, that we want to transcript into LaTeX.

    Attributes:
    -----------
    text (str): The text in markdown format that we want to transcript into LaTeX.
    lines (str): The previous text split into a list of line.
    images (dict): A dictionary containing information about the different images in the text.
    reference (dict): A dictionary containing information about the reference of the images
    translation (str): The translation of 'text' into LaTeX.
    """
    base_directory = "/mnt/etienne/detente/python/marklatex/data/"

    def __init__(self, text, directory=base_directory):
        self.text = text
        self.lines = text.split('\n')
        self.directory = directory
        self.images = dict()
        self.reference = dict()
        self.ind_reference = []
        self.packages = dict()
        self.translation = self.images_2_latex()

    def detect_images(self, text=None):
        """
        This function detect the lines which have to see with images.
        It adds all the images find to the self.images object,
        and all reference to images to the self.reference object.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        find_paren = re.compile("^!\[.+\]\(.+\)$")
        find_brace = re.compile("^!\[.+\]\[.+\]$")
        find_colon = re.compile("^\[.+\]:")

        self.ind_reference = []
        self.images = dict()
        self.reference = dict()
        for ind, line in enumerate(lines):
            if find_brace.findall(line):
                find_image = re.compile('\[.*?\]')
                description, reference_name = find_image.findall(line)
                description = description[1:-1]
                reference_name = reference_name[1:-1]
                self.images[ind] = ('reference', description, reference_name)
            elif find_paren.findall(line):
                find_description = re.compile('\[.*\]')
                find_image = re.compile('\(.*\)')
                description = find_description.findall(line)[0][1:-1]
                image_name = find_image.findall(line)[0][1:-1]
                self.images[ind] = ('direct', description, image_name)
            elif find_colon.findall(line):
                line_no_space = re.sub(" ", "", line)
                ind_location = line_no_space.index(":")
                location = line_no_space[ind_location + 1:]
                self.reference[find_colon.findall(line)[0][1:-2]] = location
                self.ind_reference.append(ind)

    def download_image(self, image_coord, image_name):
        """
        Download the images needed, and put it in the 'self.directory' folder
        """
        connection = url.PoolManager()
        file_download = connection.request('GET', image_coord)
        with open(image_name, 'wb') as fileo:
            fileo.write(file_download.data)

    def find_name(self, image):
        """
        Find the name of an image, and download it if necessary.
        """
        if image[0] == 'direct':
            if 'https://' in image[2] or 'http://' in image[
                    2] or "www." == image[2][:4]:
                image_coord = image[2]
                image_name = self.directory + image[2].split('/')[-1]
                self.download_image(image[2], image_name)
            else:
                image_name = image[2]
            return image_name, image[1]
        elif image[0] == 'reference':
            if image[2] not in self.reference:
                raise ValueError(
                    "{} is not in the set of possible references".format(
                        image[2]))
            image_coord = self.reference[image[2]]
            if 'https://' in image_coord or 'http://' in image_coord or "www." == image_coord[:
                                                                                              4]:
                image_name = self.directory + image_coord.split('/')[-1]
                self.download_image(image_coord, image_name)
            else:
                image_name = image_coord
            return image_name, image[1]
        else:
            raise ValueError(
                "Image should be a 'reference' or a 'direct' image")

    def translate_images(self, text=None):
        """
        Translate the text from markdown to LaTeX.
        """
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        processed_lines = []
        if self.images:
            self.packages['subcaption'] = None
            self.packages['graphicx'] = None
        for ind, line in enumerate(lines):
            if ind in self.images:
                processed_lines.append("\\begin{figure}[h]")
                image_name, image_caption = self.find_name(self.images[ind])
                processed_lines.append(
                    "\\includegraphics[width=\\textwidth]{{{}}}".format(
                        image_name))
                processed_lines.append("\\caption{{{}}}".format(image_caption))
                processed_lines.append("\\end{figure}")
            else:
                processed_lines.append(line)
        return processed_lines

    def images_2_latex(self, text=None):
        self.detect_images(text)
        translation = self.translate_images(text)
        return '\n'.join(translation)

    def delete_reference(self, text=None):
        if text is None:
            lines = self.lines
        else:
            lines = text.split('\n')
        for ind in sorted(self.ind_reference)[::-1]:
            del lines[ind]
        return '\n'.join(lines)
