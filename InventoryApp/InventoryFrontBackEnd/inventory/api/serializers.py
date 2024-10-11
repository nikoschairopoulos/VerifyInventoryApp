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



class ComponentSerializer(serializers.ModelSerializer):
    #simapro_runs = SimaPro_runs(many=True,write_only=True)
    class Meta:
        model=Component
        fields='__all__'
    def create(self, validated_data):
        return super().create(validated_data)
    def update(self, instance, validated_data):
        obj =  super().update(instance, validated_data)
        return obj
    def validate(self, data):
        if data['lifetime'] < 0 :
            raise serializers.ValidationError({"lifetime": "must be greater than zero"})
        if data['annual_performance_degradation']<0:
            raise serializers.ValidationError({"degradation": "must be greater than or equal to zero"})
        
        return data




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

##############################
# SimaPro_runs Serializer
##############################
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


###############################
#To implement nested Attributes 
#between component and simaproRuns  (#TODO)
###############################
        

