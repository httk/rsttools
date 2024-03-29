#!/usr/bin/env python3
import os, sys, codecs, argparse

try:
    import http.server as httpserver, socketserver
except ImportError:
    import SimpleHTTPServer as httpserver, SocketServer as socketserver

from .SlidesParser import SlidesParser
from .HandoutParser import HandoutParser
from ._version import __version__ as version


class Rstslide:

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

        argparser.add_argument("-t", "--theme", type=str, help="Set rstslide theme (overrides theme set in input file)")

        mode = argparser.add_mutually_exclusive_group(required=False)
        mode.add_argument("-S", "--slide", action='store_true', help="Normal slide mode (default).")
        mode.add_argument("-P", "--pdf", action='store_true', help="Pdf rendering mode (run and follow instructions).")
        mode.add_argument("-N", "--pdf-with-notes", action='store_true', help="Pdf rendering mode with notes (run and follow instructions).")
        mode.add_argument("-H", "--handout", action='store_true', help="Handout rendering mode.")
        mode.add_argument("-X", "--handout-alt", action='store_true', help="An alternative handout rendering mode that uses the default html5 docutils converter.")

        argparser.add_argument("-s", "--serve", action='store_true', help="Start webserver that serves the slides.")
        argparser.add_argument('-v', '--version', action='version', version='rstslide ' + version)
        argparser.add_argument('-d', '--debug', action='store_true', help="Write debug output on stdout")

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

        mode = 'slide'
        notes = False
        if args.pdf or args.pdf_with_notes:
            mode = 'print'
            notes = True
        elif args.handout_alt:
            mode = 'handout-alt'
        elif args.handout:
            mode = 'handout'

        if (args.pdf or args.serve) and args.resources is None:
            args.resources = 'local'

        if (args.pdf or args.serve) and args.resources == 'central':
            print("Pdf printing or serving does not work with resource option 'central', exiting.")
            exit(1)

        # Create the RST parser and create the slides
        if mode != 'handout-alt':
            parser = SlidesParser(input_file=filename, output_file=output_file, theme=args.theme, resources=args.resources, mode=mode, notes=notes, debug=args.debug)
            parser.create_slides()
        else:
            parser = HandoutParser(input_file=filename, output_file=output_file, theme=args.theme, resources=args.resources, mode=mode, notes=notes, debug=args.debug)
            parser.create_handout()

        if args.pdf or args.serve:
            port = 8000
            handler = httpserver.SimpleHTTPRequestHandler
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer(("", port), handler)
            if args.serve:
                print("The slides are served here:")
                print("  http://127.0.0.1:8000/"+output_file+"?print-pdf")
                print("To end serving the slides, end the program with Ctrl+C")
            else:
                print("Follow the following steps to export the slides as pdf:")
                print("1. Open the following URL in your web browser:")
                print("  http://127.0.0.1:8000/"+output_file+"?print-pdf")
                print("2. Wait for everything to load and then print to pdf")
                print("  (this is known to work in Google Chrome and similar browsers.)")
                print("3. End this program with Ctrl+C")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                print("Closing server")
                # Clean-up server (close socket, etc.)
                httpd.server_close()
