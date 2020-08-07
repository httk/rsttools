""" Two-columns directive.

Usage:

.. column:: left

    * item
    
    * item
    
.. column:: right

    * item
    
    * item 

Also available: column:: main and column:: side
"""

# Define the nodes.
from docutils import nodes
from .RevealTranslator import RSTTranslator


class LeftColumnNode(nodes.Part, nodes.Element):
    pass


class RightColumnNode(nodes.Part, nodes.Element):
    pass


class MainColumnNode(nodes.Part, nodes.Element):
    pass


class SideColumnNode(nodes.Part, nodes.Element):
    pass 


def visit_left_column(self, node):
    self.body.append(' '*12 + '<div class="columns"><div class="left">\n')


def depart_left_column(self, node):
    self.body.append(' '*12 + '</div>\n')


def visit_right_column(self, node):
    self.body.append(' '*12 + '<div class="right">\n')


def depart_right_column(self, node):
    self.body.append(' '*12 + '</div></div>\n')


def visit_main_column(self, node):
    self.body.append(' '*12 + '<div class="columns"><div class="main">\n')


def depart_main_column(self, node):
    self.body.append(' '*12 + '</div>\n')


def visit_side_column(self, node):
    self.body.append(' '*12 + '<div class="side">\n')


def depart_side_column(self, node):
    self.body.append(' '*12 + '</div></div>\n')


def add_node(node, **kwds):
    nodes._add_node_class_names([node.__name__])
    for key, val in kwds.items():
        try:
            visit, depart = val
        except ValueError:
            raise ExtensionError('Value for key %r must be a '
                                 '(visit, depart) function tuple' % key)

        assert key == 'html', 'accept html only'

        setattr(RSTTranslator, 'visit_'+node.__name__, visit)
        setattr(RSTTranslator, 'depart_'+node.__name__, depart)


add_node(LeftColumnNode, html=(visit_left_column, depart_left_column))
add_node(RightColumnNode, html=(visit_right_column, depart_right_column))
add_node(MainColumnNode, html=(visit_main_column, depart_main_column))
add_node(SideColumnNode, html=(visit_side_column, depart_side_column))

# Define the Directive
from docutils.parsers.rst import Directive


class Column(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = True

    node_class = None

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)
        # Left or right column?
        if self.arguments[0] in ['left', 'Left']:
            self.node_class = LeftColumnNode
        if self.arguments[0] in ['right', 'Right']:
            self.node_class = RightColumnNode
        if self.arguments[0] in ['main', 'Main']:
            self.node_class = MainColumnNode
        if self.arguments[0] in ['side', 'Side']:
            self.node_class = SideColumnNode            
        # Create the admonition node, to be populated by `nested_parse`.
        column_node = self.node_class(rawsource=text)
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset,
                                column_node)
        return [column_node]    


from docutils.parsers.rst import directives
directives.register_directive('column', Column)         

