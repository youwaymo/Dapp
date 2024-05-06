from jinja2 import Environment, FileSystemLoader, select_autoescape

class template_generator():

    def template(template):
        # set the environment variable for basic configuration
        # autoescape : This configures autoescaping for the templates. 
        # Autoescaping helps prevent XSS (cross-site scripting) attacks by automatically escaping potentially dangerous characters in the rendered output.
        env = Environment(loader=FileSystemLoader(template), autoescape=select_autoescape())

        # get the template from the env variable
        return env.get_template('index.html')
