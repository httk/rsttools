try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

import os, sys, codecs, shutil, subprocess
import docutils.core

from .RevealTranslator import RSTTranslator, HTMLWriter

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

class Parser:
    """Class converting a stand-alone reST file into a Reveal.js-powered HTML5 file, using the provided options."""
    
    def __init__(self, input_file, output_file=''):
        """ Constructor of the Parser class.
        
        ``create_slides()`` must then be called to actually produce the presentation.
        
        Arguments:
        
            * input_file : name of the reST file to be processed (obligatory).
            
            * output_file: name of the HTML file to be generated (default: same as input_file, but with a .html extension).

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
    
        # Input/Output files
        self.input_file = input_file
        self.output_file = output_file
        
        # Style
        self.reveal_theme = 'simple'
        self.transition = 'fade'
        self.pygments_style = 'default'
        self.stylesheet = ''
        self.vertical_center=False
        self.horizontal_center = False
        self.title_center = False
        self.write_footer=False
        self.page_number=False
        self.controls=False
        
        self.css_embedd = ''
        
        # Pygments
        
        # Template for the first slide
        self.firstslide_template = ''
        
        # Temnplate for the footer
        self.footer_template = ''

        # Initalization html for reveal.js
        self.init_html = ''

        # Root path to rstslide
        self.rstslide_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))

        # Root path to rstslide
        self.reveal_root = os.path.join(self.rstslide_root,'resources','reveal.js','dist')

        # MathJax
        self.mathjax_path = os.path.join(self.rstslide_root,'resources','mini-mathjax','build','MathJax.js')
        
    def create_slides(self):
        """Creates the HTML5 presentation based on the arguments given to the constructor."""
    
        self._setup()
        
        # Create the writer and retrieve the parts
        self.html_writer = HTMLWriter()
        self.html_writer.translator_class = RSTTranslator
        with codecs.open(self.input_file, 'r', 'utf8') as infile:
            self.parts = docutils.core.publish_parts(source=infile.read(), writer=self.html_writer)

        # Produce the html file
        self._produce_output()
        
    def _setup(self):
        curr_dir = os.path.dirname(os.path.realpath(self.output_file))
        cwd = os.getcwd()
        if os.path.exists(os.path.join(curr_dir,'rstslide')):
            shutil.rmtree(os.path.join(curr_dir,'rstslide'))
        os.makedirs(os.path.join(curr_dir,'rstslide'))

        #source_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','css','rstslide.css'))
        #shutil.copyfile(source_file, os.path.join(curr_dir,'rstslide.css'))
        
        # Generate the Pygments CSS file
        self.is_pygments = False
        if not self.pygments_style == '':
            # Check if Pygments is installed
            try:
                import pygments
                self.is_pygments = True
            except:
                print('Warning: Pygments is not installed, the code will not be highlighted.')
                print('You should install it with `pip install pygments`')
                return
            os.chdir(curr_dir)
            #os.system("pygmentize -S "+self.pygments_style+" -f html -O bg=light > pygments.css")
            self.css_embedd += codecs.decode(subprocess.check_output(['pygmentize', '-S', self.pygments_style, "-f","html","-O","bg=light"]),'utf-8')
            # Fix the bug where the literal color goes to math blocks...
            #with codecs.open('pygments.css', 'r', 'utf8') as infile:
            #    with codecs.open('pygments.css.tmp', 'w', 'utf8') as outfile:
            #        for aline in infile:
            #            outfile.write('.highlight '+aline)
            #shutil.move('pygments.css.tmp', os.path.join('rstslide','pygments.css'))
            os.chdir(cwd)        
            
    def _produce_output(self):
    
        self.title =  self.parts['title']
        self._analyse_metainfo()
        
        header = self._generate_header()
        body = self._generate_body()
        footer = self._generate_footer()
        
        document_content = header + body + footer
        

        with codecs.open(self.output_file, 'w', 'utf8') as wfile:
            wfile.write(document_content)
        
    def _generate_body(self):
    
        body =  """
	        <body>
                        <div class="static-content"></div>
		        <div class="reveal">
			        <div class="slides">
%(titleslide)s
%(body)s
			        </div>
		        </div>
        """ % {'body': self.parts['body'],
                'titleslide' : self.titleslide}
        
        return body
        
    def _analyse_metainfo(self):
        
        def clean(text):

            import re
            if len(re.findall(r'<paragraph>', text)) > 0:
                text = re.findall(r'<paragraph>(.+)</paragraph>', text)[0]
            if len(re.findall(r'<author>', text)) > 0:
                text = re.findall(r'<author>(.+)</author>', text)[0]
            if len(re.findall(r'<date>', text)) > 0:
                text = re.findall(r'<date>(.+)</date>', text)[0]
            if len(re.findall(r'<reference', text)) > 0:
                text = re.findall(r'<reference refuri="mailto:(.+)">', text)[0]
            return text
        
        self.meta_info ={'author': ''}

        texts=self.parts['metadata'].split('\n')
        for t in texts:
            if not t == '':
                name=t.split('=')[0]
                content=t.replace(name+'=', '')
                content=clean(content)
                self.meta_info[name]= content
            
        self._generate_titleslide()
        
    def _generate_titleslide(self):
    
        if self.parts['title'] != '': # A title has been given
            self.meta_info['title'] = self.parts['title']
        elif not 'title' in self.meta_info.keys():
            self.meta_info['title'] = '' 
        
        if self.parts['subtitle'] != '': # defined with a underlined text instead of :subtitle:
            self.meta_info['subtitle'] = self.parts['subtitle']
        elif not 'subtitle' in self.meta_info.keys():
            self.meta_info['subtitle'] = ''    
        
        if not 'email' in self.meta_info.keys():
            self.meta_info['email'] = ''
            
        if not 'institution' in self.meta_info.keys():
            self.meta_info['institution'] = ''
            
        if not 'date' in self.meta_info.keys():
            self.meta_info['date'] = ''  
        
        # Separators
        self.meta_info['is_institution'] = '-' if self.meta_info['institution'] != '' else ''
        self.meta_info['is_author'] = '.' if self.meta_info['author'] != '' else ''
        self.meta_info['is_subtitle'] = '.' if self.meta_info['subtitle'] != '' else ''
            
            
        if self.firstslide_template == "":
             self.firstslide_template = """
    <section class="titleslide">
    <h1>%(title)s</h1>
    <h3>%(subtitle)s</h3>
    <br>
    <p><a href="mailto:%(email)s">%(author)s</a> %(is_institution)s %(institution)s</p>
    <p><small>%(email)s</small></p>
    <p>%(date)s</p>
    </section>
""" 

        self.titleslide=self.firstslide_template % self.meta_info
        if self.footer_template=="":
            self.footer_template = """<b>%(title)s %(is_subtitle)s %(subtitle)s.</b> %(author)s%(is_institution)s %(institution)s. %(date)s"""
        
        if self.write_footer:
            self.footer_html = """<footer id=\"footer\">""" + self.footer_template % self.meta_info +  """<b id=\"slide_number\" style=\"padding: 1em;\"></b></footer>"""
        elif self.page_number:
            self.footer_html =  """<footer><b id=\"slide_number\"></b></footer>"""
        else:
            self.footer_html =  ""
            
        
        
    def _generate_header(self):

        header="""<!doctype html>
        <html lang="en">
	        <head>
		        <meta charset="utf-8">
		        <title>%(title)s</title>
		        <meta name="description" content="%(title)s">
		        %(meta)s
		        <meta name="apple-mobile-web-app-capable" content="yes" />
		        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
		        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=no">
		        <link rel="stylesheet" href="%(reveal_root)s/reveal.css">
		        %(pygments)s
		        <link rel="stylesheet" href="%(rstslide_root)s/css/rstslide.css">
		        <link rel="stylesheet" href="%(reveal_root)s/theme/%(reveal_theme)s.css" id="theme">
                        <script type="text/x-mathjax-config">
                          MathJax.Hub.Config({
                            jax: ["input/TeX","output/SVG"],
                            extensions: ["tex2jax.js"],
                            TeX: {
                              extensions: ["AMSmath.js","AMSsymbols.js","noErrors.js","noUndefined.js"]
                            },
                            SVG: {
                               font: "Gyre-Pagella"
                            }
                          });
                        </script>
		        <script type="text/javascript" src="%(mathjax_path)s"></script>
		        <!-- Extra styles -->
                <style>
                    %(css_embedd)s

                    .reveal section {
                      text-align: %(horizontal_center)s; 
                    }

                    .reveal h2{
                      text-align: %(title_center)s; 
                    }
                </style>
                %(custom_stylesheet)s
		        <!--[if lt IE 9]>
		        <script src="%(reveal_root)s/lib/js/html5shiv.js"></script>
		        <![endif]-->
	        </head>
        """%{'title': self.title,
             'meta' : self.parts['meta'],
             'reveal_theme': self.reveal_theme,
             'reveal_root' : self.reveal_root,
             'rstslide_root' : self.rstslide_root,
             'pygments': '<link rel="stylesheet" href="pygments.css">' if self.is_pygments else '',
             'mathjax_path': self.mathjax_path,
             'horizontal_center': 'center' if self.horizontal_center else 'left',
             'title_center': 'center' if self.title_center else 'left',
             'css_embedd': self.css_embedd,
             'custom_stylesheet' : '<link rel="stylesheet" href="%s">'%self.stylesheet if self.stylesheet != '' else ''}
             
        return header
             
             
    def _generate_footer(self):
    
        if self.page_number:
            script_page_number = """
		            <script>                 
                        // Fires each time a new slide is activated
                        Reveal.addEventListener( 'slidechanged', function( event ) {
                            if(event.indexh > 0) {
                                if(event.indexv > 0) {
                                    val = event.indexh + ' - ' + event.indexv
                                    document.getElementById('slide_number').innerHTML = val;
                                }
                                else{
                                    document.getElementById('slide_number').innerHTML = event.indexh;
                                }
                            }
                            else {
                                document.getElementById('slide_number').innerHTML = '';
                            }  
                        } );
                    </script>"""
        else:
            script_page_number = ""

        if self.init_html:
            footer = self.init_html
        else:
            footer="""
		        <script src="%(reveal_root)s/reveal.js"></script>
		        <script>
			        // Full list of configuration options available here:
			        // https://github.com/hakimel/reveal.js#configuration
			        Reveal.initialize({
				        controls: %(controls)s,
				        progress: false,
				        history: true,
				        overview: true,
				        keyboard: true,
				        loop: false,
				        touch: true,
				        rtl: false,
				        center: %(vertical_center)s,
				        mouseWheel: false,
				        fragments: true,
				        rollingLinks: false,
				        transition: '%(transition)s',
                                        transitionSpeed: 'fast',
                                        slideNumber: '',
                                        menu : {
                                          side: 'right',
                                          width: 'normal',
                                          numbers: false,
                                          titleSelector: 'h1, h2, h3, h4, h5, h6',
                                          useTextContentForMissingTitles: false,
                                          hideMissingTitles: false,
                                          markers: true,
                                          custom: false,
                                          themes: false,
                                          themesPath: 'css/theme/',
                                          transitions: false,
                                          openButton: true,
                                          openSlideNumber: false,
                                          keyboard: true,
                                          sticky: false,
                                          autoOpen: true,
                                          delayInit: false,
                                          openOnInit: false,
                                          loadIcons: true,
                                        },
      	keyboard: {
        37: 'prev', // go to the next slide when the ENTER key is pressed
      	39: 'next', // go to the next slide when the ENTER key is pressed
      	33: 'prev', // go to the next slide when the ENTER key is pressed
      	34: 'next', // go to the next slide when the ENTER key is pressed
	190: 'right', // go to the next slide when the ENTER key is pressed
      	188: 'left', // go to the next slide when the ENTER key is pressed
      	},
        dependencies: [
          { src: '%(rstslide_root)s/resources/reveal-plugins/reveal.js-menu/menu.js', async: true },  
          { src: '%(rstslide_root)s/resources/reveal-plugins/toc-progress/toc-progress.js',
                async: true,
                callback: function()
                {
                    toc_progress.initialize(null,null,'{ background-color: white; color: var(--liublue0);}');
                    toc_progress.create();
                }
          }
          ]
        });
        
		        </script>"""

        footer+="""            
            %(script_page_number)s
		    
	        %(footer)s
	        </body>
        </html>"""

        footer = footer % {'transition' : self.transition,
                           'footer' : self.footer_html,
                           'mathjax_path': self.mathjax_path,
                           'reveal_root' : self.reveal_root,
                           'rstslide_root' : self.rstslide_root,
                           'script_page_number' : script_page_number,
                           'vertical_center' : 'true' if self.vertical_center else 'false',
                           'controls': 'true' if self.controls else 'false'}

        return footer
            
					        
if __name__ == '__main__':
    # Create the object
    parser = Parser(input_file='index.rst')
    # Create the slides
    parser.create_slides()
