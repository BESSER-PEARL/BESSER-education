---
title: Extend the B-UML metamodel and a generator
number: 12
track: extend
summary: A BESSER source checkout where Property has a new max_length concept, the SQLAlchemy generator uses it, and a pytest test proves it.
duration: 90
level: Advanced
setup: [Python]
needs:
  - Python 3.11 or 3.12
  - Git
  - About 1 GB of free disk space for the checkout and its dependencies
  - A JDK (javac) for the Java exercise, optional
outcomes:
  - Set up an editable BESSER source checkout and run its test suite
  - Check what a generator already supports before changing it
  - Add a validated attribute to a B-UML metamodel class
  - Change a built-in Jinja template so it uses the new concept
  - Write a pytest test that fails before the change and passes after it
before: [code-generator]
files: []
updated: 2026-10-02
version: "8.0"
draft: false
---

Generators can only use what the metamodel can express. When a project needs a concept B-UML does not have yet, you extend the metamodel and then teach a generator to use it. This is how most contributions to BESSER start.

In this lab you add a maximum length to attributes. In BESSER 8.0.1 every string attribute becomes a `String(100)` column in the SQLAlchemy generator, whether it holds a 13-character ISBN or a long title. You add `max_length` to the `Property` metaclass, use it in the SQLAlchemy template, and protect the change with a test. The exercise then applies the same method to the Java generator.

You work in your own clone of the BESSER repository, in a separate virtual environment, so your normal `pip install besser` setup stays untouched.

## Set up a BESSER source checkout

1. Clone the `development` branch and create a virtual environment inside the clone:

   ```bash
   git clone --branch development https://github.com/BESSER-PEARL/BESSER.git
   cd BESSER
   python -m venv .venv
   source .venv/bin/activate
   ```

   ```powershell
   git clone --branch development https://github.com/BESSER-PEARL/BESSER.git
   cd BESSER
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install BESSER in editable mode. Python then imports BESSER from your clone, so every change you make to the source takes effect without reinstalling:

   ```bash
   python -m pip install -e .
   ```

3. Check that Python picks up the clone, not a PyPI copy:

   ```bash
   python -c "import besser; print(besser.__file__)"
   ```

   ```text
   /path/to/BESSER/besser/__init__.py
   ```

4. Run the tests for the parts you are going to touch. `pytest` is installed with BESSER's own dependencies:

   ```bash
   python -m pytest tests/BUML/metamodel/structural tests/generators/sqlalchemy tests/generators/java -q
   ```

   ```text
   195 passed in 15.99s
   ```

:::troubleshoot
If `besser.__file__` points into `site-packages` instead of your clone, the virtual environment is not active or another BESSER installation shadows it. Activate `.venv` again, and make sure no `PYTHONPATH` variable points at another BESSER folder.
:::

:::checkpoint
`besser.__file__` points into your clone and the three test folders pass. The exact count can differ if `development` has moved on since 8.0.1; what matters is that nothing fails.
:::

## Check what the generators already support

Before you extend anything, find out what is really missing. Earlier versions of this lab asked for unique attributes in SQLAlchemy and for methods in the Java generator. Both exist now. Create a scratch folder outside the clone, for example `../playground/`, and save this as `check_current.py`:

```python
from besser.BUML.metamodel.structural import (
    Class, DomainModel, Property, StringType, IntegerType,
)
from besser.generators.sql_alchemy import SQLAlchemyGenerator

book = Class(name="Book")
book.attributes = {
    Property(name="title", type=StringType),
    Property(name="isbn", type=StringType, is_external_id=True),
    Property(name="pages", type=IntegerType),
}
model = DomainModel(name="Library", types={book})
SQLAlchemyGenerator(model=model, output_dir="output").generate(dbms="sqlite")
```

Run it with `python check_current.py` and look at the `Book` class in `output/sql_alchemy.py`:

```python
class Book(Base):
    __tablename__ = "book"
    id: Mapped_[int] = mapped_column(primary_key=True)
    title: Mapped_[str] = mapped_column(String_(100))
    isbn: Mapped_[str] = mapped_column(String_(100), unique=True)
    pages: Mapped_[int] = mapped_column(Integer_)
```

Two things to notice:

- Uniqueness is covered. `Property` has `is_external_id` for user-facing keys, and the SQLAlchemy and Django generators turn it into `unique=True`.
- Every string is `String_(100)`. The size comes from a fixed `TYPES` mapping in `besser/generators/sql_alchemy/sql_alchemy_generator.py`, and the model has no way to change it:

  ```bash
  python -c "from besser.BUML.metamodel.structural import Property, StringType; Property(name='isbn', type=StringType, max_length=13)"
  ```

  ```text
  TypeError: Property.__init__() got an unexpected keyword argument 'max_length'
  ```

For Java, generating a class with methods shows that the generator writes a stub for each method:

```java
public void searchBook(String title) {
    // TODO: implement searchBook
    throw new UnsupportedOperationException("searchBook is not implemented");
}
```

:::checkpoint
You have seen `unique=True` on `isbn`, `String_(100)` on both string columns, and the `TypeError` for `max_length`. That gap is what you close next.
:::

## Find the Property metaclass

The structural metamodel lives in one file: `besser/BUML/metamodel/structural/structural.py`. Find the class that represents attributes and association ends:

```bash
grep -n "class Property" besser/BUML/metamodel/structural/structural.py
```

```powershell
Select-String -Pattern "class Property" -Path besser\BUML\metamodel\structural\structural.py
```

Both print line 581:

```text
581:class Property(TypedElement):
```

Read how an existing flag is built, for example `is_external_id`. Each concept on a metaclass has four parts, and your new one needs all four:

1. A constructor argument with a default, in `Property.__init__`.
2. A private attribute behind a `@property` getter and a setter. The setter is where the metamodel rejects invalid values: `is_external_id` refuses to be combined with `is_optional`.
3. A line in `__repr__`, so the value shows up when you print a property.
4. An entry in the class docstring, under both `Args` and `Attributes`.

The metaclass is documented on the [structural model page](https://besser.readthedocs.io/en/latest/buml_language/model_types/structural.html).

:::checkpoint
You have found `Property.__init__`, the `is_external_id` getter and setter, and `__repr__` in `structural.py`.
:::

## Add max_length to Property

1. Add the argument at the end of the `__init__` signature. Callers can pass constructor arguments by position, so a new parameter in the middle of the signature would silently shift their values:

   ```python
                    timestamp: datetime = None, metadata: Metadata = None, is_derived: bool = False,
                    uncertainty: float = 0.0, max_length: int = None):

           super().__init__(name, type, timestamp, metadata, visibility, is_derived, uncertainty)
           self.max_length: int = max_length
   ```

2. Add the getter and setter next to `default_value`. `None` means no limit; anything else must be a positive integer:

   ```python
       @property
       def max_length(self) -> int:
           """int: Get the maximum length of the property's value (None means no limit)."""
           return self.__max_length

       @max_length.setter
       def max_length(self, max_length: int):
           """int: Set the maximum length of the property's value.

           Raises:
               ValueError: if max_length is not None and not a positive integer.
           """
           if max_length is not None and (not isinstance(max_length, int) or max_length <= 0):
               raise ValueError("max_length must be a positive integer or None.")
           self.__max_length = max_length
   ```

3. Add `f'max_length={self.max_length}, '` to `__repr__`, after the `default_value` line, and describe `max_length (int)` in the docstring.

4. Try it:

   ```python
   from besser.BUML.metamodel.structural import Property, StringType

   print(Property(name="isbn", type=StringType, max_length=13).max_length)
   print(Property(name="title", type=StringType).max_length)
   try:
       Property(name="bad", type=StringType, max_length=0)
   except ValueError as e:
       print("ValueError:", e)
   ```

   ```text
   13
   None
   ValueError: max_length must be a positive integer or None.
   ```

Because of the editable install, you did not reinstall anything for this to work.

:::checkpoint
A property accepts `max_length=13`, defaults to `None`, and rejects `0` with a `ValueError`.
:::

## Use max_length in the SQLAlchemy template

The SQLAlchemy generator renders each attribute in the `render_attributes` macro of `besser/generators/sql_alchemy/templates/helpers.py.j2`. The column type is picked here:

```jinja
mapped_column({% if attribute.type.name in enumerations|map(attribute='name') %}Enum({{ attribute.type.name }}){% else %}{{types[attribute.type.name]}}{% endif %}
```

`types` is the generator's `TYPES` mapping, where `str` is `String_(100)`. Add a branch for string attributes that have a `max_length`, and keep the mapping as the fallback:

```jinja
mapped_column({% if attribute.type.name in enumerations|map(attribute='name') %}Enum({{ attribute.type.name }}){% elif attribute.type.name == 'str' and attribute.max_length %}String_({{ attribute.max_length }}){% else %}{{types[attribute.type.name]}}{% endif %}
```

Edit only that part of the line; the `Mapped_[...]` part before it stays as it is.

Now generate a model that uses the new concept. In your playground folder, save `max_length_demo.py`:

```python
from besser.BUML.metamodel.structural import (
    Class, DomainModel, Property, StringType, IntegerType,
)
from besser.generators.sql_alchemy import SQLAlchemyGenerator
from besser.generators.sql import SQLGenerator

book = Class(name="Book")
book.attributes = {
    Property(name="title", type=StringType, max_length=255),
    Property(name="isbn", type=StringType, max_length=13, is_external_id=True),
    Property(name="pages", type=IntegerType),
}
model = DomainModel(name="Library", types={book})

SQLAlchemyGenerator(model=model, output_dir="output").generate(dbms="sqlite")
SQLGenerator(model=model, output_dir="output", sql_dialect="sqlite").generate()
```

Run it. `output/sql_alchemy.py` now has the sizes from the model:

```python
class Book(Base):
    __tablename__ = "book"
    id: Mapped_[int] = mapped_column(primary_key=True)
    title: Mapped_[str] = mapped_column(String_(255))
    isbn: Mapped_[str] = mapped_column(String_(13), unique=True)
    pages: Mapped_[int] = mapped_column(Integer_)
```

The SQL generator builds its DDL from the SQLAlchemy code, so `output/tables_sqlite.sql` follows without any change to it:

```sql
CREATE TABLE book (
	id INTEGER NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	isbn VARCHAR(13) NOT NULL, 
	pages INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (isbn)
)

;
```

:::troubleshoot
If the output still shows `String_(100)`, Python is importing another BESSER installation. Run the playground scripts with the `.venv` of your clone active, and check `besser.__file__` again.
:::

:::checkpoint
`title` is `String_(255)`, `isbn` is `String_(13)` and still unique, and the DDL shows `VARCHAR(255)` and `VARCHAR(13)`.
:::

## Write a test for the new concept

BESSER's tests mirror the source tree: generator tests live in `tests/generators/<generator>/`. Create `tests/generators/sqlalchemy/test_max_length.py`:

```python
import os

import pytest

from besser.BUML.metamodel.structural import Class, DomainModel, Property, StringType
from besser.generators.sql_alchemy import SQLAlchemyGenerator


def _book_model(**isbn_kwargs) -> DomainModel:
    book = Class(name="Book")
    book.attributes = {
        Property(name="title", type=StringType),
        Property(name="isbn", type=StringType, **isbn_kwargs),
    }
    return DomainModel(name="Library", types={book})


def _generate(model, tmp_path) -> str:
    SQLAlchemyGenerator(model=model, output_dir=str(tmp_path)).generate(dbms="sqlite")
    with open(os.path.join(tmp_path, "sql_alchemy.py"), encoding="utf-8") as f:
        return f.read()


def test_max_length_defaults_to_none():
    assert Property(name="title", type=StringType).max_length is None


@pytest.mark.parametrize("bad", [0, -5, "13"])
def test_max_length_rejects_invalid_values(bad):
    with pytest.raises(ValueError):
        Property(name="isbn", type=StringType, max_length=bad)


def test_max_length_sets_the_column_size(tmp_path):
    code = _generate(_book_model(max_length=13), tmp_path)
    assert "isbn: Mapped_[str] = mapped_column(String_(13))" in code
    # attributes without max_length keep the generator default
    assert "title: Mapped_[str] = mapped_column(String_(100))" in code
```

`tmp_path` is a pytest fixture that gives each test its own empty folder, so the test never writes into your clone.

Run it:

```bash
python -m pytest tests/generators/sqlalchemy/test_max_length.py -v
```

```text
tests/generators/sqlalchemy/test_max_length.py::test_max_length_defaults_to_none PASSED [ 20%]
tests/generators/sqlalchemy/test_max_length.py::test_max_length_rejects_invalid_values[0] PASSED [ 40%]
tests/generators/sqlalchemy/test_max_length.py::test_max_length_rejects_invalid_values[-5] PASSED [ 60%]
tests/generators/sqlalchemy/test_max_length.py::test_max_length_rejects_invalid_values[13] PASSED [ 80%]
tests/generators/sqlalchemy/test_max_length.py::test_max_length_sets_the_column_size PASSED [100%]

============================== 5 passed in 0.42s ==============================
```

A test that passes proves little until you have seen it fail. Set your two source changes aside, run the test, then bring them back:

```bash
git stash
python -m pytest tests/generators/sqlalchemy/test_max_length.py -q
git stash pop
```

```text
5 failed in 0.55s
```

`git stash` only takes tracked files, so the new test file stays while the metamodel and template changes are set aside.

:::checkpoint
The five tests pass with your changes and all five fail without them.
:::

## Run the regression tests

A metamodel change can break code far from where you made it, such as converters or other generators that build `Property` objects. Run the same three folders as at the start:

```bash
python -m pytest tests/BUML/metamodel/structural tests/generators/sqlalchemy tests/generators/java -q
```

```text
200 passed in 7.10s
```

That is the 195 tests from the start plus your 5. To run the whole suite the way BESSER's CI does, install the web editor backend requirements first; some tests import them. The full run has more than 5000 tests and takes about ten minutes:

```bash
python -m pip install -r besser/utilities/web_modeling_editor/backend/requirements.txt
python -m pytest tests/ -q --ignore=tests/generators/nn
```

:::note
`max_length` now exists in Python models only. To use it from the Web Modeling Editor, the JSON converters in `besser/utilities/web_modeling_editor/backend/services/converters/` and the editor's attribute form would also need to carry it. The `is_external_id` flag is a complete example of a property that goes through all those layers: search the source for `is_external_id` and `isExternalId` to see each place. The [contributor guide](https://besser.readthedocs.io/en/latest/contributor_guide.html) describes how to open a pull request.
:::

:::checkpoint
The three folders pass with 5 more tests than at the start, and no existing test fails.
:::

## Exercise: abstract classes in the Java generator

:::exercise[Generate abstract classes and abstract methods in Java]
The metamodel already has `Class(is_abstract=True)` and `Method(is_abstract=True)`, but the Java generator ignores both. For this model:

```python
publication = Class(name="Publication", is_abstract=True)
publication.attributes = {Property(name="title", type=StringType)}
publication.methods = {Method(name="price", type=FloatType, is_abstract=True)}

book = Class(name="Book")
book.attributes = {Property(name="pages", type=IntegerType)}
model = DomainModel(name="Library", types={publication, book},
                    generalizations={Generalization(general=publication, specific=book)})
```

BESSER 8.0.1 generates `public class Publication {` and a `price()` method with a body that throws. Change the templates in `besser/generators/java_classes/templates/` so that:

- an abstract class is declared `public abstract class Publication {`,
- an abstract method has no body: `public abstract float price();`,
- the generated files still compile with `javac *.java`.

Then add a test in `tests/generators/java/` and run the Java tests again.
:::

:::solution
The class header and the method loop are both in `java_template.py.j2`. Use `class_obj.is_abstract` and `method.is_abstract`. The compile requirement is the hard part: once `price()` is abstract, `Book` no longer compiles because it does not implement it. A concrete class must emit a stub for every abstract method it inherits; `class_obj.all_parents()` gives you the ancestors to collect them from. Look at `tests/generators/java/test_java_generator.py`: it already contains a test that compiles the generated code when `javac` is available, which you can copy.
:::

:::exercise[Keep max_length when a model is saved as Python code]
`besser.utilities.domain_model_to_code(model, file_path)` writes a model back out as a B-UML Python script. The web editor uses it for its B-UML export. Right now it drops `max_length`. Make it write `max_length=13` when an attribute has one, and write a round-trip test: build a model, save it, execute the file, and check that the attribute still has `max_length == 13`.
:::

:::solution
The attribute lines are built in `besser/utilities/buml_code_builder/domain_model_builder.py`, next to the existing `is_external_id_str` variable. There are two places: one for regular classes and one for association classes. Follow the pattern of `is_external_id_str`: an empty string when the value is `None`, otherwise `, max_length=13`.
:::
