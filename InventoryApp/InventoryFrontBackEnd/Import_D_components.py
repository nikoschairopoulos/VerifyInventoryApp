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

#from folder.subfolder.myfile import tade

if __name__  != "__main__":
    raise RuntimeError("Do not import from this script")

#add path:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryapi.settings')
django.setup()
from inventory.models import (Component, 
                                Factor)
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

factors = Factor.objects.all()
print(factors)

for factor in factors:
    #factor.comments = 'initial year is considered 2018 but it is not sure. Year 2018 is used as a reference'
    #factor.year = 2018
    factor.source = 'source is not provided'
    factor.save()