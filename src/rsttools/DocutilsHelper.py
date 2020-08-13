import codecs, base64

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import docutils, docutils.core
from docutils.writers.null import Writer as NullWriter

class DocutilsHelper:

    @staticmethod
    def parse_docinfo(doctree, d=None):

        #print("\n########doctree\n\n",doctree)

        def getText(nodelist):
            # Iterate all Nodes aggregate TEXT_NODE
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
                else:
                    # Recursive
                    rc.append(getText(node.childNodes))
            result = (' '.join(rc)).replace("\0 ",'').replace("\0",'')
            #for repl in template:
            #    result = result.replace('|'+repl+'|',template[repl])
            return result

        if d is None:
            d = {}

        docdom = doctree.asdom()

        # Get all field lists in the document.
        docinfos = docdom.getElementsByTagName('docinfo')

        for docinfo in docinfos:
            for field in docinfo.childNodes:
                tag = field.tagName
                if tag == "authors":
                    authors = field.getElementsByTagName('author')
                    d["authors"] = [x.firstChild.nodeValue for x in authors]
                elif tag == "field":
                    field_name = field.getElementsByTagName('field_name')[0]
                    field_name_str = field_name.firstChild.nodeValue.lower()
                    field_body = field.getElementsByTagName('field_body')[0]
                    if field_name_str.endswith("-list"):
                        field_name = field_name_str[:-len("-list")]
                        if field_body.firstChild.tagName == 'bullet_list':
                            d[field_name] = [getText(x.childNodes) for x in field_body.childNodes] #[x.firstChild.firstChild.nodeValue % template for c in field_body.childNodes for x in c.childNodes]
                        else:
                            d[field_name] = [getText(field_body.childNodes)] #[getText(c.firstChild) % template for c in field_body.childNodes]
                    elif field_name_str.endswith("-list-add"):
                        field_name = field_name_str[:-len("-list-add")]
                        if not field_name in d:
                            d[field_name] = []
                        if field_body.firstChild.tagName == 'bullet_list':
                            d[field_name] += [getText(c.childNodes) for x in c.childNodes] #[x.firstChild.firstChild.nodeValue % template for c in field_body.childNodes for x in c.childNodes]
                        else:
                            d[field_name] += [getText(field_body.childNodes)] #[getText(c.firstChild) % template for c in field_body.childNodes]
                    else:
                        d[field_name_str] = getText(field_body.childNodes)#" ".join(getText(c.firstChild) for c in field_body.childNodes) % template

                else:
                    d[tag] = getText(field.childNodes) # % template

        topics = docdom.getElementsByTagName('topic')
        for topic in topics:
            classes = topic.getAttribute("classes").lower()
            if classes in [ 'abstract', 'dedication' ]:
                d[classes] = getText(topic.childNodes) #" ".join(getText(c.firstChild) for c in topic.childNodes)

        metas = docdom.getElementsByTagName('meta')
        for meta in metas:
            name = meta.getAttribute("name").lower()
            content = meta.getAttribute("content").strip()
            if name.endswith("-list"):
                name = name[:-len("-list")]
                d[name] = content.split(";;")
            elif name.endswith("-list-add"):
                name = name[:-len("-list-add")]
                if name in d:
                    d[name] += content.split(";;")
                else:
                    d[name] = content.split(";;")
            else:
                d[name] = content

        #import pprint
        #pprint.pprint(d)

        return d

    @staticmethod
    def dict_to_rst_replacements(d):
        text = ''
        for key in d:
            try:
                out = ""+d[key]
            except TypeError:
                try:
                    out = "".join(d[key])
                except TypeError:
                    out = ""

            if out != '':
                out = out.replace('\n','\n  ').replace('*','\*')
                text += '.. |'+key+'| replace:: '+out+'\n\n'
            else:
                text += '.. |'+key+'| replace:: \ \ \n\n'
        return text

    @staticmethod
    def publish_parts_from_doctree(document, destination_path=None,
                                   writer=None, writer_name='pseudoxml',
                                   settings=None, settings_spec=None,
                                   settings_overrides=None, config_section=None,
                                   enable_exit_status=False):
        reader = docutils.readers.doctree.Reader(parser_name='null')
        pub = docutils.core.Publisher(reader, None, writer,
                        source=docutils.io.DocTreeInput(document),
                        destination_class=docutils.io.StringOutput, settings=settings)
        if not writer and writer_name:
            pub.set_writer(writer_name)
        pub.process_programmatic_settings(
            settings_spec, settings_overrides, config_section)
        pub.set_destination(None, destination_path)
        pub.publish(enable_exit_status=enable_exit_status)
        return pub.writer.parts

    def publish_doctree(source, source_path=None,
                        source_class=docutils.io.StringInput,
                        reader=None, reader_name='standalone',
                        parser=None, parser_name='restructuredtext',
                        settings=None, settings_spec=None,
                        settings_overrides=None, config_section=None,
                        enable_exit_status=False):
        """
        Set up & run a `Publisher` for programmatic use with string I/O.
        Return the document tree.

        For encoded string input, be sure to set the 'input_encoding' setting to
        the desired encoding.  Set it to 'unicode' for unencoded Unicode string
        input.  Here's one way::

            publish_doctree(..., settings_overrides={'input_encoding': 'unicode'})

        Parameters: see `publish_programmatically`.
        """
        pub = docutils.core.Publisher(reader=reader, parser=parser, writer=RstslideDoctreeWriter(),
                        settings=settings,
                        source_class=source_class,
                        destination_class=docutils.io.NullOutput)
        pub.set_components(reader_name, parser_name, 'null')
        pub.process_programmatic_settings(
            settings_spec, settings_overrides, config_section)
        pub.set_source(source, source_path)
        pub.set_destination(None, None)
        output = pub.publish(enable_exit_status=enable_exit_status)
        return pub.document

    @staticmethod
    def encode_uri(uri):
        if uri.startswith('https://') or uri.startswith('http://'):
            with urlopen(uri) as f:
                imgdata = f.read()
                mimetype = f.headers['Content-Type']
        else:
            mimetype = mimetypes.guess_type(uri)
            with open(os.path.join(self.settings['theme_path'], theme_filename), 'rb') as f:
                    imgdata = f.read()
        encoded = codecs.decode(base64.b64encode(imgdata),'utf-8')
        imgdata = "data:"+mimetype+";base64," + encoded
        return imgdata



class RstslideDoctreeWriter(NullWriter):

    supported = ('rstslide')


