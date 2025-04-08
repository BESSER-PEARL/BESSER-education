# Lab Guide 2: Create your code generator with BESSER

## Welcome to our BESSER lab guide!

In this guide, you will learn to use [BESSER](https://github.com/BESSER-PEARL/BESSER.git) from the perspective of a developer user, specifically for developing a code generator.

## 1. Context

BESSER provides the B-UML modeling language for creating different types of models. In this case, we will develop a code generator that takes as input a structural model defined with B-UML and generates Java code representing the object model, i.e., the classes and attributes in the Java language.

To create the code generator, you can utilize the interface provided by BESSER and define a Jinja template for code generation. You can find more information about this in the [BESSER documentation](https://besser.readthedocs.io/en/latest/generators.html). The documentation provides details about BESSER's code generation capabilities, including how to create custom generators and work with Jinja templates.

## 2. Requirements

For this lab guide, the [BESSER basic installation](https://besser.readthedocs.io/en/latest/installation.html#) is sufficient.

## 3. Creating your Code Generator in BESSER

To define a code generator, you should create a class (e.g., *JavaGenerator*) that implements the ``GeneratorInterface``. This ensures that all BESSER generators follow a consistent structure. 

An example can be found in the [java_generator.py](java_generator.py) script. You can reuse this script for the purposes of this guide. In the code, the constructor of the `JavaGenerator` class receives a *DomainModel* (or B-UML structural model) as an input parameter, while the ``generate()`` method handles the code generation. Note that the ``java_template.py.j2`` template is used for code generation, and we need to develop this template.

Download the [java_generator.py](java_generator.py) file, and let's create the Jinja template.

## 4. Jinja template example

Now that we have defined our `JavaGenerator` class, we can create the template that will structure the generated code.

### What is a Jinja Template?

[Jinja](https://jinja.palletsprojects.com/en/stable/) is a templating engine for Python that allows us to dynamically generate text-based content, such as HTML, configuration files, and in our case, Java code.

A Jinja template contains placeholders and control structures (e.g., loops and conditionals) that are later replaced with actual data when rendered. This makes it an ideal tool for generating code based on a model, such as our B-UML model.

### Creating a Jinja Template

Create a file named `templates/java_template.py.j2` and add the following code:

```jinja2
This is a template example to list the name of the classes

{% for class in model.get_classes() %}
    class {{ class.name }}
{% endfor %}
```

This template will generate a basic class declaration for each class in our B-UML model, using a for loop.

### Testing the Code Generator

Now that we have defined our Jinja template, let's test the code generator by applying it to a sample B-UML model.

We will start by defining the library model with its classes (*Library*, *Book*, and *Author*), and then use the generator to produce the corresponding Java code. Execute the following Python code, and check the output folder for the generated code:

```python
from besser.BUML.metamodel.structural import DomainModel, Class, Property, \
    Multiplicity, BinaryAssociation, StringType, IntegerType, DateTimeType
from java_generator import JavaGenerator

############################
#   BUML model definition  #
############################

# Library attributes definition
library_name: Property = Property(name="name", type=StringType)
address: Property = Property(name="address", type=StringType)
# Library class definition
library: Class = Class(name="Library", attributes={library_name, address})

# Book attributes definition
title: Property = Property(name="title", type=StringType)
pages: Property = Property(name="pages", type=IntegerType)
release: Property = Property(name="release", type=DateTimeType)
# Book class definition
book: Class = Class(name="Book", attributes={title, pages, release})

# Author attributes definition
author_name: Property = Property(name="name", type=StringType)
email: Property = Property(name="email", type=StringType)
# Author class definition
author: Class = Class(name="Author", attributes={author_name, email})

# Library-Book association definition
located_in: Property = Property(name="locatedIn", type=library, multiplicity=Multiplicity(1, 1))
has: Property = Property(name="has", type=book, multiplicity=Multiplicity(0, "*"))
lib_book_association: BinaryAssociation = BinaryAssociation(name="lib_book_assoc", ends={located_in, has})

# Book-Author association definition
publishes: Property = Property(name="publishes", type=book, multiplicity=Multiplicity(0, "*"))
writed_by: Property = Property(name="writtenBy", type=author, multiplicity=Multiplicity(1, "*"))
book_author_association: BinaryAssociation = BinaryAssociation(name="book_author_assoc", ends={writed_by, publishes})

# Domain model definition
library_model: DomainModel = DomainModel(name="Library model", types={library, book, author},
                                        associations={lib_book_association, book_author_association})

############################
#      Code Generation     #
############################

generator: JavaGenerator = JavaGenerator(model=library_model)
generator.generate()
```

The B-UML model defined in the previous code (Library model) corresponds to the diagram in the next figure. Therefore, by running the above code, you should obtain a file containing the names of the three classes (*Library*, *Book*, and *Author*) as output.

<div align="center">
  <img src="figs/library_model.png" alt="Example model domain" width="550"/>
</div>


## 5. Exercise

Modify the `java_template.py.j2` to build a Java code generator. In other words, your code generator should produce a set of classes in the Java language with their respective methods, attributes, etc. For example, when providing a model like the one in the [previous figure](figs/library_model.png), your code generator should produce a file containing the following code:

```java
import java.util.List;
import java.util.ArrayList;
import java.time.LocalDate;

public class Library {
    private String name;
    private String address;
    private List<Book> books;

    public Library(String name, String address) {
        this.name = name;
        this.address = address;
        this.books = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public List<Book> getBooks() {
        return books;
    }

    public void addBook(Book book) {
        if (!books.contains(book)) {
            books.add(book);
            book.setLibrary(this);
        }
    }

    @Override
    public String toString() {
        return "Library{name='" + name + "', address='" + address + "', books=" + books.size() + "}";
    }
}

class Book {
    private String title;
    private int pages;
    private LocalDate release;
    private List<Author> authors;
    private Library library;

    public Book(String title, int pages, LocalDate release) {
        this.title = title;
        this.pages = pages;
        this.release = release;
        this.authors = new ArrayList<>();
        this.library = null;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public int getPages() {
        return pages;
    }

    public void setPages(int pages) {
        this.pages = pages;
    }

    public LocalDate getRelease() {
        return release;
    }

    public void setRelease(LocalDate release) {
        this.release = release;
    }

    public List<Author> getAuthors() {
        return authors;
    }

    public void addAuthor(Author author) {
        if (!authors.contains(author)) {
            authors.add(author);
            author.addBook(this);
        }
    }

    public Library getLibrary() {
        return library;
    }

    public void setLibrary(Library library) {
        if (this.library != library) {
            this.library = library;
            library.addBook(this);
        }
    }

    @Override
    public String toString() {
        return "Book{title='" + title + "', pages=" + pages + ", release=" + release + 
               ", authors=" + authors.size() + ", library=" + (library != null ? library.getName() : "None") + "}";
    }
}

class Author {
    private String name;
    private String email;
    private List<Book> books;

    public Author(String name, String email) {
        this.name = name;
        this.email = email;
        this.books = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public List<Book> getBooks() {
        return books;
    }

    public void addBook(Book book) {
        if (!books.contains(book)) {
            books.add(book);
            book.addAuthor(this);
        }
    }

    @Override
    public String toString() {
        return "Author{name='" + name + "', email='" + email + "', books=" + books.size() + "}";
    }
}
```
