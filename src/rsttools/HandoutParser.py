try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except BaseException:
    pass

import os, sys, codecs, shutil, subprocess, pprint

import docutils, docutils.core

# Pyhton2 compatibility
try:
    from html import unescape
except ImportError:
    from cgi import unescape


from .RevealTranslator import RevealTranslator, HTMLWriter
from .DocutilsHelper import DocutilsHelper

# Import custom directives
from .TwoColumnsDirective import *
from .PygmentsDirective import *
from .VideoDirective import *
from .PlotDirective import *
from .SmallRole import *
from .VspaceRole import *
from .ClassDirective import *
from .ClearDirective import *
from .TemplateDirective import *


class HandoutParser:
    """Class converting a stand-alone reST file into a class handout."""

    def __init__(self, input_file, output_file='', theme=None, resources=None, mode=None, notes=None, debug=None):
        """ Constructor of the Parser class.

        ``create_slides()`` must then be called to actually produce the presentation.

        Arguments:

            * input_file : name of the reST file to be processed (obligatory).

            * output_file: name of the HTML file to be generated (default: same as input_file, but with a .html extension).

            * theme: set rstslide theme (overrides theme set in input file)

            * resources: 'central', 'local', or 'inline': how external resources should be handled:

              - central (default): "Use centralized resources from where rstslide is installed
              - local: Copy needed resources to a directory <outfile>-resources
              - inline: Embedd all resources into a single file HTML document
              - online: Use links to online resources when possible (internet needed to show presentation)

            * mode: 'slide' (default) or 'print'

            * notes: True/False whether speaker notes should be rendered onto slides or not

            * debug: set to true to produce debug output on stdout

        The input rst file allows the following settings in the first field list:

            * theme: the name of the theme to be used ({**default**, beige, night}).

            * transition: the transition between slides ({**default**, cube, page, concave, zoom, linear, fade, none}).

            * stylesheet: a custom CSS file which extends or replaces the used theme.

            * pygments_style: the style to be used for syntax color-highlighting using Pygments. The list depends on your Pygments version, type::

                from pygments.styles import STYLE_MAP
                print STYLE_MAP.keys()

            * vertical_center: boolean stating if the slide content should be vertically centered (default: False).

            * horizontal_center: boolean stating if the slide content should be horizontally centered (default: False).

            * title_center: boolean stating if the title of each slide should be horizontally centered (default: False).

            * footer: boolean stating if the footer line should be displayed (default: False).

            * page_number: boolean stating if the slide number should be displayed (default: False).

            * controls: boolean stating if the control arrows should be displayed (default: False).

            * firstslide_template: template string defining how the first slide will be rendered in HTML.

            * footer_template: template string defining how the footer will be rendered in HTML.

        The ``firstslide_template`` and ``footer_template`` can use the following substitution variables:

            * %(title)s : will be replaced by the title of the presentation.

            * %(subtitle)s : subtitle of the presentation (either a level-2 header or the :subtitle: field, if any).

            * %(author)s : :author: field (if any).

            * %(institution)s : :institution: field (if any).

            * %(email)s : :email: field (if any).

            * %(date)s : :date: field (if any).

            * %(is_author)s : the '.' character if the :author: field is defined, '' otherwise.

            * %(is_subtitle)s : the '-' character if the subtitle is defined, '' otherwise.

            * %(is_institution)s : the '-' character if the :institution: field is defined, '' otherwise.

        You can also use your own fields in the templates.

        """

        self.input_file = input_file
        self.output_file = output_file

        self.theme = theme

        self.curr_dir = os.path.dirname(os.path.realpath(self.output_file))
        self.output_name = os.path.splitext(os.path.basename(output_file))[0]
        self.resource_dir_abspath = None
        self.resource_dir_relpath = None

        if resources:
            self.resources = resources
        else:
            self.resources = 'central'
        self.global_to_local_map = {}

        self.notes = notes

        if mode:
            self.mode = mode
        else:
            self.mode = 'normal'

        self.debug = debug

        # Path to rsttools directory
        self.rsttools_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        # Path to rstslide resource directory
        self.rstslide_root = os.path.join(self.rsttools_root, 'rstslide')

        # Path to reveal
        self.reveal_root = os.path.join(self.rsttools_root, 'external', 'reveal.js', 'dist')
        self.reveal_plugins_root = os.path.join(self.rstslide_root, 'reveal-plugins')

        # Path to MathJax
        self.mathjax_root = os.path.join(self.rsttools_root, 'external', 'mathjax', 'node_modules', 'mathjax','es5')

        self.settings = {}

        # Css to embed in the document
        self.settings['css_embedd'] = []

        # Extra css files to add
        self.settings['css_files'] = []

        # Javascript code to embed in the document
        self.settings['js_embedd'] = []

        # Extra js files to add
        self.settings['js_files'] = []

        # Style
        #self.settings['reveal_theme'] = 'white'
        self.settings['transition'] = 'fade'
        self.settings['pygments_style'] = 'default'
        self.settings['stylesheet'] = ''
        self.settings['vertical_center'] = False
        self.settings['horizontal_center'] = False
        self.settings['title_center'] = False
        self.settings['write_footer'] = False
        self.settings['page_number'] = False
        self.settings['controls'] = False

        # Template for the first slide
        self.settings['firstslide_template'] = ''

        # Template for the footer
        self.settings['footer_template'] = ''

        # Initalization html for reveal.js
        self.settings['init_html'] = ''

    def create_handout(self):
        """Creates the HTML5 presentation based on the arguments given to the constructor."""

        with codecs.open(self.input_file, 'r', 'utf8') as infile:
            source = infile.read()

        doctree = docutils.core.publish_doctree(source)
        docinfo_pos = doctree.first_child_matching_class(docutils.nodes.docinfo)
        del doctree[docinfo_pos]

        #print("DOCTREE\n",doctree)
        #print([x for x in doctree])
        #print(list(doctree.traverse('docinfo')))
        #doctree.remove('docinfo')
        #help(doctree)
        #docdom = doctree.asdom()
        #elem = docdom.getElementsByTagName('docinfo')[0]
        #elem.unlink()
        #doctree = docdom.toxml()

        self.parts = DocutilsHelper.publish_parts_from_doctree(doctree,
            writer_name="html5")

        document_content = self.parts['whole']

        with codecs.open(self.output_file, 'w', 'utf8') as wfile:
            wfile.write(document_content)

