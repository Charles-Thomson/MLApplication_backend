Back end - business, API, and data storage logic of the Machine Learning application *** See MLApplication_Frontend for presentation layer ***
The aim of the application is to generate and train neural networks in a predefined environment.
Requirements:

Django 5.0.3
django-cors-headers 4.3.1
django-environ 0.11.2
graphene-django 3.2.0
graphql-core 3.2.3
graphql-relay 3.2.0
psycopg2 2.9.9
pytest 8.1.1
pytest-django 4.8.0
numpy 1.26.4
jsonpickle 3.0.3

The main process:

- API receive work item
- Data formatting: Format work item into formatted_work_item
- Staging: Stage formatted work item for processing
- Processing: Process the staged work item


During Processing:

- Each instance will generate an initial set of randomly weighted neural networks. Generation 0.
- Each network that achieves a fitness above the defined value will be classed as viable
- At the end of the generation, viable networks are randomly selected to be amalgamated to produce the next generation. Generation 1.
- Process is repeated until the newly produced generation of networks is unable to achieve a high enough fitness
- Fitness is increased per generation by the average fitness of the previous generation + 10%
- The learning process that is currently implemented is reinforcement generational learning.

*** API ***

GraphQL based API built around a single core schema. Endpoints are marked.
Models are defined in relation to the database models.

All models are currently exposing all fields *
*** Database ***

ORM based PostgreSQL database - Currently being hosted using PgAdmin 4

Contains database models definitions
Model conversion functions

*** Data Formatting ***

Formatting functions for the conversion of a new instance, given by API call
Contains class for a formatted work item

*** Staging ***

Takes a formatted work item and generates a staged work item based on the work item
This includes but is not limited to the partial creation of generator functions and the Environment

*** Processing ***

Main Process
Takes a staged work item and processes. Will push data to Database where relevant
Separated down into;

 - Instance, for the over-processing of the instance
 - Generation, each instance will have X number of generations
 - Agent, each generation will have x number of agents"
