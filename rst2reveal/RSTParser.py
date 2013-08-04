try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

import os, sys
import docutils.core
from docutils.parsers.rst import Directive, directives

from RevealTranslator import RevealTranslator, RevealWriter

class RSTParser:
    """Class converting a stand-alone reST file into a Reveal.js-powered HTML5 file, using the provided options."""
    
    def __init__(self, input_file, output_file='', theme='default', transition = 'default', stylesheet='', 
                 mathjax_path='', pygments_style='', vertical_center=False, 
                 horizontal_center=False, title_center=False, footer=True, page_number=True, 
                 controls=False, firstslide_template='', footer_template=''):
        """ Constructor.
        
        Arguments:
        
            * input_file : name of the reST file to be processed (obligatory).
            
            * output_file: name of the HTML file to be generated (default: same as input_file, but with a .html extension).
            
            * theme: the name of the theme to be used (default: 'default'). 
        """
    
        # Input/Output files
        self.input_file = input_file
        self.output_file = output_file
        
        # Style
        self.theme = theme 
        self.stylesheet = stylesheet
        self.transition = transition 
        self.vertical_center=vertical_center
        self.horizontal_center = horizontal_center
        self.title_center = title_center
        self.write_footer=footer
        self.page_number=page_number
        self.controls=controls
        
        # MathJax
        if mathjax_path =='':
            self.mathjax_path = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js'
        else:
            self.mathjax_path = mathjax_path
            
        # Pygments
        self.pygments_style = pygments_style
        
        # Template for the first slide
        self.firstslide_template = firstslide_template
        
        # Temnplate for the footer
        self.footer_template = footer_template
        

    def create_slides(self):
    
        # Copy the reveal library in the current directory
        self.copy_reveal()
        
        # Create the writer and retrieve the parts
        self.html_writer = RevealWriter()
        self.html_writer.translator_class = RevealTranslator
        with open(self.input_file, 'r') as infile:
            self.parts = docutils.core.publish_parts(source=infile.read(), writer=self.html_writer)

        # Produce the html file
        self.produce_output()
        
    def copy_reveal(self):
        curr_dir = os.path.dirname(os.path.realpath(self.output_file))
        cwd = os.getcwd()
        # Copy the reveal subfolder
        if not os.path.isdir(curr_dir+'/reveal'):
            sources_dir = os.path.abspath(os.path.dirname(__file__)+'/reveal')
            import shutil
            shutil.copytree(sources_dir, curr_dir+'/reveal')
        # Generate the Pygments CSS file
        self.is_pygments = False
        if not self.pygments_style == '':
            # Check if Pygments is installed
            try:
                import pygments
                self.is_pygments = True
            except:
                print 'Warning: Pygments is not installed, the code will not be highlighted.'
                print 'You should install it with `pip install pygments`'
                return
            os.chdir(curr_dir) 
            import subprocess, shutil
            os.system("pygmentize -S "+self.pygments_style+" -f html -O bg=light > reveal/css/pygments.css")      
            # Fix the bug where the literal color goes to math blocks...
            with open('reveal/css/pygments.css', 'r') as infile:
                with open('reveal/css/pygments.css.tmp', 'w') as outfile:
                    for aline in infile:
                        outfile.write('.highlight '+aline)
            shutil.move('reveal/css/pygments.css.tmp', 'reveal/css/pygments.css')
            os.chdir(cwd)        
            
    def produce_output(self):
    
        self.title =  self.parts['title']
        self.analyse_metainfo()
        
        header = self.generate_header()
        body = self.generate_body()
        footer = self.generate_footer()
        
        document_content = header + body + footer
        

        with open(self.output_file, 'w') as wfile:
            wfile.write(document_content)
        
    def generate_body(self):
    
        body =  """
	        <body>
		        <div class="reveal">
			        <div class="slides">
%(titleslide)s
%(body)s
			        </div>
		        </div>
        """ % {'body': self.parts['body'],
                'titleslide' : self.titleslide}
        
        return body
        
    def analyse_metainfo(self):
        
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
            
        self.generate_titleslide()
        
    def generate_titleslide(self):
    
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
    <h1>%(title)s</h1>
    <h3>%(subtitle)s</h3>
    <br>
    <p><a href="mailto:%(email)s">%(author)s</a> %(is_institution)s %(institution)s</p>
    <p><small>%(email)s</small></p>
    <p>%(date)s</p>
""" 
         
        self.titleslide="""
<section class="titleslide">""" + self.firstslide_template % self.meta_info + """
</section>
"""
        if self.footer_template=="":
            self.footer_template = """<b>%(title)s %(is_subtitle)s %(subtitle)s.</b> %(author)s%(is_institution)s %(institution)s. %(date)s"""
        
        if self.write_footer:
            self.footer_html = """<footer id=\"footer\">""" + self.footer_template % self.meta_info +  """<b id=\"slide_number\" style=\"padding: 1em;\"></b></footer>"""
        elif self.page_number:
            self.footer_html =  """<footer><b id=\"slide_number\"></b></footer>"""
        else:
            self.footer_html =  ""
            
        
        
    def generate_header(self):

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
		        <link rel="stylesheet" href="reveal/css/reveal.min.css">
		        %(pygments)s
		        <link rel="stylesheet" href="reveal/css/rst2reveal.css">
		        <link rel="stylesheet" href="reveal/css/theme/default.css" id="theme">
		        <link rel="stylesheet" href="reveal/css/theme/%(theme)s.css" id="theme">
		        <link rel="stylesheet" href="reveal/css/print/pdf.css" type="text/css" media="print"> 
		        <script type="text/javascript" src="%(mathjax_path)s?config=TeX-AMS-MML_HTMLorMML"></script>
		        <!-- Extra styles -->
                <style>
                    .reveal section {
                      text-align: %(horizontal_center)s; 
                    }
                    .reveal h2{
                      text-align: %(title_center)s; 
                    }
                </style>
                %(custom_stylesheet)s
		        <!--[if lt IE 9]>
		        <script src="reveal/lib/js/html5shiv.js"></script>
		        <![endif]-->
	        </head>
        """%{'title': self.title,
             'meta' : self.parts['meta'],
             'theme': self.theme,
             'pygments': '<link rel="stylesheet" href="reveal/css/pygments.css">' if self.is_pygments else '',
             'mathjax_path': self.mathjax_path,
             'horizontal_center': 'center' if self.horizontal_center else 'left',
             'title_center': 'center' if self.title_center else 'left',
             'custom_stylesheet' : '<link rel="stylesheet" href="%s">'%self.stylesheet if not self.stylesheet is '' else ''}
             
        return header
             
             
    def generate_footer(self):
    
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
     
        footer="""
		        <script src="reveal/lib/js/head.min.js"></script>
		        <script src="reveal/js/reveal.min.js"></script>
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
				        mouseWheel: true,
				        fragments: true,
				        rollingLinks: false,
				        transition: '%(transition)s'
			        });
		        </script>
            %(script_page_number)s
		    
	        %(footer)s
	        </body>
        </html>""" % {'transition' : self.transition,
                        'footer' : self.footer_html,
                        'script_page_number' : script_page_number,
                        'vertical_center' : 'true' if self.vertical_center else 'false',
                        'controls': 'true' if self.controls else 'false'}

        return footer
            
					        
if __name__ == '__main__':
    # Create the object
    parser = RSTParser(input_file='index.rst')
    # Create the slides
    parser.create_slides()
