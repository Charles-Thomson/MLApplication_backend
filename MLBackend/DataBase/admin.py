from django.contrib import admin
from . import models
admin.site.register(models.GenerationalLearningInstanceDataBaseModel)
admin.site.register(models.GenerationInstanceDataBaseModel)
admin.site.register(models.BrainInstanceDataBaseModel)

# admin.site.register(models.InstanceAlphaBrainDataBaseModel)
# admin.site.register(models.GenerationAlpahBrainDataBaseModel)
admin.site.register(models.AlphaBrainInstanceDataBaseModel)
admin.site.register(models.GenerationalLearningInstanceEnvironmentDataBaseModel)