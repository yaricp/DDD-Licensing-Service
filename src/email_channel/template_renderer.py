from loguru import logger
from jinja2 import Environment, FileSystemLoader, select_autoescape


class TemplateRenderer:
    """Class for processing the template

    Methods
    -------
    render()
        Template processing based on passed variables
    """

    def __init__(self, template: str, template_vars: dict = {}):
        """Initialize a template obj

        Parameters
        ----------
        template : str
            Template name like a 'default.html'
        template_vars : dict
            Dictionary with names and values of variables for the passed template
        """
        self.logger = logger
        self.env = Environment(
            loader=FileSystemLoader(searchpath="/email_client/templates"),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.template = template
        self.template_vars = template_vars

    def render(self):
        """Template processing based on passed variables

        Returns
        -------
        str
            Processed template in string format
        """

        processed_template = ''
        try:
            template = self.env.get_template(self.template)
            processed_template = template.render(**self.template_vars)
            self.logger.info(f'Template {self.template} generate successful')
        except Exception:
            self.logger.exception(
                'Error while loading template', exc_info=True
            )

        return processed_template

    def __repr__(self):
        return f'<Template obj {self.template}>'
