"""A BESSER code generator that writes Ruby on Rails model classes."""
import os

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.structural import DomainModel
from besser.generators import GeneratorInterface
from besser.utilities import sort_by_timestamp


class RailsGenerator(GeneratorInterface):
    """Generates a models.rb file from a B-UML domain model.

    Args:
        model (DomainModel): the B-UML structural model to generate from.
        output_dir (str, optional): where to write models.rb. Defaults to
            <current directory>/output.
    """

    def __init__(self, model: DomainModel, output_dir: str = None):
        super().__init__(model, output_dir)

    def generate(self):
        file_path = self.build_generation_path(file_name="models.rb")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path),
                          trim_blocks=True, lstrip_blocks=True)
        env.globals["sort_by_timestamp"] = sort_by_timestamp
        template = env.get_template("rails_models.rb.j2")
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(template.render(model=self.model))
        print("Code generated in the location: " + file_path)
