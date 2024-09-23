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
    name = models.CharField(max_length=250,unique=True)
    # here add the attributes as at excell inventory:
    #installed_ugs =  models.FloatField() 
    component_type = models.CharField(max_length=250,db_column='type')
    component_subtype = models.CharField(max_length=250,db_column='subtype',null=True)
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
    replace_or_die = models.CharField(max_length=250)
    SHEET_TYPE = models.CharField(max_length=250)             # HERE WE DECLERE THE SHEET_TYPE  e.g El.Generators,Insulation etc
    IS_MAIN_INVENTORY = models.BooleanField()                 # HERE WE DECLARE IF IT IS AT THE MAIN INVENTORY
    bibliography = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    thermal_properties = models.JSONField(null=True, blank=True)
    IS_B_COMPONENT = models.BooleanField()
    eol_pe_cost = models.FloatField(null=True,blank=True)
    eol_co2_cost = models.FloatField(null=True,blank=True)
    ######## (new attributes to confront with new Database Fields:)
    simapro_version = models.CharField(null=True,blank=True)
    ia_method_ghg   = models.CharField(null=True,blank=True)
    ia_method_pe    = models.CharField(null=True,blank=True)
    lca_db          = models.CharField(null=True,blank=True)
    functional_unit = models.CharField(null=True,blank=True)



    class Meta:
        app_label = 'inventory'


    def __str__(self):
        return f"{self.name} {self.component_type} {self.component_subtype}"
    

class Inventory(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventories"
    )
    name = models.CharField(max_length=250)
    project_name = models.CharField(max_length=250)
    components = models.ManyToManyField(Component,related_name="inventories",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"{self.name}"
    

class Factor(models.Model):
    country = models.CharField(250)
    fuel    = models.CharField(250)
    co2_factor = models.FloatField(null=True) 
    primary_energy_factor = models.FloatField(null=True)
    ## new fields:
    #year = models.IntegerField(null=True)
    source = models.TextField(blank=True,null=True)
    comments = models.TextField(blank=True,null=True)
    class Meta:
        # Define a composite primary key from field1 and field2
        constraints = [models.UniqueConstraint(fields=['country', 'fuel'], name='composite_pk')]
        app_label = 'inventory'
    def __str__(self):
        return f"{self.country} {self.fuel} {self.co2_factor} {self.primary_energy_factor}  {self.source} {self.comments}"


class Wall_Materials(models.Model):
    id = models.BigAutoField(primary_key=True, default=0)
    name = models.CharField(250)
    conductivity = models.FloatField()
    capacity = models.FloatField()
    density  = models.FloatField()

    class Meta:
        app_label = 'inventory'


#########
# in the bellow Model we add the hourly 
# measurements for electricity:
#########
    
'''
comment --> is the mapping from excell to databse: 
Datetime (UTC)                        --> datetime	
Country	   	                          --> country
Zone Name                             --> zone_name
Zone Id	                              --> zone_id
Carbon Intensity gCO₂eq/kWh (direct)  --> carbon_intensity_gco2_eq_kwh_direct	
Carbon Intensity gCO₂eq/kWh (LCA)	  --> carbon_intensity_gco2_eq_kwh_lca	
Low Carbon Percentage	              --> low_carbon_percentage
Renewable Percentage	              --> renewable_percentage
Data Source	                          --> data_source
Data Estimated	                      --> data_estimated
Data Estimation Method                -->data_estimation_method
'''

class CarbonIntensityData(models.Model):
    datetime = models.DateTimeField()
    country  = models.CharField(max_length=255) 
    zone_name = models.CharField(max_length=255)
    zone_id = models.CharField(max_length=100)  
    carbon_intensity_gco2_eq_kwh_direct = models.FloatField()
    carbon_intensity_gco2_eq_kwh_lca = models.FloatField()
    low_carbon_percentage = models.FloatField()
    renewable_percentage = models.FloatField()
    data_source = models.CharField(max_length=255)
    data_estimated = models.BooleanField(blank=True,null=True) 
    data_estimation_method = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f"{self.country_zone_name} - {self.datetime}"

    class Meta:
        #verbose_name_plural = "Carbon Intensity Data"
        
        indexes = [
            models.Index(fields=['country', 'datetime']),
        ]

        unique_together = [['country', 'datetime']]



class FactorElectricityYear(models.Model):
    country = models.CharField(250)
    year = models.IntegerField()
    measurement_co2 = models.FloatField() 
    source = models.TextField(blank=True,null=True)
    comments = models.TextField(blank=True,null=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['country', 'year'], name='composite_pk_2')]
        app_label = 'inventory'
    def __str__(self):
        return f"{self.country} {self.year} {self.measurement_co2}"
