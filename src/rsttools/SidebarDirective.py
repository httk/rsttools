"""
Patch of SidebarDirective to allow no title (as is documented)
"""

import sys
from docutils import nodes, utils
from docutils.parsers.rst import Directive, directives

class SidebarBasePseudoSection(Directive):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged}
    has_content = True

    node_class = None
    """Node class to be used (must be set in subclasses)."""

    def run(self):
        if not (self.state_machine.match_titles
                or isinstance(self.state_machine.node, nodes.sidebar)):
            raise self.error('The "%s" directive may not be used within '
                             'topics or body elements.' % self.name)
        self.assert_has_content()
        titles = []
        messages = []
        if len(self.arguments) > 0:
            title_text = self.arguments[0]
            textnodes, messages = self.state.inline_text(title_text, self.lineno)
            titles.append(nodes.title(title_text, '', *textnodes))
        # Sidebar uses this code.
        if 'subtitle' in self.options:
            textnodes, more_messages = self.state.inline_text(
                self.options['subtitle'], self.lineno)
            titles.append(nodes.subtitle(self.options['subtitle'], '',
                                         *textnodes))
            messages.extend(more_messages)
        text = '\n'.join(self.content)
        node = self.node_class(text, *(titles + messages))
        node['classes'] += self.options.get('class', [])
        self.add_name(node)
        if text:
            self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

class Sidebar(SidebarBasePseudoSection):

    node_class = nodes.sidebar

    option_spec = SidebarBasePseudoSection.option_spec.copy()
    option_spec['subtitle'] = directives.unchanged_required

    def run(self):
        if isinstance(self.state_machine.node, nodes.sidebar):
            raise self.error('The "%s" directive may not be used within a '
                             'sidebar element.' % self.name)
        return SidebarBasePseudoSection.run(self)

directives.register_directive('sidebar', Sidebar)
