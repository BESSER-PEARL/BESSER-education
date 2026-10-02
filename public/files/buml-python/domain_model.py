"""Academic research domain model, written with the B-UML Python API (BESSER 8.0).

Researchers write papers, papers are presented at research events, and an event
is either a conference or a workshop. Run it with:  python domain_model.py
"""
from besser.BUML.metamodel.structural import (
    BinaryAssociation, BooleanType, Class, DateType, DomainModel, Enumeration,
    EnumerationLiteral, Generalization, Multiplicity, Property, StringType,
)

# Enumeration
EventMode = Enumeration(name="EventMode", literals={
    EnumerationLiteral(name="in_person"),
    EnumerationLiteral(name="online"),
    EnumerationLiteral(name="hybrid"),
})

# Classes and their attributes
Researcher = Class(name="Researcher", attributes={
    Property(name="name", type=StringType),
    Property(name="institution", type=StringType),
})

Paper = Class(name="Paper", attributes={
    Property(name="title", type=StringType),
    Property(name="submitted", type=DateType),
    Property(name="acceptance", type=BooleanType),
})

ResearchEvent = Class(name="ResearchEvent", attributes={
    Property(name="name", type=StringType),
    Property(name="start", type=DateType),
    Property(name="end", type=DateType),
    Property(name="mode", type=EventMode),
})

Conference = Class(name="Conference", attributes={Property(name="acronym", type=StringType)})
Workshop = Class(name="Workshop", attributes={Property(name="topic", type=StringType)})

# Associations: each end is a Property named after the role it plays.
authorship = BinaryAssociation(name="authorship", ends={
    Property(name="papers", type=Paper, multiplicity=Multiplicity(0, "*")),
    Property(name="authors", type=Researcher, multiplicity=Multiplicity(1, "*")),
})

# Composition: an event owns its papers (is_composite goes on the whole's end).
presented_at = BinaryAssociation(name="presented_at", ends={
    Property(name="papers", type=Paper, multiplicity=Multiplicity(0, "*")),
    Property(name="event", type=ResearchEvent, multiplicity=Multiplicity(1, 1), is_composite=True),
})

# Generalizations: a Conference is a ResearchEvent, and so is a Workshop.
conference_is_event = Generalization(general=ResearchEvent, specific=Conference)
workshop_is_event = Generalization(general=ResearchEvent, specific=Workshop)

# The domain model groups everything.
domain_model = DomainModel(
    name="Research_Lab",
    types={Researcher, Paper, ResearchEvent, Conference, Workshop, EventMode},
    associations={authorship, presented_at},
    generalizations={conference_is_event, workshop_is_event},
)

if __name__ == "__main__":
    for cls in sorted(domain_model.get_classes(), key=lambda c: c.name):
        attributes = ", ".join(f"{a.name}: {a.type.name}" for a in sorted(cls.attributes, key=lambda a: a.name))
        print(f"{cls.name}({attributes})")
