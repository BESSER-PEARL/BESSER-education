"""
This module defines the `RailsGenerator` class, which is responsible for generating Ruby on Rails code 
from a given domain model using Jinja2 templates.
"""
import os
from jinja2 import Environment, FileSystemLoader
from besser.BUML.metamodel.structural import DomainModel
from besser.generators import GeneratorInterface

class RailsGenerator(GeneratorInterface):
    """
    A class to generate Ruby on Rails code from a given domain model using Jinja2 templates.

    Usage:
        The `RailsGenerator` class takes a domain model and an optional output directory as input. 
        It uses Jinja2 templates to generate Ruby on Rails code and writes the output to a specified file.
        Example:
            generator = RailsGenerator(model=my_domain_model, output_dir="output/")
            generator.generate()
    Attributes:
        model (DomainModel): The domain model used for code generation.
        output_dir (str): The directory where the generated code will be saved. Defaults to None.
    Methods:
        generate(): Generates Ruby on Rails code based on the domain model and writes it to a file.
    """

    def __init__(self, model: DomainModel, output_dir: str = None):
        super().__init__(model, output_dir)

    def generate(self):
        file_path = self.build_generation_path(file_name="models.rb")
        templates_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(
            templates_path), trim_blocks=True, lstrip_blocks=True, extensions=['jinja2.ext.do'])
        template = env.get_template('rails_template.py.j2')
        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = template.render(model=self.model)
            f.write(generated_code)
            print("Code generated in the location: " + file_path)
