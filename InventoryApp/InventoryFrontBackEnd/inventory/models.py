from django.db import models
from django.conf import settings
import json
#from inventory.api.serializers import SimaPro_runsSerializer

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
    component_type = models.CharField(max_length=250,db_column='type')  ##
    component_subtype = models.CharField(max_length=250,db_column='subtype',null=True,blank=True) ##
    capex_per_ugs =  models.FloatField(db_column='capex/u.g.s.',null=True,blank=True) 
    opex_per_capex = models.FloatField(db_column='opex_per_capex',null=True,blank=True) 
    embodied_co2_per_ugs = models.FloatField(db_column='embodied_co2/u.g.s.',null=True,blank=True) 
    embodied_pe_per_ugs = models.FloatField(db_column='embodied_pe/u.g.s.',null=True,blank=True) 
    lifetime = models.FloatField()  ## 
    pref_cost = models.FloatField(db_column='Pref_cost',null=True,blank=True) 
    pref_env = models.FloatField(db_column='Pref_env',null=True,blank=True) 
    scale_cost = models.FloatField(null=True,blank=True) 
    scale_env = models.FloatField(null=True,blank=True) 
    major_upgrade_point = models.FloatField(null=True,blank=True) 
    major_upgrade_share = models.FloatField(null=True,blank=True) 
    annual_performance_degradation = models.FloatField()  ## 
    replace_or_die = models.CharField(max_length=250) ##
    SHEET_TYPE = models.CharField(max_length=250)  ##         # HERE WE DECLERE THE SHEET_TYPE  e.g El.Generators,Insulation etc
    IS_MAIN_INVENTORY = models.BooleanField()                 # HERE WE DECLARE IF IT IS AT THE MAIN INVENTORY
    bibliography = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    thermal_properties = models.JSONField(null=True) ##
    IS_B_COMPONENT = models.BooleanField() ##
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


class LoggingComponent(models.Model):
    message = models.JSONField()
    fk = models.ForeignKey(Component,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class RegressionValues(models.Model):
    rating = models.FloatField()
    embodied_primary_energy = models.FloatField()
    embodied_co2 = models.FloatField()
    functional_unit = models.TextField()
    ## add FK:
    fk = models.ForeignKey(Component,on_delete=models.CASCADE)
    def __str__(self):
        return f"co2:{self.embodied_co2} pe:{self.embodied_primary_energy} fu:{self.functional_unit} rating:{self.rating}"

class SimaPro_runs(models.Model):
    name = models.TextField()
    component_type = models.CharField(max_length=100,db_column='type',null=True,blank=True)
    component_subtype = models.CharField(max_length=100,db_column='subtype',null=True,blank=True)
    #basics:
    fu_quantity = models.FloatField()
    fu_measurement_unit = models.TextField()
    stage_A_gwp_kgco2eq = models.FloatField()
    stage_A_embodied_pe_gj = models.FloatField()
    eol_gwp_pc = models.FloatField()
    eol_embodied_pe_pc = models.FloatField()
    #extra:
    stage_A_LCA_version = models.TextField(null=True,blank=True)
    stage_A_IA_method_GWP = models.TextField(null=True,blank=True)
    stage_A_IA_method_PE = models.TextField(null=True,blank=True)
    stage_A_comments = models.TextField(null=True,blank=True)
    waste_treatment = models.TextField(null=True,blank=True)
    stage_C_LCA_version = models.TextField(null=True,blank=True)
    stage_C_IA_method_GWP = models.TextField(null=True,blank=True)
    stage_C_IA_method_PE = models.TextField(null=True,blank=True)
    stage_C_comments = models.TextField(null=True,blank=True)
    general_comments = models.TextField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True,blank=True)
    Stage_A_LCA_DB = models.TextField(null=True,blank=True)
    Stage_C_LCA_DB = models.TextField(null=True,blank=True)
    #########################################################################
    # the 2 bellow fields must be the same as (parent component - FK), 
    # at component Table:
    ##########################################################################
    SHEET_TYPE = models.CharField(max_length=100,null=True,blank=True) 
    IS_MAIN_INVENTORY = models.BooleanField(null=True,blank=True)
    ##############################
    ##Add Foreign key restriciton:
    ##############################
    vcomponent_id = models.ForeignKey(Component,on_delete=models.CASCADE,related_name='simapro_runs',null=True)   
    # dunders:
    def _str_(self):
        return f"{self.name} {self.fu_quantity}"
    
#######
# In this class every deleted component with its corresponding
# simapro runs is loaded at this table in order 
# to retrieve it, every time is needed

#['inventories', 'loggingcomponent', 'regressionvalues', 'simapro_runs', 'deletedcomponent', 'id', 'name', 'component_type',
#  'component_subtype', 'capex_per_ugs', 'opex_per_capex', 'embodied_co2_per_ugs', 'embodied_pe_per_ugs', 'lifetime', 'pref_cost', 
# 'pref_env', 'scale_cost', 'scale_env', 'major_upgrade_point', 'major_upgrade_share', 'annual_performance_degradation', 'replace_or_die',
#  'SHEET_TYPE', 'IS_MAIN_INVENTORY', 'bibliography', 'description', 'thermal_properties', 'IS_B_COMPONENT', 'eol_pe_cost', 'eol_co2_cost', 
# 'simapro_version', 'ia_method_ghg', 'ia_method_pe', 'lca_db', 'functional_unit']
#######

class DeletedComponent(models.Model):
    # add simapro runs field (new field):
    simapro_runs_records =  models.JSONField(null=True,blank=True)
    # add the other components:
    name = models.CharField(max_length=250,unique=True)
    component_type = models.CharField(max_length=250,db_column='type')  ##
    component_subtype = models.CharField(max_length=250,db_column='subtype',null=True,blank=True) ##
    capex_per_ugs =  models.FloatField(db_column='capex/u.g.s.',null=True,blank=True) 
    opex_per_capex = models.FloatField(db_column='opex_per_capex',null=True,blank=True) 
    embodied_co2_per_ugs = models.FloatField(db_column='embodied_co2/u.g.s.',null=True,blank=True) 
    embodied_pe_per_ugs = models.FloatField(db_column='embodied_pe/u.g.s.',null=True,blank=True) 
    lifetime = models.FloatField()  ## 
    pref_cost = models.FloatField(db_column='Pref_cost',null=True,blank=True) 
    pref_env = models.FloatField(db_column='Pref_env',null=True,blank=True) 
    scale_cost = models.FloatField(null=True,blank=True) 
    scale_env = models.FloatField(null=True,blank=True) 
    major_upgrade_point = models.FloatField(null=True,blank=True) 
    major_upgrade_share = models.FloatField(null=True,blank=True) 
    annual_performance_degradation = models.FloatField()   
    replace_or_die = models.CharField(max_length=250) 
    SHEET_TYPE = models.CharField(null=True,max_length=250)          
    IS_MAIN_INVENTORY = models.BooleanField(null=True)                 
    bibliography = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    thermal_properties = models.JSONField(null=True) 
    IS_B_COMPONENT = models.BooleanField(null=True) 
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

    def __init__(self,*args,**kwargs):
        # call base constructor:
        super().__init__(*args)
        if 'base_component' not in kwargs:
            return
        else:
            component_to_delete = Component.objects.get(pk=kwargs['base_component'].id)
            # continue you will create 
            # a deleted object because from signals
            # toy take create ops key:
            # make initializations:
            fields = [field.name for field in component_to_delete._meta.get_fields()]
            for field in fields:
                if field not in {'inventories', 'loggingcomponent', 'regressionvalues', 'simapro_runs', 'id'}:
                    setattr(self,field,getattr(component_to_delete,field))

            # handle simapro runs:
            related_simapro_runs_quey_set = component_to_delete.simapro_runs.all()
            SimaPro_runsSerializer = self.get_serializer()
            ser = SimaPro_runsSerializer(related_simapro_runs_quey_set,many=True)
            self.simapro_runs_records = ser.data
            #self.simapro_runs_record = json.dumps(list(component_to_delete.simapro_runs.all().values()))
            # commit to DB:
            self.save()

    #def __str__(self):
    #    return f" deleted -> {self.name} {self.component_type} {self.component_subtype}"

    def get_serializer(self):
        from inventory.api.serializers import SimaPro_runsSerializer
        return SimaPro_runsSerializer
    



    




