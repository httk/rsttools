# $Id: html.py 8347 2019-08-26 12:12:02Z milde $
# Author: David Goodger <goodger@python.org>, modifications for rstslide by Rickard Armiento
# Copyright: This module has been placed in the public domain.

"""
Directives for typically HTML-specific constructs.
"""

__docformat__ = 'reStructuredText'

import sys
from docutils import nodes, utils
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst import states
from docutils.transforms import components

class MetaBody(states.SpecializedBody):

    class meta(nodes.Special, nodes.PreBibliographic, nodes.Element):
        """HTML-specific "meta" element."""
        pass

    def field_marker(self, match, context, next_state):
        """Meta element."""
        node, blank_finish = self.parsemeta(match, self.meta_format)
        self.parent += node
        return [], next_state, []

    def parsemeta(self, match, meta_format):
        name = self.parse_field_marker(match)
        name = utils.unescape(utils.escape2null(name))
        indented, indent, line_offset, blank_finish = \
              self.state_machine.get_first_known_indented(match.end())
        node = self.meta()
        pending = nodes.pending(components.Filter,
                                {'component': 'writer',
                                 'format': meta_format,
                                 'nodes': [node]})
        node['content'] = utils.unescape(utils.escape2null(
                                            ' '.join(indented)))
        if not indented:
            line = self.state_machine.line
            msg = self.reporter.info(
                  'No content for meta tag "%s".' % name,
                  nodes.literal_block(line, line))
            return msg, blank_finish
        tokens = name.split()
        try:
            attname, val = utils.extract_name_value(tokens[0])[0]
            node[attname.lower()] = val
        except utils.NameValueError:
            node['name'] = tokens[0]
        for token in tokens[1:]:
            try:
                attname, val = utils.extract_name_value(token)[0]
                node[attname.lower()] = val
            except utils.NameValueError as detail:
                line = self.state_machine.line
                msg = self.reporter.error(
                      'Error parsing meta tag attribute "%s": %s.'
                      % (token, detail), nodes.literal_block(line, line))
                return msg, blank_finish
        self.document.note_pending(pending)
        return pending, blank_finish


class Meta(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 1

    SMkwargs = {'state_classes': (MetaBody,)}

    def run(self):
        self.assert_has_content()

        if len(self.arguments) > 0:
            try:
                meta_format = ' '.join(self.arguments[0].lower().split())
            except ValueError:
                raise self.error(
                    'Invalid meta attribute value for "%s" directive: "%s".'
                    % (self.name, self.arguments[0]))
        else:
            meta_format = 'html'

        node = nodes.Element()
        new_line_offset, blank_finish = self.state.nested_list_parse(
            self.content, self.content_offset, node,
            initial_state='MetaBody', blank_finish=True,
            state_machine_kwargs=self.SMkwargs, extra_settings={'meta_format': meta_format})
        if (new_line_offset - self.content_offset) != len(self.content):
            # incomplete parse of block?
            error = self.state_machine.reporter.error(
                'Invalid meta directive.',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            node += error
        return node.children



directives.register_directive('meta', Meta)
