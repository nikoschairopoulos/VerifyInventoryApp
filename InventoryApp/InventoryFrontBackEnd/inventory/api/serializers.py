from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers
from inventory.models import (Inventory,
                              Component,
                              Factor,
                              CarbonIntensityData,
                              FactorElectricityYear,
                              LoggingComponent,
                              RegressionValues,
                              SimaPro_runs)
from django.core.exceptions import ObjectDoesNotExist
from inventory.utils import send_email 
from rest_framework.exceptions import NotFound 
from copy import deepcopy
from django.db import transaction


##############################
# SimaPro_runs Serializer
##############################
class SimaPro_runsSerializer(serializers.ModelSerializer):
    #component_lci_id = serializers.IntegerField(write_only=True)
    FK_lci_id = serializers.IntegerField(source='vcomponent_id.id', read_only=True)
    id = serializers.IntegerField()
    #related_component_name = serializers.CharField(source='fk.name',read_only=True)
    class Meta:
        model = SimaPro_runs
        #exclude = ['vcomponent_id']
        fields = '__all__'
    def create(self, validated_data):
        #component_lci_id = validated_data.pop('component_lci_id',None)
        vcomponent_instance =  validated_data.pop('vcomponent_id',None)
        if not vcomponent_instance:
            raise NotFound(f'There is no related virtaul component with the given LCI id')
        #pass the related instance:
        new_regression_instance = SimaPro_runs.objects.create(vcomponent_id = vcomponent_instance, **validated_data)
        return new_regression_instance
    
    def validate_component_type(self, value):
        if value == "":  # If the component_subtype is an empty string
            return None  # Return None to store it as NULL in the database
        return value

    def validate_component_subtype(self, value):
        if value == "":  # If the component_subtype is an empty string
            return None  # Return None to store it as NULL in the database
        return value   
    
    def validate(self,data):
        if data['fu_quantity'] < 0 :
            raise serializers.ValidationError({"rating (fu_quantity)": "must be greater than zero"})
        if data['eol_gwp_pc'] < 0 or data['eol_gwp_pc']>100 :
            raise serializers.ValidationError({"eol co2":"eol gwp must be in interval [0,100]"})
        if data['eol_embodied_pe_pc'] < 0 or data['eol_embodied_pe_pc']>100 :
            raise serializers.ValidationError({"eol pe":"eol pe must be in interval [0,100]"})
        return data

class ComponentSerializer(serializers.ModelSerializer):
    simapro_runs = SimaPro_runsSerializer(many=True)
    #simapro_runs = SimaPro_runsSerializer(many=True, required=False)
    class Meta:
        model=Component
        fields='__all__'
    def create(self, validated_data):
        simapro_runs = validated_data.pop('simapro_runs',None)
        try:
            with transaction.atomic():  # Start a transaction
                created_component = Component.objects.create(**validated_data)
                #if you have simapro runs iterate over them, to create the components simapro run
                if simapro_runs:
                    for simapro_run in simapro_runs:
                        self.update_simapro_run_json(record=simapro_run,
                                                component_validated_data=deepcopy(validated_data))
                        SimaPro_runs.objects.create(vcomponent_id = created_component,**simapro_run) ##### ADD COMPONENT TYPE SUBTYPE ETC
                return created_component
        except Exception as e:
            print(e)
            raise serializers.ValidationError({'error': str(e)})
    
    def update_simapro_run_json(self,record,component_validated_data): 
        record['component_type'] = component_validated_data["component_type"]
        record['component_subtype'] = component_validated_data["component_subtype"]
        record['IS_MAIN_INVENTORY'] = component_validated_data["IS_MAIN_INVENTORY"]
        record["SHEET_TYPE"] = component_validated_data["SHEET_TYPE"]
        #test:
        #record['IS_B_COMPONENT'] = component_validated_data["IS_B_COMPONENT"]


    #UPDATES EVERY SINGLE SIMAPRO RUN
    #DOES ORM DIRECTLY BECAUSE DATA 
    #ARE VALIDATED:
    def update_simapro_runs(self, simapro_run_data):
        instance = SimaPro_runs.objects.get(pk=simapro_run_data['id'])
        simapro_run_data.pop('id')
        # Update fields directly
        for attr, value in simapro_run_data.items():
            setattr(instance, attr, value)
        instance.save()
    
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                #get simapro runs:
                simapro_runs_list = validated_data.pop('simapro_runs',None)
                #iterate over them and update their values:
                for record in simapro_runs_list:
                    self.update_simapro_runs(record)
                obj =  super().update(instance, validated_data)
                return obj
        except Exception as e:
            print(e)
            raise serializers.ValidationError({'error': str(e)})

    
    
    def validate(self, data):
        if data['lifetime'] < 0 :
            raise serializers.ValidationError({"lifetime": "must be greater than zero"})
        if data['annual_performance_degradation']<0 or data['annual_performance_degradation']>1:
            raise serializers.ValidationError({"degradation": "takes values 0 to 1"})
        return data
    
    
    def validate_component_subtype(self, value):
        if value == "":  # If the component_subtype is an empty string
            return None  # Return None to store it as NULL in the database
        return value


    def to_representation(self, instance):
        component_view = super().to_representation(instance)
        to_show = {
            "name", 
            "component_type", 
            "component_subtype", 
            "annual_performance_degradation",
            "replace_or_die", 
            "SHEET_TYPE", 
            "IS_MAIN_INVENTORY",
            "lifetime",
            "description",
            "thermal_properties",
            "id",
            "IS_B_COMPONENT",
            "simapro_runs"
        }
        component_to_show = {k:v for k,v in component_view.items() 
                             if k in to_show}
        
        return component_to_show





class InventorySerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True,read_only=True)
    components_collection = serializers.ListField(write_only=True)
    author = serializers.StringRelatedField(read_only=True)
    email  =  serializers.EmailField(source='author.email', read_only=True)
    class Meta:
        model=Inventory
        fields = '__all__'

    def create(self, validated_data):
        components_list = validated_data.pop('components_collection')
        try:
            for comp in components_list:
                i = Component.objects.get(pk=comp)
        except ObjectDoesNotExist:
            raise Exception(f" Error: Object with pk = {comp} does not exist.") # To do, mporeis na valeis kai lookups
        
        inventory_obj = Inventory.objects.create(**validated_data)
        inventory_obj.components.set(components_list) # use field setter , django dont lets writing the many to many as KWARGS
                                                      # if is empty list , creates an inventory with no components
        return inventory_obj
        
    def update(self, instance, validated_data):
        #TO DO : USE ORM TO TO CHECKS
        instance.name = validated_data.get('name',instance.name)
        instance.project_name = validated_data.get('project_name',instance.project_name)
        try: 
            instance.components.set(validated_data['components_collection'])
        except ObjectDoesNotExist:
            raise Exception(f"Integrity Constraint:You try to update the Components of the Inventory with non existed component for tha Primary Key")
        instance.save()
        return instance
    '''
    def to_representation(self, instance):
        components_queryset = instance.components.all()                 # like that you take all the associated components
        components = ComponentSerializer(components_queryset,many=True) # Serialize them
        # to make changes --> dont show all the information
        #transform_data() --> components_data
        to_return = { "id":instance.id,
                      "name":instance.name,
                      "project_name":instance.project_name,
                      "components":components.data}
        return to_return
    '''

########
    #learning tip:
    #every serializer has the 3 bellow methods: create,update,validate
########
class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Factor
        fields='__all__'
    def create(self, validated_data):
        return super().create(validated_data)
    def update(self, instance, validated_data):
        test=1
        obj =  super().update(instance, validated_data)
        return obj
    
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['primary_energy_factor'] < 1:
            raise serializers.ValidationError({"primary energy factor cannot be < 1 "})
        

        if data['co2_factor']<0:
            raise serializers.ValidationError({"co2 factor must >= 0 "})
        
        return data

class CarbonIntensityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonIntensityData
        fields = '__all__'

class CarbonIntensityDataSerializerYear(serializers.ModelSerializer):
    class Meta:
        model = FactorElectricityYear
        fields = '__all__'
    
  
class LogsSerializer(serializers.ModelSerializer):
    #you must add all custom fields ==> at fields:
    fk = ComponentSerializer(read_only=True)
    class Meta:
        model = LoggingComponent
        fields =['message','fk','created_at']


##############################
# Regression Values Serializer
##############################
class RegressionValuesSerializer(serializers.ModelSerializer):
    component_lci_id = serializers.IntegerField(write_only=True)
    related_lci_id = serializers.IntegerField(source='fk.id', read_only=True)
    related_component_name = serializers.CharField(source='fk.name',read_only=True)
    class Meta:
        model = RegressionValues
        fields = ["component_lci_id",
                  "embodied_primary_energy",
                  "embodied_co2",
                  "functional_unit",
                  "rating",
                  "related_lci_id",
                  "related_component_name"
                  ]
    
    def create(self, validated_data):
        component_lci_id = validated_data.pop('component_lci_id')
        try:
            related_component_instance = Component.objects.get(pk=component_lci_id)
        except ObjectDoesNotExist:
            raise NotFound(f'There is no component with lci id = {component_lci_id}')
        new_regression_instance = RegressionValues.objects.create(fk = related_component_instance, **validated_data)
        return new_regression_instance
    
    def validate_component_type(self, value):
        if value == "":  # If the component_subtype is an empty string
            return None  # Return None to store it as NULL in the database
        return value

    def validate_component_subtype(self, value):
        if value == "":  # If the component_subtype is an empty string
            return None  # Return None to store it as NULL in the database
        return value

##############################
# SimaPro_runs Serializer
##############################
'''
class SimaPro_runsSerializer(serializers.ModelSerializer):
    #component_lci_id = serializers.IntegerField(write_only=True)
    FK_lci_id = serializers.IntegerField(source='vcomponent_id.id', read_only=True)
    #related_component_name = serializers.CharField(source='fk.name',read_only=True)
    class Meta:
        model = SimaPro_runs
        #exclude = ['vcomponent_id']
        fields = '__all__'
    def create(self, validated_data):
        #component_lci_id = validated_data.pop('component_lci_id',None)
        vcomponent_instance =  validated_data.pop('vcomponent_id',None)
        if not vcomponent_instance:
            raise NotFound(f'There is no related virtaul component with the given LCI id')
        #pass the related instance:
        new_regression_instance = SimaPro_runs.objects.create(vcomponent_id = vcomponent_instance, **validated_data)
        return new_regression_instance
'''

###############################
#To implement nested Attributes 
#between component and simaproRuns  (#TODO)
###############################
        

