#SOLUTION:https://stackoverflow.com/questions/32590241/standalone-django-orm-default-settings-not-recognized

'''
import django
from django.conf import settings
from inventoryapi import myapp_defaults 

settings.configure(default_settings=myapp_defaults,DEBUG=True)
django.setup()

# Now this script or any imported module can use any part of Django it needs.
'''


import os
import sys
import django
from pathlib import Path
from django.shortcuts import get_object_or_404
from copy import deepcopy
import requests
import json
import pandas as pd

#from folder.subfolder.myfile import tade

if __name__  != "__main__":
    raise RuntimeError("Do not import from this script")

#add path:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryapi.settings')
django.setup()
from inventory.models import (Component, 
                                Factor,
                                CarbonIntensityData,
                                SimaPro_runs)

from users.models import (CustomUser)

from inventory.api.serializers import ComponentSerializer
#import pandas as pd 

#FILES PATH:
CURRENT_DIRECTORY = Path(__file__).parent.absolute()

'''
#print(Component.objects.filter(SHEET_TYPE='El. Storage'))
query = Component.objects.filter(SHEET_TYPE='El. Storage')
ser = ComponentSerializer(query,many=True)
d_batteries = []
for comp in ser.data:
    if 'battery' in comp['component_type']:
        #print(comp)
        #change sheet type for B batteries
        obj_b = get_object_or_404(Component,pk=comp['id'])
        obj_b.SHEET_TYPE = 'B_Batteries'
        obj_b.save()

        d_comp = deepcopy(comp)
        d_comp['SHEET_TYPE'] = 'D_Batteries'
        d_comp['IS_B_COMPONENT'] = False
        d_comp['name']+=' district'
 
        #D components:
        d_batteries.append(d_comp) 
        print(d_batteries)

d_batteries_serializer = ComponentSerializer(data=d_batteries, many=True)
if d_batteries_serializer.is_valid():
    d_batteries_serializer.save()
else:
    print('no valid data')
'''

'''
query = Component.objects.all()
ser = ComponentSerializer(query,many=True)
deleted_comp = []
# find the deleted and add the into the DB
for comp in ser.data:
    if  ('thermochromic' in comp['name']  or  'facade' in comp['name'] and 'zappa' not in comp['name'] )
        print(comp['name'])
        deleted_comp.append(comp)

for comp in deleted_comp:
    print(comp)

        try:
            response = requests.post(
                    f"http://192.168.101.31:8003/api/component",
                    json=comp,
                    headers={"Authorization": "Token 503ee22e7fcb2cd811c40143aa16392cf4145818"},
                )
            print(response.text)
        except:
            print(response.text)

try:
    with open('deleted_components.json', 'w') as file:
        print('i write components')
        json.dump(deleted_comp, file, indent=4)
except Exception as e:
    print(e)
'''

'''
#READ THE OBJECTS FROM .json
with open('deleted_components.json', 'r') as file:
    deleted_comp = json.load(file)
    print(deleted_comp)




for comp in deleted_comp:
    try:
        # Ensure 'id' is accessed correctly
        obj_comp = Component(**comp)
        obj_comp.save()
        print(f"Created component with ID {obj_comp.id}")

    except Exception as e:
        print(f"Error creating component with ID {comp['id']}: {e}")
'''

'''NOT FOR PK CHANGES DUE TO SERIALIZER DRF DEFAULT BEHAVIOUR'''
'''
#use the old (id=3) to restore:
boiler_biomass_data = {'id': 3, 'name': 'boiler biomass (default)', 
              'component_type': 'boiler', 'component_subtype': 'biomass',
              'capex_per_ugs': 54.34782608695652, 'opex_per_capex': 0.02,
              'embodied_co2_per_ugs': 75.77777777777777, 'embodied_pe_per_ugs': 0.9555555555555555,
              'lifetime': 20.0, 'pref_cost': 46.0, 'pref_env': 9.0, 'scale_cost': 0.0, 'scale_env': -0.083, 'major_upgrade_point': 999.0,
              'major_upgrade_share': 0.0, 'annual_performance_degradation': 0.005, 'replace_or_die': 'replace', 'SHEET_TYPE': 'Thermal Sources',
              'IS_MAIN_INVENTORY': True, 'bibliography': None, 'description': None, 'thermal_properties': None, 'IS_B_COMPONENT': True}

serializer = ComponentSerializer(data = boiler_biomass_data)
if serializer.is_valid():
    serializer.save()
else:
    print(serializer.error_messages)
'''

'''
deleted_comp = []
boiler_biomass_data = {'id': 3, 'name': 'boiler biomass (default)', 
              'component_type': 'boiler', 'component_subtype': 'biomass',
              'capex_per_ugs': 54.34782608695652, 'opex_per_capex': 0.02,
              'embodied_co2_per_ugs': 75.77777777777777, 'embodied_pe_per_ugs': 0.9555555555555555,
              'lifetime': 20.0, 'pref_cost': 46.0, 'pref_env': 9.0, 'scale_cost': 0.0, 'scale_env': -0.083, 'major_upgrade_point': 999.0,
              'major_upgrade_share': 0.0, 'annual_performance_degradation': 0.005, 'replace_or_die': 'replace', 'SHEET_TYPE': 'Thermal Sources',
              'IS_MAIN_INVENTORY': True, 'bibliography': None, 'description': None, 'thermal_properties': None, 'IS_B_COMPONENT': True}
deleted_comp.append(boiler_biomass_data)
for comp in deleted_comp:
    try:
        # Ensure 'id' is accessed correctly
        obj_comp = Component(**comp)
        obj_comp.save()
        print(f"Created component with ID {obj_comp.id}")

    except Exception as e:
        print(f"Error creating component with ID {comp['id']}: {e}")
'''
'''
    def change_component_name(component):
        #make it list
        name_temp = component.name.split('_')
    
        #remove _
        name_temp = [elem for elem in name_temp if elem!='_']
        
        name_uptaded = " ".join(name_temp).title()
        

        component.name = name_uptaded
        component.save()


    components = Component.objects.all()
    for comp in components:
        change_component_name(component = comp)
'''


#print(factors)
#iterate on every country and take a set of countries:

'''
factors = Factor.objects.all()
s1 = set()
for f in factors:
    s1.add(f.country)
print(s1)

#create gasoline factors:
for country in s1:
    obj1 = Factor(country=country,
                  fuel='gasoline',
                  co2_factor=0.27,
                  primary_energy_factor=1.2)
    obj1.save()
'''
'''
#gasoline_objects = Factor.objects.values('country')
gasoline_objects = Factor.objects.values('country').distinct()
print(type(gasoline_objects))

for item in gasoline_objects:
    print(item)
    print(type(item))
    
#for factor in factors:
    #factor.comments = 'initial year is considered 2018 but it is not sure. Year 2018 is used as a reference'
    #factor.year = 2018
#    factor.source = 'source is not provided'
#    factor.save()
'''

'''
# make eol equal to zero:
for element in Component.objects.all():
    element.eol_co2_cost = 0
    element.eol_pe_cost  = 0
    element.save()

# add gasoline to all countries:
factors = Factor.objects.all()
s1 = set()
for f in factors:
    s1.add(f.country)
print(s1)
for country in s1:
    obj1 = Factor(country=country,
                  fuel='gasoline',
                  co2_factor=0.314,
                  primary_energy_factor=1.1)
    obj1.save()
'''
############################################################
############################################################

'''
def create_format_for_simapro_runs(components_list):
    simapro_runs = []
    for single_component_dict in components_list:
        simapro_run_record = get_format_dict()
        #update fields:
        simapro_run_record['name'] = single_component_dict['name']
        simapro_run_record["stage_A_gwp_kgco2eq"] = single_component_dict['embodied_co2_per_ugs']
        simapro_run_record["stage_A_embodied_pe_gj"] = single_component_dict['embodied_pe_per_ugs']
        simapro_run_record["vcomponent_id"] = single_component_dict['id']
        simapro_run_record['component_type'] = single_component_dict['component_type']
        simapro_run_record['component_subtype'] = single_component_dict['component_subtype']
        simapro_run_record['SHEET_TYPE'] = single_component_dict['SHEET_TYPE']
        simapro_run_record['IS_MAIN_INVENTORY'] = single_component_dict['IS_MAIN_INVENTORY']
        #for debug reasons, we keep the label:
        simapro_run_record['scale_env'] = single_component_dict['scale_env']
        simapro_runs.append(simapro_run_record)
    return simapro_runs

def get_format_dict():
    return {
    "name": None,
    "component_type": None,
    "component_subtype": None,
    "fu_quantity": None,
    "fu_measurement_unit": None,
    "stage_A_gwp_kgco2eq": None,
    "vcomponent_id": None,
    "stage_A_embodied_pe_gj": None,
    "stage_A_LCA_version": None,
    "stage_A_IA_method_GWP": None,
    "stage_A_IA_method_PE": None,
    "stage_A_comments": None,
    "eol_gwp_pc": None,
    "eol_embodied_pe_pc": None,
    "waste_treatment": None,
    "stage_C_LCA_version": None,
    "stage_C_IA_method_GWP": None,
    "stage_C_IA_method_PE": None,
    "stage_C_comments": None,
    "general_comments": None,
    "IS_MAIN_INVENTORY": None,
    "SHEET_TYPE": None,
    "stage_A_LCA_DB":None,
    "stage_C_LCA_DB":None
}

def create_dataframe(scale_env_zero_or_one):
    custom_components_scale_env = Component.objects.filter(IS_MAIN_INVENTORY=False,scale_env=scale_env_zero_or_one)
    serializer = ComponentSerializer(custom_components_scale_env,many=True)
    components_dict = serializer.data
    simapro_runs_transformed = create_format_for_simapro_runs(components_dict)
    df = pd.DataFrame(simapro_runs_transformed)
    #df.to_csv(f'simapro_run_scale_env_equal_{scale_env_zero_or_one}_custom_components.csv')
    return df 

#create 2 excells
df_simapro_runs_0 = create_dataframe(scale_env_zero_or_one=0)
df_simapro_runs_1 = create_dataframe(scale_env_zero_or_one=1)
#breakpoint()
df_all = pd.concat([df_simapro_runs_0,df_simapro_runs_1],axis=0,ignore_index=True)
#breakpoint()
df_all.to_csv('custom_components_from_component_to_simapro_runs.csv')
'''




## this method will much the FK -> sheet type , type , subtype , IS_MAIN_INVENTORY 
def update_some_fields_simapro_run():
    simapro_runs_queryset = SimaPro_runs.objects.all()
    for instance in simapro_runs_queryset:
        #take visual component fk:
        vc = Component.objects.filter(pk = instance.vcomponent_id.id)
        #update components:
        instance.SHEET_TYPE = vc[0].SHEET_TYPE
        instance.IS_MAIN_INVENTORY = vc[0].IS_MAIN_INVENTORY
        instance.component_type = vc[0].component_type
        instance.component_subtype = vc[0].component_subtype
        instance.save()

#pdate_some_fields_simapro_run()

'''
def update_some_fields_simapro_run():
    simapro_runs_queryset = SimaPro_runs.objects.filter(pk=417)
    for instance in simapro_runs_queryset:
        #take visual component fk:
        vc = Component.objects.filter(pk=3)
        breakpoint()
        #update components:
        instance.SHEET_TYPE = vc[0].SHEET_TYPE
        instance.IS_MAIN_INVENTORY = vc[0].IS_MAIN_INVENTORY
        instance.component_type = vc[0].component_type
        instance.component_subtype = vc[0].component_subtype
        #save instance:
        instance.save()
update_some_fields_simapro_run()
'''

#simapro_run_set = SimaPro_runs.objects.values_list('vcomponent_id',flat=True)
#breakpoint()
#components = Component.objects.filter(id__in = simapro_run_set)
#breakpoint()

#users = CustomUser.objects.all()
#for user in CustomUser:
#breakpoint()
#inventories =  users[2].inventories.all()
#breakpoint()
'''
all_components = []
#take current user:
current_user = CustomUser.objects.get(email='rehouse@verify.gr')
#take all its inventories:
inventories = current_user.inventories.all()
#add all custom components of the inventories:
for inventory in inventories:
    all_components.extend(inventory.components.all()) 
print(len(all_components))
default_components = Component.objects.filter(IS_MAIN_INVENTORY=True)
#create overall component List:
all_components.extend(default_components)
print(len(all_components))
component_serializer = ComponentSerializer(all_components,many=True)
'''
'''
#arguments = {
            'is_superuser':False,
            'username':'test_user 2',
            'first_name':'test_name',
            'last_name':'test_lastname',
            'email':'test_email',
            'is_staff':False,
            'is_active':True
        }
'''
from inventory.models import Inventory
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

def flatten(xss):
    return [x for xs in xss for x in xs]

users = CustomUser.objects.all()
components = []
for user in users:
    # If the user has multiple inventories
    if len(user.inventories.all()) > 1:
        # collect all components
        unify_inventory_components = [inventory.components.all() for inventory in user.inventories.all()]
        unify_inventory_components_flat = flatten(unify_inventory_components)
        
        # delete
        for inventory in user.inventories.all():
            inventory.delete()
        
        # crete the new inventory
        new_inventory = Inventory(
            author=user,
            name='custom_inventory',
            project_name=f'{user.username}'
        )
        new_inventory.save()
        
        # Add all unique components to the new inventory
        new_inventory.components.add(*unify_inventory_components_flat)
        new_inventory.save()
