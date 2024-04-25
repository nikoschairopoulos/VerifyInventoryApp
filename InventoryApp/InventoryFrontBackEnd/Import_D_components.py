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
DATA_FILE = CURRENT_DIRECTORY/'library_new.xlsm'

## NOT ADD SECTION:
#SUBTYPES_TO_NOT_ADD_PLANTS = {'pemfc','pafc','safc','afc','sofc','mcfc'}
##

class FillDataBaseWithComponentsD:

    def __init__(self):
        print('loader initialized..')
        #print(Component.objects.all())

    def load_components(self):
        '''
        #script_dir = os.path.dirname(os.path.abspath(__file__))
        #file_path = os.path.join(script_dir,'library_new.xlsm')
        '''
        DATAFRAME_DICT_COMPONENTS = FillDataBaseWithComponentsD.read_library( DATA_FILE )
        for SHEET_TYPE, dataframe_of_sheet_type in DATAFRAME_DICT_COMPONENTS.items():
            #print(comp)
            for index, row in dataframe_of_sheet_type.iterrows():
                comp_dict = row.to_dict()
            
                #Add name of the component:
                component_name = f"{comp_dict['type']}_{comp_dict['subtype']} (default)"
               
                #DO SOME RENAMINGS:
                comp_dict['name'] = component_name
                comp_dict['component_type'] = comp_dict.pop('type')
                comp_dict['component_subtype'] = comp_dict.pop('subtype')
                comp_dict['capex_per_ugs'] = comp_dict.pop('capex/u.g.s.')
                comp_dict['embodied_co2_per_ugs'] = comp_dict.pop('embodied_co2/u.g.s.')
                comp_dict['embodied_pe_per_ugs'] = comp_dict.pop('embodied_pe/u.g.s.')
                comp_dict['pref_cost'] = comp_dict.pop('Pref_cost')
                comp_dict['pref_env'] = comp_dict.pop('Pref_env')
                comp_dict['SHEET_TYPE'] = SHEET_TYPE
                comp_dict['IS_MAIN_INVENTORY'] = True
                comp_dict['replace_or_die'] = 'replace'
                comp_dict['IS_B_COMPONENT'] = False
                #breakpoint()

                #SERIALIZE AND LOAD:
                serializer = ComponentSerializer(data=comp_dict)
                if serializer.is_valid():
                    new_component = serializer.save()
                    #breakpoint()
                else:
                    print("error:",serializer.errors)

    def specify_b_components(self):
        objects_b = Component.objects.filter(IS_B_COMPONENT=None)
        for obj in objects_b:
            obj.IS_B_COMPONENT = True
            obj.save()

        
###################
#Methods from Verify
###################
    @staticmethod
    def read_library_sheet(path, sheet_name):
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

    @staticmethod
    def read_library(path):
        sheets = [
            #"Thermal Sources",
            #"Ventilation",
            #"Glazing",
            #"Insulation",
            #"PCM",
            #"Water Storage",
            #"El. Generators",
            #"El. Storage",
            #"Various Assets",
            #"Rigid Materials",
            #"Fuels",
            #"El. Profiles",
            "Plants",
            "Transport",
            "Public"
        ]
        library = {sheet: FillDataBaseWithComponentsD.read_library_sheet(path, sheet) for sheet in sheets}
        return library




# Iterate over each path in sys.path and print it
    #for path in sys.path:
    #    print(path)

#obj = FillDataBaseWithComponentsD()
#obj.load_components()


'''
FUNCTION TO UPDATE NAMES:
'''
#update_name = {component_name="this is a new name"}
def update_component(primary_key,update_name):
    obj = get_object_or_404(Component,pk=primary_key)
    data_of_object = ComponentSerializer(obj).data
    del data_of_object['name']
    data_of_object['name'] =  update_name
    serializer = ComponentSerializer(instance=obj,data=data_of_object)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)



#update_component(338,'update_name')
obj = FillDataBaseWithComponentsD()
obj.load_components()
obj.specify_b_components()

