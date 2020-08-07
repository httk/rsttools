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
                if 'slide-attributes' in pending.details and pending.details['slide-attributes'] is not None:
                    if 'slide-attributes' in element.attributes:
                        element.attributes['slide-attributes'].update(pending.details['slide-attributes'])
                    else:
                        element.attributes['slide-attributes'] = pending.details['slide-attributes']
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

    option_spec = {'attributes': directives.unchanged, 'slide-attributes': directives.unchanged}

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
                attributes = ast.literal_eval(self.options['attributes'])
            except ValueError:
                raise self.error(
                    'Could not parse attribute string: "%s"'
                    % self.options['attributes'])
                attributes = None
        else:
            attributes = None

        if 'slide-attributes' in self.options and self.options['slide-attributes'] is not None:
            try:
                slide_attributes = ast.literal_eval(self.options['slide-attributes'])
            except ValueError:
                raise self.error(
                    'Could not parse slide-attribute string: "%s"'
                    % self.options['slide-attributes'])
                slide_attributes = None
        else:
            slide_attributes = None

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
                if slide_attributes is not None:
                    if 'slide-attributes' in node:
                        node['slide-attributes'].update(slide_attributes)
                    else:
                        node['slide-attributes'] = slide_attributes

            node_list.extend(container.children)
        else:
            if 'attributes' in self.options and self.options['attributes'] is not None:
                try:
                    attributes = ast.literal_eval(self.options['attributes'])
                except ValueError:
                    raise self.error(
                        'Could not parse attribute string: "%s"'
                        % self.options['attributes'])
                    attributes = None
            else:
                attributes = None
            if 'slide-attributes' in self.options and self.options['slide-attributes'] is not None:
                try:
                    slide_attributes = ast.literal_eval(self.options['slide-attributes'])
                except ValueError:
                    raise self.error(
                        'Could not parse slide-attribute string: "%s"'
                        % self.options['slide-attributes'])
                    slide_attributes = None
            else:
                slide_attributes = None
            pending = nodes.pending(
                ClassAttribute2,
                {'class': class_value, 'directive': self.name, 'attributes': attributes, 'slide-attributes': slide_attributes},
                self.block_text)
            self.state_machine.document.note_pending(pending)
            node_list.append(pending)
        return node_list


directives.register_directive('class', Class)
