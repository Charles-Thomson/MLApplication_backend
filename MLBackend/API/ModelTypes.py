import graphene
from graphene_django import DjangoObjectType
from DataBase.models import *

# class InstanceAlphaType(DjangoObjectType):
#     class Meta:
#         model = InstanceAlphaBrainDataBaseModel
#         fields = '__all__'

class AlphaAgentInstanceType(DjangoObjectType):
    class Meta:
        model = AlphaBrainInstanceDataBaseModel
        fields = '__all__'
        
class GenerationalLearningInstanceType(DjangoObjectType):
    instance_alpha = graphene.Field(AlphaAgentInstanceType)
    class Meta:
         model = GenerationalLearningInstanceDataBaseModel 
         fields = '__all__'

class InstanceEnvironmentType(DjangoObjectType):
    class Meta:
        model = GenerationalLearningInstanceEnvironmentDataBaseModel  
        fields = '__all__'
            
class GenerationInstanceType(DjangoObjectType):
    class Meta:
        model = GenerationInstanceDataBaseModel
        fields = '__all__'
        
class AgentInstanceType(DjangoObjectType):
    class Meta:
        model = BrainInstanceDataBaseModel
        fields = '__all__'
        
# class GenerationAlpahType(DjangoObjectType):
#     class Meta:
#         model = GenerationAlpahBrainDataBaseModel
#         fields = '__all__'

