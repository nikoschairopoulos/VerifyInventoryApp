from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers
from inventory.models import Inventory,Component,Factor
from django.core.exceptions import ObjectDoesNotExist
from inventory.utils import send_email 



class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Component
        fields='__all__'
    #    extra_kwargs = {'id': {'write_only': False}}
    def create(self, validated_data):
        return super().create(validated_data)
    def update(self, instance, validated_data):
        obj =  super().update(instance, validated_data)
        return obj

class InventorySerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True,read_only=True)
    components_collection = serializers.ListField(write_only=True)
    author = serializers.StringRelatedField(read_only=True)
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

class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Factor
        fields='__all__'
    def create(self, validated_data):
        return super().create(validated_data)
    def update(self, instance, validated_data):
        obj =  super().update(instance, validated_data)
        return obj


    
