"""
This module defines a domain model for academic research using the BUML metamodel. 
It includes classes, attributes, relationships, and generalizations to represent 
various entities and their interactions in the context of academic research.
"""
from besser.BUML.metamodel.structural import (
    Class, Property, BinaryAssociation, Generalization,
    DomainModel, Multiplicity, StringType, BooleanType,
    DateType
)

# Classes
ResearchEvent = Class(name="ResearchEvent")
Paper = Class(name="Paper")
Conference = Class(name="Conference")
Workshop = Class(name="Workshop")
Symposium = Class(name="Symposium")
Researcher = Class(name="Researcher")

# ResearchEvent class attributes and methods
ResearchEvent_name: Property = Property(name="name", type=StringType)
ResearchEvent_start: Property = Property(name="start", type=DateType)
ResearchEvent_end: Property = Property(name="end", type=DateType)
ResearchEvent.attributes={ResearchEvent_end, ResearchEvent_start, ResearchEvent_name}

# Paper class attributes and methods
Paper_title: Property = Property(name="title", type=StringType)
Paper_submitted_date: Property = Property(name="submitted_date", type=DateType)
Paper_acceptance: Property = Property(name="acceptance", type=BooleanType)
Paper.attributes={Paper_acceptance, Paper_submitted_date, Paper_title}

# Researcher class attributes and methods
Researcher_name: Property = Property(name="name", type=StringType)
Researcher_institution: Property = Property(name="institution", type=StringType)
Researcher.attributes={Researcher_name, Researcher_institution}

# Relationships
paper_authors: BinaryAssociation = BinaryAssociation(
    name="paper_authors",
    ends={
        Property(name="paper", type=Paper, multiplicity=Multiplicity(0, "*")),
        Property(name="authors", type=Researcher, multiplicity=Multiplicity(1, "*"))
    }
)
organizer_list: BinaryAssociation = BinaryAssociation(
    name="organizer_list",
    ends={
        Property(name="event", type=ResearchEvent, multiplicity=Multiplicity(0, "*")),
        Property(name="organizers", type=Researcher, multiplicity=Multiplicity(1, "*"))
    }
)
paper_list: BinaryAssociation = BinaryAssociation(
    name="paper_list",
    ends={
        Property(name="papers", type=Paper, multiplicity=Multiplicity(0, "*")),
        Property(name="event", type=ResearchEvent, multiplicity=Multiplicity(1, 1), is_composite=True)
    }
)

# Generalizations
gen_Symposium_ResearchEvent = Generalization(general=ResearchEvent, specific=Symposium)
gen_Conference_ResearchEvent = Generalization(general=ResearchEvent, specific=Conference)
gen_Workshop_ResearchEvent = Generalization(general=ResearchEvent, specific=Workshop)

# Domain Model
domain_model = DomainModel(
    name="Academic_Research",
    types={ResearchEvent, Paper, Conference, Workshop, Symposium, Researcher},
    associations={paper_authors, organizer_list, paper_list},
    generalizations={gen_Symposium_ResearchEvent, gen_Conference_ResearchEvent, gen_Workshop_ResearchEvent}
)

for cls in domain_model.get_classes():
    print(cls.name)
