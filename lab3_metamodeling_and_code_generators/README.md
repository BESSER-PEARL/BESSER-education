# Lab Guide 3: Metamodel extension and code generator improvements

## Welcome to our BESSER lab guide!

In this guide, you will use [BESSER](https://github.com/BESSER-PEARL/BESSER.git) from the perspective of a developer user. Specifically you will extend the B-UML metamodel and improve some code generators.

## 1. Context

BESSER provides the B-UML modeling language for creating different [types of models](https://besser.readthedocs.io/en/latest/buml_language/model_types.html) including structural, object, deployment, graphical user interface, etc. In this guide, we will extend the structural model definition of B-UML and improve some code generators.

The structural model enables the specification of the static structure of an application or system. The metamodel can be accesed in the [BESSER documentation](https://besser.readthedocs.io/en/latest/buml_language/model_types/structural.html), while the source code or implementation in Python is [the repository](https://github.com/BESSER-PEARL/BESSER/blob/master/besser/BUML/metamodel/structural/structural.py).

## 2. Requirements

For this lab guide, [running BESSER locally](https://besser.readthedocs.io/en/latest/installation.html#running-besser-locally) is necessary as we will modify the soure code.

## 3. Code Generators to Improve

BESSER's code generators use [Jinja](https://jinja.palletsprojects.com/en/stable/), a templating engine for Python, used to dynamically generate HTML or other text-based formats by embedding logic within template files. Each generator in BESSER contains at least one jinja template, which traverses the B-UML model to generate code dinamically.

Low-code platforms can generate up to 80% of an application’s code. However, these generators can often be improved or extended to support additional specifications.

Let's explore two possible improvements.

### 3.1 SQLAlchemy Generator

BESSER provides a [code generator that creates SQLAlchemy models](https://besser.readthedocs.io/en/latest/generators/alchemy.html#) to define the structure of a relational database.

Let's consider the following basic model, where a *Library* can has several *Book*s, and a *Book* is written by at least one *Author*.

<div align="center">
  <img src="figs/library_model.png" alt="Example model domain" width="550"/>
</div>

The SQLAlchemy generator currently does not support unique fields. For example, if we want to specify that the book title should be unique (but not necessarily a ForeignKey), the current generator does not allow this.

To address this limitation, we need to extend the Structural metamodel of B-UML, to enable the definition of unique attributes in a class. And then, modify the jinja templates to produce the SQLAlchemy code covering unique fields.

> ### **Exercise:**
>
> Address the limitation above in the SQLAlchemy generator, following the next recomendations:
> - Update the code of the structural metamodel of B-UML, to include a new parameter in the *Property* class to capture the *is_unique* information. This metamodel is defined in the file *besser/BUML/metamodel/structural/structural.py*
> - Check the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/core/constraints.html) to identify how to define unique fields in a table.
> - Update the jinja template of the SQLAlchemy Generator to address the uniqueness of fields. The templates and the generator code are located in the directory *besser/generators/sql_alchemy*

### 3.2 Python Generator


