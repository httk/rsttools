from docutils.parsers.rst import Directive, directives, roles, convert_directive_function

class CustomTemplate:
    """
    Wrapper for custom templates.
    """

    def __init__(self, role_name, base_role, options={}):
        self.name = role_name
        self.base_role = base_role
        if 'prefix' in options:
            self.prefix = options['prefix']
        else:
            self.prefix = ''
        if 'suffix' in options:
            self.suffix = options['suffix']
        else:
            self.suffix = ''

    def __call__(self, role, rawtext, text, lineno, inliner,
                 options={}, content=[]):
        opts = {'format':'html'}
        opts.update(options)
        text = self.prefix + text + self.suffix
        return self.base_role(role, rawtext, text, lineno, inliner,
                              options=opts, content=content)




class Template(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False    
    has_content = False
    
    option_spec = {'prefix': directives.unchanged, 'suffix': directives.unchanged}
    
    def run(self):
        """Dynamically create and register a custom interpreted text template."""
        try:
            new_role_name = self.arguments[0]
        except ValueError:
            raise self.error(
                'Missing template name for directive: "%s".'
                % (self.name))            
        messages = []
        base_role = roles.raw_role
        converted_role = convert_directive_function(base_role)
        role = CustomTemplate(new_role_name, base_role, self.options)
        roles.register_local_role(new_role_name, role)
        return messages

directives.register_directive('template', Template)
