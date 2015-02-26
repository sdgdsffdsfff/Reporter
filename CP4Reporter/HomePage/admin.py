from django.contrib import admin
from HomePage import models

# Register your models here.
admin.site.register(models.AssignModel)
admin.site.register(models.ReporterModel)
admin.site.register(models.PersonModel)
admin.site.register(models.NoCaseBugModel)
admin.site.register(models.CaseBugModel)
admin.site.register(models.ServerBugModel)
admin.site.register(models.ClientBugModel)
admin.site.register(models.SOABugModel)
admin.site.register(models.InterfaceModel)

