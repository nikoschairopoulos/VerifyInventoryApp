from django.contrib import admin
from inventory.models import (Inventory,
                              Component,
                              Factor,
                              Wall_Materials,
                              RegressionValues,
                              SimaPro_runs,
                              DeletedComponent)

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Component)
admin.site.register(Factor)
admin.site.register(Wall_Materials)
#admin.site.register(RegressionValues)
admin.site.register(SimaPro_runs)
#admin.site.register(DeletedComponent)