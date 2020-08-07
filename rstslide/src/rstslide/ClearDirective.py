""" Mark a line where floats are cleared

Usage:

.. clear

.. clear:: left

.. clear:: right

"""

# Define the nodes.
from docutils import nodes
from .RevealTranslator import RevealTranslator


class ClearBothNode(nodes.Part, nodes.Element):
    pass


class ClearLeftNode(nodes.Part, nodes.Element):
    pass


class ClearRightNode(nodes.Part, nodes.Element):
    pass


def visit_clear_both(self, node):
    self.body.append(' '*12 + '<div style="clear:both"/>\n')


def depart_clear_both(self, node):
    pass


def visit_clear_left(self, node):
    self.body.append(' '*12 + '<div style="clear:left"/>\n')


def depart_clear_left(self, node):
    pass


def visit_clear_right(self, node):
    self.body.append(' '*12 + '<div style="clear:right"/>\n')


def depart_clear_right(self, node):
    pass


def add_node(node, **kwds):
    nodes._add_node_class_names([node.__name__])
    for key, val in kwds.items():
        try:
            visit, depart = val
        except ValueError:
            raise ExtensionError('Value for key %r must be a '
                                 '(visit, depart) function tuple' % key)

        assert key == 'html', 'accept html only'

        setattr(RevealTranslator, 'visit_'+node.__name__, visit)
        setattr(RevealTranslator, 'depart_'+node.__name__, depart)


add_node(ClearBothNode, html=(visit_clear_both, depart_clear_both))
add_node(ClearLeftNode, html=(visit_clear_left, depart_clear_left))
add_node(ClearRightNode, html=(visit_clear_right, depart_clear_right))

# Define the Directive
from docutils.parsers.rst import Directive


class Clear(Directive):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {}
    has_content = False

    node_class = None

    def run(self):
        if len(self.arguments) == 0:
            self.node_class = ClearBothNode
        elif self.arguments[0] in ['left', 'Left']:
            self.node_class = ClearLeftNode
        elif self.arguments[0] in ['right', 'Right']:
            self.node_class = ClearRightNode
        elif self.arguments[0] in ['both', 'Both']:
            self.node_class = ClearBothNode
        else:
            raise self.error("Uknown argument to clear directive %s" % (self.arguments[0],))
        column_node = self.node_class()
        return [column_node]


from docutils.parsers.rst import directives
directives.register_directive('clear', Clear)

