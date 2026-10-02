---
title: Write your own code generator
number: 11
track: extend
summary: A working BESSER generator that turns a B-UML class model into Ruby on Rails model classes.
duration: 60
level: Intermediate
setup: [Python]
needs:
  - Python 3.11 or 3.12
  - A terminal and a code editor
  - Basic Jinja or other template syntax helps but is not required
outcomes:
  - Implement a generator class on top of BESSER's GeneratorInterface
  - Load and render a Jinja template the way the built-in generators do
  - Traverse classes, attributes and association ends of a domain model from a template
  - Map multiplicities to Rails associations (has_many, belongs_to, has_and_belongs_to_many)
before: [buml-python]
files:
  - { label: "Generator class (rails_generator.py)", href: "/files/code-generator/rails_generator.py" }
  - { label: "Starter template (rails_models.rb.j2)", href: "/files/code-generator/rails_models.rb.j2" }
  - { label: "Library model (library_model.py)", href: "/files/code-generator/library_model.py" }
  - { label: "Run script (generate.py)", href: "/files/code-generator/generate.py" }
updated: 2026-10-02
version: "8.0"
draft: false
---

Every BESSER generator follows the same recipe: a Python class receives a B-UML model, a Jinja template walks through that model, and the rendered text is written to a file. Once you know the recipe, you can target any language or framework BESSER does not support yet.

In this lab you build a generator for Ruby on Rails. Rails follows the Model-View-Controller pattern, and you generate the Model part: one `ApplicationRecord` class per B-UML class, with its attributes and its associations. You work with the same Library, Book and Author model used in earlier labs.

You do not need Ruby or Rails installed. The generator only writes text; checking it with Ruby is optional.

## Set up the project folder

1. Create a folder for the generator and a virtual environment with BESSER in it.

   ```bash
   mkdir rails-generator
   cd rails-generator
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install besser
   ```

   ```powershell
   mkdir rails-generator
   cd rails-generator
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install besser
   ```

2. Download the four starter files from the top of this page. Put [rails_generator.py](/files/code-generator/rails_generator.py), [library_model.py](/files/code-generator/library_model.py) and [generate.py](/files/code-generator/generate.py) in `rails-generator/`. Create a `templates/` folder and put [rails_models.rb.j2](/files/code-generator/rails_models.rb.j2) in it.

   ```text
   rails-generator/
   ├── generate.py
   ├── library_model.py
   ├── rails_generator.py
   └── templates/
       └── rails_models.rb.j2
   ```

3. Check the installed version:

   ```bash
   python -c "from importlib.metadata import version; print(version('besser'))"
   ```

   ```text
   8.0.1
   ```

`library_model.py` builds this model with the B-UML Python API:

| Class | Attributes | Associations |
|---|---|---|
| Library | name: str, address: str | `locatedIn` 1 on the Library side, `has` 0..* on the Book side |
| Book | title: str, pages: int, release: datetime | `publishes` 0..* on the Book side, `writtenBy` 1..* on the Author side |
| Author | name: str, email: str | |

:::checkpoint
The four files are in place, `templates/` holds the `.j2` file, and the version command prints `8.0.1` (or a later 8.x release).
:::

## Read the generator class

Open `rails_generator.py`. Without its docstrings, this is the whole generator:

```python
import os

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.structural import DomainModel
from besser.generators import GeneratorInterface
from besser.utilities import sort_by_timestamp


class RailsGenerator(GeneratorInterface):

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
```

What each piece does:

- `GeneratorInterface` (in `besser/generators/generator_interface.py`) is an abstract base class with two abstract methods: `__init__(self, model, output_dir=None)` and `generate(self)`. Calling `super().__init__` stores the model in `self.model` and the folder in `self.output_dir`.
- `build_generation_path("models.rb")` is a helper from the interface. It creates `output_dir`, or `./output` when you passed none, and returns the full path of the file to write.
- The Jinja `Environment` loads templates from the `templates/` folder next to the generator file, so the generator works from any working directory. The built-in generators, for example `besser/generators/java_classes/java_generator.py`, use the same pattern with `trim_blocks` and `lstrip_blocks`, which stop `{% %}` lines from leaving blank lines and indentation in the output.
- `env.globals["sort_by_timestamp"]` makes a BESSER helper available inside the template. You will see why it matters in the next step.
- `template.render(model=self.model)` exposes the domain model to the template as `model`.

:::note
The BESSER documentation page on creating a generator shows `self.render_template(...)` and `self.write_file(...)`. Those methods do not exist on `GeneratorInterface` in 8.0.1. Load the template with Jinja and write the file yourself, as above.
:::

:::checkpoint
You can say which line decides the output file name (`build_generation_path`), which line picks the template (`get_template`) and which name the template uses for the model (`model`).
:::

## Write a first template that lists the classes

Open `templates/rails_models.rb.j2`:

```jinja
{% for class in sort_by_timestamp(model.get_classes()) %}
class {{ class.name }} < ApplicationRecord
end

{% endfor %}
```

`model.get_classes()` returns a Python `set`, so its order changes from run to run. On one run it came back as:

```python
>>> [c.name for c in library_model.get_classes()]
['Author', 'Book', 'Library']
```

Every B-UML element records when it was created, and `sort_by_timestamp` turns the set into a list in creation order. The built-in generators use it for the same reason: the same model always produces the same file, so diffs between two generations stay meaningful.

:::checkpoint
The template loops over the sorted classes and prints a `class ... < ApplicationRecord` / `end` pair for each one.
:::

## Run the generator on the Library model

`generate.py` imports the model and calls the generator:

```python
from library_model import library_model
from rails_generator import RailsGenerator

RailsGenerator(model=library_model).generate()
```

Run it from the `rails-generator/` folder:

```bash
python generate.py
```

```text
Code generated in the location: /path/to/rails-generator/output/models.rb
```

Open `output/models.rb`:

```ruby
class Library < ApplicationRecord
end

class Book < ApplicationRecord
end

class Author < ApplicationRecord
end
```

Pass `output_dir` to write somewhere else, for example straight into a Rails project: `RailsGenerator(model=library_model, output_dir="app/models").generate()`.

:::troubleshoot
`jinja2.exceptions.TemplateNotFound: rails_models.rb.j2` means the template is not inside a `templates/` folder next to `rails_generator.py`. Check the folder name and that the file did not get a `.txt` extension from the browser download.
:::

:::checkpoint
`output/models.rb` lists Library, Book and Author in that order, and running `python generate.py` again gives the same file.
:::

## Add attributes with a type mapping

Rails needs a type for each attribute. B-UML primitive types have short names: `StringType.name` is `str`, and the others are `int`, `float`, `bool`, `date`, `datetime` and `time`. Map them to Rails types with a dictionary at the top of the template, and loop over each class's attributes:

```jinja
{% set rails_types = {"str": "string", "int": "integer", "float": "float", "bool": "boolean",
                      "date": "date", "datetime": "datetime", "time": "time"} %}
{% for class in sort_by_timestamp(model.get_classes()) %}
class {{ class.name }} < ApplicationRecord
{% for attr in sort_by_timestamp(class.attributes) %}
  attribute :{{ attr.name }}, :{{ rails_types.get(attr.type.name, "string") }}
{% endfor %}
end

{% endfor %}
```

`class.attributes` is also a set, so it gets the same sorting. Types that are not in the dictionary, such as an enumeration, fall back to `string`.

Run `python generate.py` again:

```ruby
class Library < ApplicationRecord
  attribute :name, :string
  attribute :address, :string
end

class Book < ApplicationRecord
  attribute :title, :string
  attribute :pages, :integer
  attribute :release, :datetime
end

class Author < ApplicationRecord
  attribute :name, :string
  attribute :email, :string
end
```

:::checkpoint
Each class lists its attributes in the order they were declared in `library_model.py`, with `:integer` for `pages` and `:datetime` for `release`.
:::

## Explore how the model exposes associations

Before you generate associations, look at what the model gives you. Create `explore_associations.py` in the project folder:

```python
from besser.utilities import sort_by_timestamp
from library_model import library_model

for cls in sort_by_timestamp(library_model.get_classes()):
    print(cls.name)
    for end in sort_by_timestamp(cls.association_ends()):
        mine = end.opposite_end()
        print(f"  via {end.owner.name}: this side '{mine.name}' {mine.multiplicity.min}..{mine.multiplicity.max}, "
              f"other side '{end.name}' -> {end.type.name} {end.multiplicity.min}..{end.multiplicity.max}, "
              f"navigable={end.is_navigable}")
```

Run it with `python explore_associations.py`:

```text
Library
  via lib_book_assoc: this side 'locatedIn' 1..1, other side 'has' -> Book 0..9999, navigable=True
Book
  via lib_book_assoc: this side 'has' 0..9999, other side 'locatedIn' -> Library 1..1, navigable=True
  via book_author_assoc: this side 'publishes' 0..9999, other side 'writtenBy' -> Author 1..9999, navigable=True
Author
  via book_author_assoc: this side 'writtenBy' 1..9999, other side 'publishes' -> Book 0..9999, navigable=True
```

What this tells you about the API:

- An association end is a `Property`. Its `type` is the class at that end, and its `owner` is the `BinaryAssociation` it belongs to.
- `cls.association_ends()` returns the ends at the other side of each of the class's associations, the ones you navigate to from `cls`. For Book that is `locatedIn` (to Library) and `writtenBy` (to Author).
- `end.opposite_end()` returns the end on the class's own side of the same association.
- `end.multiplicity.min` and `end.multiplicity.max` are integers. An unbounded `"*"` is stored as `9999`, so test `max > 1` for "many", not `max == "*"`.
- `end.is_navigable` is `False` when the association cannot be traversed in that direction. Skip those ends in generated code.
- `cls.associations` returns the associations themselves, and `association.ends` returns both ends.

:::note
`cls.association_ends()` only covers associations declared on the class itself. Use `cls.all_association_ends()` when a subclass should also see the associations of its parents.
:::

:::checkpoint
The script prints two ends for Book and one each for Library and Author, and you can read off, for every end, the multiplicity on both sides.
:::

## Exercise: generate Rails associations and validations

:::exercise[Generate has_many, belongs_to and has_and_belongs_to_many]
Extend `rails_models.rb.j2` so that the generator writes the associations as well. For the Library model, `output/models.rb` must match this file exactly:

```ruby
class Library < ApplicationRecord
  attribute :name, :string
  attribute :address, :string
  has_many :books
end

class Book < ApplicationRecord
  attribute :title, :string
  attribute :pages, :integer
  attribute :release, :datetime
  belongs_to :library
  has_and_belongs_to_many :authors
end

class Author < ApplicationRecord
  attribute :name, :string
  attribute :email, :string
  has_and_belongs_to_many :books
end
```

Rails names associations after the target class: plural for "many" (`:books`), singular for "one" (`:library`). If you have Ruby installed, `ruby -c output/models.rb` should print `Syntax OK`.
:::

:::solution
Add a second inner loop after the attributes: `{% for end in sort_by_timestamp(class.association_ends()) if end.is_navigable %}`. Inside it, compare `end.multiplicity.max` with `end.opposite_end().multiplicity.max`. Many on both sides gives `has_and_belongs_to_many`. Many on the other side only gives `has_many`. One on the other side and many on this side gives `belongs_to`. Build the name with `end.type.name | lower`, adding an `s` for the plural forms. Watch the blank line between classes: `loop.last` helps you avoid a trailing one.
:::

:::exercise[Generate validations from the model]
Make the generator write Rails validations. Every attribute that is not optional (`attr.is_optional` is `False`) gets `validates :<name>, presence: true`. An attribute marked as an external identifier (`is_external_id=True`, a user-facing key such as an ISBN) also gets `uniqueness: true`. Test it by setting `is_external_id=True` on `Book.title` and `is_optional=True` on `Author.email` in `library_model.py`.
:::

:::solution
Add one more loop over `sort_by_timestamp(class.attributes)` with the filter `if not attr.is_optional`, and append `, uniqueness: true` inside `{% if attr.is_external_id %}`. With the two model changes, Book should get `validates :title, presence: true, uniqueness: true` and Author should get no validation for `email`.
:::

To make your generator available in the Web Modeling Editor's :ui[Generate] menu, it has to be registered in a BESSER source checkout: in `SUPPORTED_GENERATORS` in `besser/utilities/web_modeling_editor/backend/config/generators.py`, plus a menu entry in the editor frontend, followed by running the editor locally. The [generator guide](https://besser.readthedocs.io/en/latest/generators/build_generator.html) covers the backend part. [Extend the B-UML metamodel](/labs/metamodel-extension/) shows how to set up the source checkout.
