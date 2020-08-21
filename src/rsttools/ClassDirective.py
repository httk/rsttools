from docutils.parsers.rst import Directive
from docutils.transforms import misc
from docutils.parsers.rst import directives
from docutils.transforms import Transform
from docutils import nodes

import ast


class ClassAttribute2(Transform):

    """
    Move the "class" attribute specified in the "pending" node into the
    immediately following non-comment element.
    """

    default_priority = 210

    def apply(self):
        pending = self.startnode
        parent = pending.parent
        child = pending
        while parent:
            # Check for appropriate following siblings:
            for index in range(parent.index(child) + 1, len(parent)):
                element = parent[index]
                if (isinstance(element, nodes.Invisible) or
                        isinstance(element, nodes.system_message)):
                    continue
                if 'class' in pending.details and pending.details['class'] is not None:
                    element['classes'] += pending.details['class']
                if 'attributes' in pending.details and pending.details['attributes'] is not None:
                    if 'attributes' in element.attributes:
                        element.attributes['attributes'].update(pending.details['attributes'])
                    else:
                        element.attributes['attributes'] = pending.details['attributes']

                pending.parent.remove(pending)
                return
            else:
                # At end of section or container; apply to sibling
                child = parent
                parent = parent.parent
        error = self.document.reporter.error(
            'No suitable element following "%s" directive'
            % pending.details['directive'],
            nodes.literal_block(pending.rawsource, pending.rawsource),
            line=pending.line)
        pending.replace_self(error)


class Class(Directive):

    """
    Set a "class" attribute on the directive content or the next element.
    When applied to the next element, a "pending" element is inserted, and a
    transform does the work later.
    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True

    option_spec = {'attributes': directives.unchanged}

    def run(self):

        if len(self.arguments) > 0:
            try:
                class_value = directives.class_option(self.arguments[0])
            except ValueError:
                raise self.error(
                    'Invalid class attribute value for "%s" directive: "%s".'
                    % (self.name, self.arguments[0]))
        else:
            class_value = None

        if 'attributes' in self.options and self.options['attributes'] is not None:
            try:
                attributes = []
                for attribute in self.options['attributes'].split("\n"):

                    left, sep, right = attribute.partition('=')
                    if sep == '':
                        a_rest_and_key = left
                        a_val = None
                    else:
                        a_rest_and_key = left
                        a_val = right

                    a_list = a_rest_and_key.split(' ')
                    if len(a_list) == 2:
                        a_restriction = a_list[0]
                        a_key = a_list[1]
                    elif len(a_list) == 1:
                        a_restriction = None
                        a_key = a_list[0]
                    else:
                        raise ValueError("wrong format: "+attribute)

                    if a_key in ['data-background-image', 'data-background-video', 'data-src']:
                        a_val = 'RSTTOOLS_DEPLOY(' + a_val + ')RSTTOOLS_DEPLOY'

                    attributes += [{'key':a_key, 'val':a_val, 'restriction':a_restriction}]

            except ValueError as e:
                raise self.error(
                    'Could not parse attribute string: "%s" (%s)'
                    % (self.options['attributes'], str(e)))
                attributes = None
        else:
            attributes = None

        node_list = []
        if self.content:
            container = nodes.Element()
            self.state.nested_parse(self.content, self.content_offset,
                                    container)
            for node in container:
                if class_value is not None:
                    node['classes'].extend(class_value)

                if attributes is not None:
                    if 'attributes' in node:
                        node['attributes'].update(attributes)
                    else:
                        node['attributes'] = attributes

            node_list.extend(container.children)
        else:
            pending = nodes.pending(
                ClassAttribute2,
                {'class': class_value, 'directive': self.name, 'attributes': attributes},
                self.block_text)
            self.state_machine.document.note_pending(pending)
            node_list.append(pending)
        return node_list


directives.register_directive('class', Class)
