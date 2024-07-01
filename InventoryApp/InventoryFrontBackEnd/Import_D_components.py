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

#from folder.subfolder.myfile import tade

if __name__  != "__main__":
    raise RuntimeError("Do not import from this script")

#add path:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryapi.settings')
django.setup()
from inventory.models import Component
from inventory.api.serializers import ComponentSerializer
import pandas as pd 

#FILES PATH:
CURRENT_DIRECTORY = Path(__file__).parent.absolute()


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




