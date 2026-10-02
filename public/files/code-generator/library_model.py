from besser.BUML.metamodel.structural import (
    DomainModel, Class, Property, Multiplicity, BinaryAssociation,
    StringType, IntegerType, DateTimeType,
)

# Classes and attributes
library = Class(name="Library")
library.attributes = {
    Property(name="name", type=StringType),
    Property(name="address", type=StringType),
}

book = Class(name="Book")
book.attributes = {
    Property(name="title", type=StringType),
    Property(name="pages", type=IntegerType),
    Property(name="release", type=DateTimeType),
}

author = Class(name="Author")
author.attributes = {
    Property(name="name", type=StringType),
    Property(name="email", type=StringType),
}

# Library 1 --- 0..* Book
lib_book = BinaryAssociation(name="lib_book_assoc", ends={
    Property(name="locatedIn", type=library, multiplicity=Multiplicity(1, 1)),
    Property(name="has", type=book, multiplicity=Multiplicity(0, "*")),
})

# Book 0..* --- 1..* Author
book_author = BinaryAssociation(name="book_author_assoc", ends={
    Property(name="publishes", type=book, multiplicity=Multiplicity(0, "*")),
    Property(name="writtenBy", type=author, multiplicity=Multiplicity(1, "*")),
})

library_model = DomainModel(name="Library_model",
                            types={library, book, author},
                            associations={lib_book, book_author})
