from besser.BUML.metamodel.structural import NamedElement, DomainModel, Type, Class, \
        Property, PrimitiveDataType, Multiplicity, Association, BinaryAssociation, Generalization, \
        GeneralizationSet, AssociationClass, StringType, DateType, BooleanType, IntegerType

# Paper class definition
tittle: Property = Property(name="tittle", type=StringType)
submitted_date: Property = Property(name="submitted_date", type=DateType)
acceptance: Property = Property(name="acceptance", type=BooleanType)
paper: Class = Class(name="Paper", attributes={tittle, submitted_date, acceptance})

# Researcher class definition
name: Property = Property(name="name", type=StringType)
institution: Property = Property(name="institution", type=StringType)
researcher: Class = Class(name="Researcher", attributes={name, institution})

# ResearchEvent class definition
event_name: Property = Property(name="name", type=StringType)
start: Property = Property(name="start", type=DateType)
end: Property = Property(name="end", type=DateType)
research_event: Class = Class(name="ResearchEvent", attributes={event_name, start, end})

# Conference class definition
conference: Class = Class(name="Conference", attributes=set())

# Workshop class definition
workshop: Class = Class(name="Workshop", attributes=set())

# Symposium class definition
symposium: Class = Class(name="Symposium", attributes=set())

# Relationships
is_authored_by: BinaryAssociation = BinaryAssociation(name="is_authored_by", ends={
        Property(name="is_authored_by", type=paper, multiplicity=Multiplicity(0, "*")),
        Property(name="is_authored_by", type=researcher, multiplicity=Multiplicity(1, "*"))})
organizers: BinaryAssociation = BinaryAssociation(name="organizers", ends={
        Property(name="organizers", type=research_event, multiplicity=Multiplicity(0, "*")),
        Property(name="organizers", type=researcher, multiplicity=Multiplicity(1, "*"))})
papers: BinaryAssociation = BinaryAssociation(name="papers", ends={
        Property(name="papers", type=research_event, multiplicity=Multiplicity(1, 1), is_navigable=False, is_composite=True),
        Property(name="papers", type=paper, multiplicity=Multiplicity(0, "*"))})

# Generalizations
gen_ResearchEvent_Conference: Generalization = Generalization(general=research_event, specific=conference)
gen_ResearchEvent_Workshop: Generalization = Generalization(general=research_event, specific=workshop)
gen_ResearchEvent_Symposium: Generalization = Generalization(general=research_event, specific=symposium)
ResearchEvent_generalization_set: GeneralizationSet = GeneralizationSet(name="ResearchEvent_gen_set",
                                                                        generalizations={gen_ResearchEvent_Conference, 
                                                                                        gen_ResearchEvent_Workshop, 
                                                                                        gen_ResearchEvent_Symposium},
                                                                        is_disjoint=True, is_complete=True)


# Domain Model
buml_model: DomainModel = DomainModel(name="Domain Model",
                                types={paper, researcher, research_event, conference, workshop, symposium},
                                associations={is_authored_by, organizers, papers},
                                generalizations={gen_ResearchEvent_Conference, gen_ResearchEvent_Workshop, gen_ResearchEvent_Symposium})


for cls in buml_model.get_classes():
    print(cls.name)
