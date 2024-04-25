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
sys.path.append('/home/nikos/Desktop/InventoryApp/InventoryApp/InventoryFrontBackEnd')
#from django_project import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryapi.settings')
django.setup()


from inventory.models import Component
from inventory.api.serializers import ComponentSerializer
import pandas as pd 

# This is a test:

class FillDataBaseWithComponentsD:
    #print(Component.objects.all())
    def load_components(self):
        DATAFRAME_DICT_COMPONENTS = self.read_library('/inventory')
        for comp in DATAFRAME_DICT_COMPONENTS.values():
            serializer = ComponentSerializer(data=comp)
            if serializer.is_valid():
                new_component = serializer.save()
            else:
                print("error:",serializer.errors)
    
    @classmethod
    def read_library(cls,path):
        sheets = [
            "Thermal Sources",
            "Ventilation",
            "Glazing",
            "Insulation",
            "PCM",
            "Water Storage",
            "El. Generators",
            "El. Storage",
            # "Various Assets",
            "Rigid Materials",
            "Fuels",
            "El. Profiles",
            # "Plants"
        ]
        library = {sheet: cls.read_library_sheet(path, sheet) for sheet in sheets}
        return library
    
    @classmethod
    def read_library_sheet(cls,path, sheet_name):
        df = pd.read_excel(path, sheet_name=sheet_name, skiprows=1)
        df = df.iloc[:, 1:]
        df = df[df.columns[~df.columns.isin(["source"])]]
        df = df.dropna(axis=1, how="all")
        # df = df[~df.isna().any(axis=1)]
        df = (
            df.dropna(axis=0, how="any")
            if sheet_name != "Fuels"
            else df.dropna(axis=0, how="all")
        )
        # print(df)
        return df

