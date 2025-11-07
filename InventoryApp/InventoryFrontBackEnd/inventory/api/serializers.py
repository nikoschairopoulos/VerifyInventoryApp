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
                              SimaPro_runs,
                              DeletedComponent, ETS)
from django.core.exceptions import ObjectDoesNotExist
from inventory.utils import send_email 
from rest_framework.exceptions import NotFound 
from copy import deepcopy
from django.db import transaction
from users.models import CustomUser


##############################
# SimaPro_runs Serializer
##############################
class SimaPro_runsSerializer(serializers.ModelSerializer):
    #component_lci_id = serializers.IntegerField(write_only=True)
    
    #is the Vcomponent Id (only to return) (maybe not needed)
    FK_lci_id = serializers.IntegerField(source='vcomponent_id.id', read_only=True)
    #is the pk of this simapro run record
    id = serializers.IntegerField(required=False)
    #related_component_name = serializers.CharField(source='fk.name',read_only=True)
    class Meta:
        model = SimaPro_runs
        #exclude = ['vcomponent_id']
        fields = '__all__'
    def create(self, validated_data):
        #Framework by it self mapping the id provided by json and
        #an at validated data gives the vcomponent_instance
        vcomponent_instance =  validated_data.pop('vcomponent_id',None)
        if not vcomponent_instance:
            raise NotFound(f'There is no related virtaul component with the given LCI id')
        #pass the related instance:
        new_regression_instance = SimaPro_runs.objects.create(vcomponent_id = vcomponent_instance, **validated_data)
        return new_regression_instance

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    ##############
    # validations:
    ##############

    def validate_component_type(self, value):
        if value == "":  # If the component_subtype is an empty string
            return None  # Return None to store it as NULL in the database
        return value
    
    def validate_stage_A_LCA_version(self,value):
        if value is None:
            raise serializers.ValidationError("stage_A_LCA_version can not be null")
        return value
    
    def validate_stage_C_LCA_version(self,value):
        if value is None:
            raise serializers.ValidationError("stage_C_LCA_version can not be null")
        return value

    def validate_component_subtype(self, value):
        if value == "":  # If the component_subtype is an empty string
            return None  # Return None to store it as NULL in the database
        return value   
    
    
    def validate(self,data):
        ## add extra validation in case component has assumption (0,0) simapro run like District Heating
        ## Then can only have one simapro run -> with fu quantity = 0 and all the numerics other zeros:
        #if 'vcomponent_id' in data:
        #    pass
            #framework does the retieving of the object automatically:
            #so component is an instance
        #    component = data['vcomponent_id']
        #    self.check_default_0_0(data = data,vcomponent = component)
        if data['fu_quantity'] < 0 :
            raise serializers.ValidationError({"message": " rating must be greater than zero"})
        if data['eol_gwp_pc'] < 0 or data['eol_gwp_pc'] > 100 :
            raise serializers.ValidationError({"message":"eol gwp must be in interval [0,100]"})
        if data['eol_embodied_pe_pc'] < 0 or data['eol_embodied_pe_pc'] > 100 :
            raise serializers.ValidationError({"message":"eol pe must be in interval [0,100]"})
        ## add extra logic for data validation:
        if data['fu_quantity'] == 0 and (data['stage_A_gwp_kgco2eq']!=0 or data['stage_A_embodied_pe_gj']!=0):
            raise serializers.ValidationError({"message":"Point of Format (0,N) is not acceptaple"})
        if data['fu_quantity'] != 0 and (data['stage_A_gwp_kgco2eq']==0 or data['stage_A_embodied_pe_gj']==0):
            raise serializers.ValidationError({"message":"Point of Format (N,0) is not acceptaple"})
        #you have pass all validations so return:
        return data

    def allow_zero_numerics_if_you_are_the_only_component(self,data):
        '''
        Here handle what happends if you change 
        the unique simapro run 
        of a component
        '''
        pass


    #This method is added here but is used
    #at component serializer for validations,
    #during creations and updates simultaneously:
    '''
    1. does not allows if you have list of json that are not valid to be created
    3. does not allows if you try to update a list of json that is not valid to updated
    '''
    @staticmethod
    def check_default_0_0(data,vcomponent):
        # take reverse query set:
        simapro_runs = vcomponent.simapro_runs.all()
        
        #if you try to add fu = 0 but vcomponent has and other measurements raise Exception
        #all this is done to prevent violate the assumption for example District Heating Components:
        if data['fu_quantity'] == 0 and simapro_runs.exists():
            raise serializers.ValidationError({'message':f'try to add record with 0 rating having other  rating measurements - CHECK YOUR MEASUREMENTS - lci_id =  {vcomponent.id}'})
        
        #an extra validation in case you try to add an extra simapro run
        #for a component that have already 0 rating
        for instance in simapro_runs:
            if instance.fu_quantity == 0:
                raise serializers.ValidationError({'message':f'has point with FU = 0 - Must have only that simapro run -  CHECK YOUR MEASUREMENTS - lci_id =  {vcomponent.id}'})



class ComponentSerializer(serializers.ModelSerializer):
    simapro_runs = SimaPro_runsSerializer(many=True)
    user_email = serializers.CharField(write_only = True, required = False)
    #simapro_runs = SimaPro_runsSerializer(many=True, required=False)
    class Meta:
        model=Component
        fields='__all__'
    def create(self, validated_data):
        simapro_runs = validated_data.pop('simapro_runs',None)
        user_email = validated_data.pop('user_email',None)
        try:
            with transaction.atomic():  # Start a transaction
                created_component = Component.objects.create(**validated_data)
                #if you have simapro runs iterate over them, to create the components simapro run
                if simapro_runs:
                    self.check_if_lca_version_is_none(simapro_runs=simapro_runs)
                    for simapro_run in simapro_runs:
                        #make an extra validation:
                        #SimaPro_runsSerializer.check_default_0_0(data=simapro_run,vcomponent=created_component)
                        
                        #update json
                        self.inform_simapro_run_json(record=simapro_run,
                                                component_validated_data=deepcopy(validated_data))
                        #create:
                        SimaPro_runs.objects.create(vcomponent_id = created_component,**simapro_run) ##### ADD COMPONENT TYPE SUBTYPE ETC
                #in case you have send user email add it at users inventory:
                self.set_component_at_user_inventory(user_email,created_component)
                #return component:
                return created_component
        except Exception as e:
            print(e)
            raise serializers.ValidationError({'error': str(e)})
    # this method checks if 
    def check_if_lca_version_is_none(self,simapro_runs):
        for run in simapro_runs:
            if run["stage_A_LCA_version"] is None or run["stage_C_LCA_version"] is None:
                raise serializers.ValidationError({'error':'stage_A_LCA_version and "stage_C_LCA_version" must be non null - check your request body'})
    
    def add_custom_component_at_users_inventory(self,email,inventory_id):
        pass
        #users = CustomUser.objects.all()
    
    def inform_simapro_run_json(self,record,component_validated_data): 
        record['component_type'] = component_validated_data["component_type"]
        record['component_subtype'] = component_validated_data["component_subtype"]
        record['IS_MAIN_INVENTORY'] = component_validated_data["IS_MAIN_INVENTORY"]
        record["SHEET_TYPE"] = component_validated_data["SHEET_TYPE"]
        #test:
        #record['IS_B_COMPONENT'] = component_validated_data["IS_B_COMPONENT"]
    
    def set_component_at_user_inventory(self,user_email,component_instance):
        if user_email is not None:
            current_user = CustomUser.objects.get(email=user_email)
            inventories = current_user.inventories.all()
            if len(inventories) > 1:
                raise serializers.ValidationError(f'user: {user_email}, has more than one inventories - something goes wrong')
            if component_instance.IS_MAIN_INVENTORY:
                raise serializers.ValidationError({'message':'you try to add main inventory component at custom inventory'})
            unique_inventory  = inventories[0]
            unique_inventory.components.add(component_instance)
            unique_inventory.save()


    # UPDATES EVERY SINGLE SIMAPRO RUN
    # DOES ORM DIRECTLY BECAUSE DATA 
    # ARE VALIDATED:
    def update_simapro_runs(self, simapro_run_data):
        if 'id' not in simapro_run_data:
            raise serializers.ValidationError({'error': 'ID is required to update simapro_run.'})
        try:
        # Try fetching the existing instance by ID
            instance = SimaPro_runs.objects.get(pk=simapro_run_data['id'])
        except ObjectDoesNotExist:
        # If the ID is not found, raise an error and don't create
            raise serializers.ValidationError(
                {'error': f"SimaPro_run with id {simapro_run_data['id']} does not exist."}
            )
        # dont update id
        simapro_run_data.pop('id')
        # Update fields directly
        for attr, value in simapro_run_data.items():
            setattr(instance, attr, value)
        instance.save()
    
    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                #get simapro runs:
                simapro_runs_list = validated_data.pop('simapro_runs',[])
                #iterate over them and update their values:
                for record in simapro_runs_list:
                    #make extra validation:
                    #SimaPro_runsSerializer.check_default_0_0(data=record,vcomponent=instance)
                    #inform the record with its parent component for the common fields:
                    self.inform_simapro_run_json(record,component_validated_data=deepcopy(validated_data))
                    #update current simapro run instance:
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

class DeletedComponentSerializer(serializers.ModelSerializer):
    # for post request -> dont take into account:
    simapro_runs_records = serializers.JSONField(required=False)
    class Meta:
        model = DeletedComponent
        fields = '__all__'
        

class EtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ETS
        # fields = "__all__"  # We want all the fields of our model
        exclude = ("id",)
