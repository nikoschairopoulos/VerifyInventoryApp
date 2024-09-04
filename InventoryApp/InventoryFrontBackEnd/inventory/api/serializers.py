from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers
from inventory.models import Inventory,Component,Factor,CarbonIntensityData,FactorElectricityYear
from django.core.exceptions import ObjectDoesNotExist
from inventory.utils import send_email 



class ComponentSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError({"lifetime must be greater than zero"})
        if data['capex_per_ugs']<0:
            raise serializers.ValidationError("capex/ugs must >=0")
        
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
    

    
