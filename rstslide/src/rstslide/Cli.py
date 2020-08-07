#!/usr/bin/env python3
import os, sys, codecs, argparse

from .Parser import Parser
from ._version import __version__ as version


class Cli:

    @staticmethod
    def run():
        # Test the presence of Pygments
        isPygments = False
        try:
            from pygments.styles import STYLE_MAP
            isPygments = True
        except BaseException:
            print("Pygments is not installed, code blocks won't be highlighted")

        # Allowed themes and transitions
        themes = ['default', 'beige', 'night']
        transitions = ['default', 'cube', 'page', 'concave', 'zoom', 'linear', 'fade', 'none']
        options = ['input_file', 'output_file', 'theme', 'transition', 'mathjax_path', 'pygments_style']
        if isPygments:
            pygments_styles = STYLE_MAP.keys()

        # Define arguments
        argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        argparser.description = "reStructuredText to HTML slide generator using reveal.js."
        argparser.add_argument("input_file", help="The name of the reStructuredText file to parse.")
        argparser.add_argument("-o", "--output_file", type=str, help="The name of the HTML file to produce (by default the same basename as the input file with a .html suffix.")
        argparser.add_argument("-u", "--update_file", type=str, help="The name of a previously generated HTML file for updating only the headers part.")
        argparser.add_argument('-v', '--version', action='version', version='rstslide ' + version)

        resource_mgmt_choices = {
            'central': "Use centralized resources from where rstslide is installed",
            'local': "Copy needed resources to a directory <outfile>-resources",
            'inline': "Embedd all resources into a single file HTML document"
        }

        argparser.add_argument("-r", "--resources", type=str, choices=resource_mgmt_choices,
                               help="How to handle resources that the presentation is dependent on:\n" +
                               '\n'.join("{}: {}".format(key, value) for key, value in resource_mgmt_choices.items()))
        args = argparser.parse_args()

        # input file name
        filename = args.input_file
        # output file name
        if args.output_file:
            output_file = args.output_file
        else:
            output_file = filename.split('.')[-2]+'.html'

        # Create the RST parser and create the slides
        parser = Parser(input_file=filename, output_file=output_file)

        parser.create_slides()
