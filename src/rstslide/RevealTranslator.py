__docformat__ = 'reStructuredText'

import os
import re

import docutils
from docutils import nodes
from docutils.writers.html4css1 import HTMLTranslator, Writer



class RSTWriter(Writer):
    """ Writer to be used with the RevealTranslator class."""

    visitor_attributes = (
        'head_prefix', 'head', 'stylesheet', 'body_prefix',
        'body_pre_docinfo', 'docinfo', 'body', 'body_suffix',
        'title', 'subtitle', 'header', 'footer', 'meta', 'fragment',
        'html_prolog', 'html_head', 'html_title', 'html_subtitle',
        'html_body', 'metadata')

                    
class RSTTranslator(HTMLTranslator):
    """ Translator converting the reST items into HTML5 code usable by Reveal.js.
    
    Derived from docutils.writers.html4css1.HTMLTranslator.
    """ 

    def __init__(self, document):
        HTMLTranslator.__init__(self, document) 
        self.math_output = 'mathjax' 
        self.metadata = []
        self.subsection_previous =False
        self.inline_lists = False
        self.slide_tile_level = 0 
        self.in_slide_title = False
        self.hide_next_title = True
        self.delayed_header_attributes = {}
        
    def visit_header(self, node):
        self.context.append(len(self.body))

    def depart_header(self, node):
        start = self.context.pop()
        header = [self.starttag(node, 'section')]
        header.extend(self.body[start:])
        header.append('\n</section>\n')
        self.body_prefix.extend(header)
        self.header.extend(header)
        del self.body[start:]
        
    def visit_title(self, node):
        """Only 6 section levels are supported by HTML."""
        check_id = 0  # TODO: is this a bool (False) or a counter?
        close_tag = ' '*12 + '</p>\n'
        if isinstance(node.parent, nodes.topic):
            self.body.append(' '*12 + 
                  self.starttag(node, 'p', '', CLASS='topic-title first'))
        elif isinstance(node.parent, nodes.sidebar):
            self.body.append(' '*12 + 
                  self.starttag(node, 'p', '', CLASS='sidebar-title'))
        elif isinstance(node.parent, nodes.Admonition):
            self.body.append(' '*12 + 
                  self.starttag(node, 'p', '', CLASS='admonition-title'))
        elif isinstance(node.parent, nodes.table):
            self.body.append(' '*12 + 
                  self.starttag(node, 'caption', ''))
            close_tag = ' '*12 + '</caption>\n'
        elif isinstance(node.parent, nodes.document):
            self.body.append(' '*8 + self.starttag(node, 'h2'))
            close_tag = '</h2>\n'
            self.in_document_title = len(self.body)
        else:
            self.slide_tile_level += 1
            self.in_slide_title = True
            assert isinstance(node.parent, nodes.section)
            if self.hide_next_title:
                self.body.append(' '*8 + self.starttag(node, 'h2', '', style='display:none', **self.delayed_header_attributes))
            else:
                self.body.append(' '*8 + self.starttag(node, 'h2', '', **self.delayed_header_attributes))
            self.delayed_header_attributes = {}
            close_tag = '</h2>\n'
        self.context.append(close_tag)

    def depart_title(self, node):
        self.body.append(self.context.pop())
        if self.in_document_title:
            self.title = self.body[self.in_document_title:-1]
            self.in_document_title = 0
            self.body_pre_docinfo.extend(self.body)
            self.html_title.extend(self.body)
            del self.body[:]
        if self.in_slide_title:
            self.in_slide_title = False
            self.slide_title_level = 0
            
    def visit_section(self, node):
        self.section_level += 1
        if self.section_level == 2:
            if not self.hide_next_title:
                self.body.append('    </section>\n')
            self.delayed_header_attributes = node.get('attributes',{})
            node.attributes['attributes']=node.get('slide-attributes',{})
            self.body.append('    ' + self.starttag(node, 'section','\n',check="me"))
            self.hide_next_title = False
        else:
            self.body.append('<section>\n')
            self.hide_next_title = True
            
    def depart_section(self, node):
        self.section_level -= 1
        if not self.section_level == 1:
            self.subsection_previous =False
            if not self.hide_next_title:
                self.body.append('    </section>\n')
        else:
            self.subsection_previous =True
        if not self.subsection_previous:
            self.hide_next_title = True
            self.body.append('</section>\n\n')
        self.inline_lists = False
        
    def visit_docinfo(self, node):
        self.context.append(len(self.body))
        self.in_docinfo = True

    def depart_docinfo(self, node):
        self.in_docinfo = False
        start = self.context.pop()
        self.docinfo = self.body[start:]
        self.body = []

    def visit_docinfo_item(self, node, name, meta=True):
        self.metadata.append(name + '=' + unicode(node)+'\n')
        self.body.append(self.starttag(node, 'tr', ''))
        if len(node):
            if isinstance(node[0], nodes.Element):
                node[0]['classes'].append('first')
            if isinstance(node[-1], nodes.Element):
                node[-1]['classes'].append('last')

    def depart_docinfo_item(self):
        pass
        
    def visit_field(self, node):
        pass

    def depart_field(self, node):
        pass

    def visit_field_body(self, node):
        field_names = re.findall(r'<field_name>(.+)</field_name>', unicode(node.parent[0]))
        field_values = re.findall(r'<field_body>(.+)</field_body>', unicode(node.parent[1]))
        if len(field_names) > 0 and len(field_values) > 0:
            name = field_names[0]
            value = field_values[0]
            self.metadata.append(name + '=' + value + '\n')
            
    def depart_field_body(self, node):
        pass
        
    def visit_block_quote(self, node):
        if not isinstance(node.parent, nodes.list_item):
            self.body.append(' '*12 + self.starttag(node, 'blockquote'))

    def depart_block_quote(self, node):
        if not isinstance(node.parent, nodes.list_item):
            self.body.append(' '*12 + '</blockquote>\n')
        

    def visit_image(self, node):
        atts = {}
        uri = node['uri']
        # place SWF images in an <object> element
        types = {'.swf': 'application/x-shockwave-flash'}
        ext = os.path.splitext(uri)[1].lower()
        if ext in ('.swf'):
            atts['data'] = uri
            atts['type'] = types[ext]
        else:
            atts['src'] = uri
            atts['alt'] = node.get('alt', uri)
        # image size
        if 'width' in node:
            atts['width'] = node['width']
        if 'height' in node:
            atts['height'] = node['height']
        if 'scale' in node:
            if (PIL and not ('width' in node and 'height' in node)
                and self.settings.file_insertion_enabled):
                imagepath = urllib.url2pathname(uri)
                try:
                    img = PIL.Image.open(
                            imagepath.encode(sys.getfilesystemencoding()))
                except (IOError, UnicodeEncodeError):
                    pass # TODO: warn?
                else:
                    self.settings.record_dependencies.add(
                        imagepath.replace('\\', '/'))
                    if 'width' not in atts:
                        atts['width'] = unicode(img.size[0])
                    if 'height' not in atts:
                        atts['height'] = unicode(img.size[1])
                    del img
            for att_name in 'width', 'height':
                if att_name in atts:
                    match = re.match(r'([0-9.]+)(\S*)$', atts[att_name])
                    assert match
                    atts[att_name] = '%s%s' % (
                        float(match.group(1)) * (float(node['scale']) / 100),
                        match.group(2))
        style = []
        for att_name in 'width', 'height':
            if att_name in atts:
                if re.match(r'^[0-9.]+$', atts[att_name]):
                    # Interpret unitless values as pixels.
                    atts[att_name] += 'px'
                style.append('%s: %s;' % (att_name, atts[att_name]))
                del atts[att_name]
        if style:
            atts['style'] = ' '.join(style)
        if (isinstance(node.parent, nodes.TextElement) or
            (isinstance(node.parent, nodes.reference) and
             not isinstance(node.parent.parent, nodes.TextElement))):
            # Inline context or surrounded by <a>...</a>.
            suffix = ''
        else:
            suffix = '\n'
        align='align-center'
        if 'align' in node:
            atts['class'] = 'align-%s' % node['align']
            align=atts['class']
            #if node['align'] in ['left', 'right']:
            #    self.inline_lists = True
        self.context.append('')
        if ext in ('.swf'): # place in an object element,
            # do NOT use an empty tag: incorrect rendering in browsers
            self.body.append(self.starttag(node, 'object', suffix, **atts) +
                             node.get('alt', uri) + '</object>' + suffix)
        else:
            self.body.append(' '*12 + '<div class=\"'+align+'\">\n')
            self.body.append(' '*12 + self.emptytag(node, 'img', suffix, **atts))
            self.body.append(' '*12 + '</div>\n')

    def depart_image(self, node):
        self.body.append(self.context.pop())

        
    def visit_bullet_list(self, node):
        atts = {}
        old_compact_simple = self.compact_simple
        self.context.append((self.compact_simple, self.compact_p))
        self.compact_p = None
        self.compact_simple = self.is_compactable(node)
        
        if 'fragment' in node['classes']:
            node['classes'].remove('fragment')
            node['classes'].append('fragmented_list')
            
        if self.compact_simple and not old_compact_simple:
            atts['class'] = 'simple'
        if self.inline_lists: # the list  should wrap an image
            self.body.append(' '*12 + '<ul style="display: inline;">')
        else:
            self.body.append(' '*12 + self.starttag(node, 'ul', **atts))

    def depart_bullet_list(self, node):
        self.compact_simple, self.compact_p = self.context.pop()
        self.body.append(' '*12 + '</ul>\n')
        
    def visit_enumerated_list(self, node):
        """
        The 'start' attribute does not conform to HTML 4.01's strict.dtd, but
        CSS1 doesn't help. CSS2 isn't widely enough supported yet to be
        usable.
        """
        atts = {}
        if 'start' in node:
            atts['start'] = node['start']
        if 'enumtype' in node:
            atts['class'] = node['enumtype']
        # @@@ To do: prefix, suffix. How? Change prefix/suffix to a
        # single "format" attribute? Use CSS2?
        old_compact_simple = self.compact_simple
        self.context.append((self.compact_simple, self.compact_p))
        self.compact_p = None
        self.compact_simple = self.is_compactable(node)
        if 'fragment' in node['classes']:
            node['classes'].remove('fragment')
            node['classes'].append('fragmented_list')
        if self.compact_simple and not old_compact_simple:
            atts['class'] = (atts.get('class', '') + ' simple').strip()
        self.body.append(' '*12 + self.starttag(node, 'ol', **atts))

    def depart_enumerated_list(self, node):
        self.compact_simple, self.compact_p = self.context.pop()
        self.body.append(' '*12 + '</ol>\n')
                
    def visit_list_item(self, node):
        if 'fragmented_list' in node.parent['classes']:
            self.body.append(' '*16 + self.starttag(node, 'li', '', CLASS='fragment'))
        else:
            self.body.append(' '*16 + self.starttag(node, 'li', ''))
        if len(node):
            node[0]['classes'].append('first')

    def depart_list_item(self, node):
        self.body.append('</li>\n')
                
                
    def visit_sidebar(self, node):
        if 'classes' in node:
            if node['classes'][0] in ['left', 'right']:
                self.inline_lists = True
        HTMLTranslator.visit_sidebar(self, node)

    def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
        """
        Construct and return a start tag given a node (id & class attributes
        are extracted), tag name, and optional attributes.
        """
        tagname = tagname.lower()
        prefix = []
        atts = node.get('attributes',{})
        ids = []
        for (name, value) in attributes.items():
            atts[name.lower()] = value            
        classes = []
        languages = []
        # unify class arguments and move language specification
        for cls in node.get('classes', []) + atts.pop('class', '').split() :
            if cls.startswith('language-'):
                languages.append(cls[9:])
            elif cls.strip() and cls not in classes:
                classes.append(cls)
        if languages:
            # attribute name is 'lang' in XHTML 1.0 but 'xml:lang' in 1.1
            atts[self.lang_attribute] = languages[0]
        if classes:
            atts['class'] = ' '.join(classes)
        assert 'id' not in atts
        ids.extend(node.get('ids', []))
        if 'ids' in atts:
            ids.extend(atts['ids'])
            del atts['ids']
        if ids:
            atts['id'] = ids[0]
            for id in ids[1:]:
                # Add empty "span" elements for additional IDs.  Note
                # that we cannot use empty "a" elements because there
                # may be targets inside of references, but nested "a"
                # elements aren't allowed in XHTML (even if they do
                # not all have a "href" attribute).
                if empty:
                    # Empty tag.  Insert target right in front of element.
                    prefix.append('<span id="%s"></span>' % id)
                else:
                    # Non-empty tag.  Place the auxiliary <span> tag
                    # *inside* the element, as the first child.
                    suffix += '<span id="%s"></span>' % id
        attlist = atts.items()
        attlist.sort()
        parts = [tagname]
        for name, value in attlist:
            if value is None:
                parts.append('%s' % (name.lower()))
            elif isinstance(value, list):
                values = [unicode(v) for v in value]
                parts.append('%s="%s"' % (name.lower(),
                                          self.attval(' '.join(values))))
            else:
                parts.append('%s="%s"' % (name.lower(),
                                          self.attval(unicode(value))))
        if empty:
            infix = ' /'
        else:
            infix = ''
        return ''.join(prefix) + '<%s%s>' % (' '.join(parts), infix) + suffix
