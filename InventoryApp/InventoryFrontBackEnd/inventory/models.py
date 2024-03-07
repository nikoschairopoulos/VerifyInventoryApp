from django.db import models
from django.conf import settings

'''
models:  1.users
         2.Inventory
         3.Components

relations:
#user table (DRF MODEL) 1 - n with inventories
#inventory table   n - n with components table
'''
# Create your models here.

class Component(models.Model):
    name = models.CharField(max_length=50)
    # here add the attributes as at excell inventory:
    #installed_ugs =  models.FloatField() 
    component_type = models.CharField(max_length=50,db_column='type')
    component_subtype = models.CharField(max_length=50,db_column='subtype',null=True)
    capex_per_ugs =  models.FloatField(db_column='capex/u.g.s.') 
    opex_per_capex = models.FloatField(db_column='opex_per_capex') 
    embodied_co2_per_ugs = models.FloatField(db_column='embodied_co2/u.g.s.') 
    embodied_pe_per_ugs = models.FloatField(db_column='embodied_pe/u.g.s.') 
    lifetime = models.FloatField() 
    pref_cost = models.FloatField(db_column='Pref_cost') 
    pref_env = models.FloatField(db_column='Pref_env') 
    scale_cost = models.FloatField() 
    scale_env = models.FloatField() 
    major_upgrade_point = models.FloatField() 
    major_upgrade_share = models.FloatField() 
    annual_performance_degradation = models.FloatField() 
    replace_or_die = models.CharField(max_length=20)
    SHEET_TYPE = models.CharField(max_length=20)             # HERE WE DECLERE THE SHEET_TYPE  e.g El.Generators,Insulation etc
    IS_MAIN_INVENTORY = models.BooleanField()                # HERE WE DECLARE IF IT IS AT THE MAIN INVENTORY
    bibliography = models.TextField(null=True)
    description = models.TextField(null=True)


    def __str__(self):
        return f"{self.name} {self.component_type} {self.component_subtype}"
    

class Inventory(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventories"
    )
    name = models.CharField(max_length=60)
    project_name = models.CharField(max_length=60)
    components = models.ManyToManyField(Component,related_name="inventories",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}"
    

class Factor(models.Model):
    country = models.CharField(25)
    fuel    = models.CharField(25)
    co2_factor = models.FloatField() 
    primary_energy_factor = models.FloatField()
    class Meta:
        # Define a composite primary key from field1 and field2
        constraints = [
            models.UniqueConstraint(fields=['country', 'fuel'], name='composite_pk')
        ]


class Wall_Insulation_Materials(models.Model):
    wall_or_insulation = models.CharField(50) # takes only values (wall,insulation)
    component_element = models.CharField(50)
    conductivity = models.FloatField()
    capacity = models.FloatField()
    density  = models.FloatField()

    



