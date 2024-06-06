import json
import logging
import graphene
from API.ModelTypes import *
from graphene import String
from graphene.types.generic import GenericScalar
from DataFormatting.work_item_data_formatting import format_work_item_json_to_work_item
from DataBase.ModelFunctions import generational_learning_instance_functions
from DataBase.ModelFunctions import generation_instance_functions
from Staging.staging import stage_work_item_for_processing
from datetime import datetime

from application_logging.logging_functions.general_system_logging import general_system_logger_generator

from processing.instance_processing import ProcessInstance




class Query(graphene.ObjectType):
    """The base Query for the GQL API
        - contains GraphQL fields
        - conatins GraphQL Resolvers

    Args:
        graphene (_type_): _description_
    """

    # **** GraphQL fields ****

    new_work_item = GenericScalar(input_config=String(default_value="no_config_given"))

    # ** Getting ID's **
    get_all_instance_ids = graphene.List(graphene.String)

    get_all_generation_ids_from_instance_by_id = graphene.List(
        graphene.String, instance_id=graphene.String()
    )

    # ** Getting Objects **

    get_instance_base_data_by_id = graphene.Field(
        GenerationalLearningInstanceType, instanceId=graphene.String()
    )

    get_generation_and_agents = graphene.Field(
        GenerationInstanceType,
        instance_id=graphene.String(),
        generationId=graphene.String(),
    )
    
    get_all_alphas = graphene.List(
        AlphaAgentInstanceType,
        instance_id=graphene.String()
    )
    
    save_new_model = graphene.List(graphene.String)

    def resolve_save_new_model(self, info):
        instance_ref = (
            generational_learning_instance_functions.add_Generational_Learning_Instance_to_data_base()
        )

        generation_instance_functions.add_generation_instance_to_DB(
            referance=instance_ref
        )
        
        return "done"

    # **** GraphQL Resolvers ****

    def resolve_new_work_item(self, info, input_config: json):
        """
        Recieved a new work item

        Args:
            info (_type_): Requiered Arg
            input_config (json): The configuration data of the new work item
        """
        
        
        general_system_logger = logging.getLogger("general_system_logger")
        general_system_logger.info(f"New work item recived: {datetime.now()}")
        
        
        try:
            new_work_item = format_work_item_json_to_work_item(input_config)
        except Exception as e:
            general_system_logger.info(f"FORMATTING ERROR: {e}")
            
        try:
            staged_work_item = stage_work_item_for_processing(new_work_item)
        except Exception as e:
            general_system_logger.error(f"STAGING ERROR : {e}")
            
        try:
            new_processing_instance: ProcessInstance = ProcessInstance(staged_work_item)
            general_system_logger.info(f"ProcessInstance Call")
            new_processing_instance.process_instance(logging_variables=new_processing_instance.logging_variables)
            
        except Exception as e: 
            general_system_logger.error(f"PROCESSING ERROR : {e}")
            
        return "Done";
        
        
    def resolve_get_all_instance_ids(self, info) -> json :
        """Resolver to get all the stored ID's of all GenerationalLearningInstance's

        Args:
            self: Base field
            info: Requiered argument

        Returns:
            Json(List[str]): List, in JSON form, containg the ID's of each GenerationalLearningInstance
        """
        data = GenerationalLearningInstanceDataBaseModel.objects.values_list(
            "instance_id", flat=True
        )
        print(data)
        return data

    def resolve_get_all_generation_ids_from_instance_by_id(self, info, instance_id):
        """Resolver to get all the stored ID's of all GenerationInstance with the Given FK of instance_id

        Args:
            self: Base field
            info: Requiered argument
            instance_id (string): The ID of a GenerationalLearningInstanceDataBaseModel

        Returns:
            Json(List[str]): List, in JSON form, containg the ID's of each GenerationalInstance within a GenerationalLearningInstanceDataBaseModel
        """
        full_instances = GenerationalLearningInstanceDataBaseModel.objects.get(
            instance_id=instance_id
        )
        generation_instances = full_instances.generation_instance.values_list(
            "generation_id", flat=True
        )

        return generation_instances
    
    def resolve_get_all_alphas(self,info, instance_id):
        """Get all the Alpha AGents associated with a Learning instance

        Args:
            info (_type_): _description_
            instace_id (str): ID of the Instance 
        """
        
        # THIS WORKS
        # Next need to make the call in the front end and sort the showing of the data from there
        
        return AlphaBrainInstanceDataBaseModel.objects.filter(instance_relation__instance_id=instance_id)
        
    def resolve_get_generation_and_agents(self, info, instance_id, generationId):
        """Get a generation from a given instance with all associated agents

        Potentail Bug:
        Can get generations from seperate instance with the same id e.g genertion_1 from instance 1 and 2 ect

        Args:
            self: Base field
            info: Requiered argument
            generationId (string): The ID of a GenerationInstance
 
        Returns:
            JSON: The generation with all related agents
        """

        generation = GenerationInstanceDataBaseModel.objects.prefetch_related(
            "brain_instance"
        ).get(generation_id=generationId)

        return generation

    def resolve_get_instance_base_data_by_id(self, info, instanceId):
        """Get the InstanceAlpha and InstanceEnviroment for a GenerationalLearningInstanceDataBaseModel

        Args:
            self: Base field
            info: Requiered argument
            instanceId (string): The ID of a GenerationalLearningInstanceDataBaseModel

        Returns:
            JSON: JSON of the the Instance Alpha and the Instance Enviroment Data
        """

        instance = GenerationalLearningInstanceDataBaseModel.objects.prefetch_related(
            "instance_environment"
        ).get(instance_id=instanceId)
        print(instance.instance_id)
        return instance


schema = graphene.Schema(query=Query)
