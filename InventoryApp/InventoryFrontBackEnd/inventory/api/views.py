from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from inventory.api.serializers import ComponentSerializer,InventorySerializer,FactorSerializer
from inventory.models import Component,Inventory
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from inventory.models import Inventory
from inventory.models import Factor
from rest_framework.exceptions import NotFound
from rest_framework import status
import requests
from django.http import HttpResponse
import json 
#from inventory.api.permissions import IsAdminUserOrReadOnly

def error404(request):
    raise NotFound(detail="Error 404, page not found", code=404)

class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    #permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        try:
            id = self.kwargs['pk']
            warning = self.check_for_component_usage(id)    
        except Exception as e:
            return {'exception':'lci id is not provided at delete request - something went wrong'}
        # if there is no warnings delete the components:
        if not warning:
             instance.delete()
             return{'success':{'component has been deleted'}}
        message = {f'warn_{index}':warn  for index,warn in enumerate(warning)}
        return message

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        result = self.perform_destroy(instance)
        if 'exception' in result:
            return Response(result['exception'],status.HTTP_400_BAD_REQUEST)
        #successfull Deletion: 
        elif 'success' in result:
            return Response(status=status.HTTP_204_NO_CONTENT)
        #component has usage -> show warns at vue js modals
        else:
            return Response(result,status=status.HTTP_400_BAD_REQUEST)
        

        #super().destroy(request, *args, **kwargs)
        #return Response({'message':'hi'},status=400)
    
    def check_for_component_usage(self,lci_id):
        response = requests.get(f"http://192.168.101.31:3003/api/stored_lci_ids?component_id={lci_id}")
        json_response = response.json()
        warnings = []
        for key in ('verify_buildings', 'verify_districts', 'verify_district_buildings'):
            elements = json_response.get(key,None)
            for comp in elements:
                temp_dict = {'building_id':comp.get('building_id',None),
                            'scenario_id':comp.get('scenario_id',None),
                            'building_name':comp.get('building_name',None),
                            'scenario_name':comp.get('scenario_name'),
                            'district_id':comp.get('district_id',None),
                            'district_name':comp.get('district_name',None)
                            }
                record = {k:v for k,v in temp_dict.items() 
                        if v is not None}
                warnings.append(record)        
        return warnings

 

class InventoryViewSet(ModelViewSet):
    queryset=Inventory.objects.all()
    serializer_class = InventorySerializer
    #permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) #Additionally author is added (this is added procedure after serializer) 
                                                  #adds the user at validated_data ==> .create(**validated_data)


class FactorViewSet(ModelViewSet):
    queryset = Factor.objects.all()
    serializer_class = FactorSerializer
    #permission_classes = [IsAuthenticated]


                                            ####CUSTOM VIEWS (NON MODELS)####:

#take the inventories of a user:
class ListInventory(APIView):
    def get(self,request):
        items = Inventory.objects.filter(author__username=request.user.username)
        serializer = InventorySerializer(items,many=True)
        return Response(serializer.data)


#https://copyprogramming.com/howto/retrieving-a-single-object-of-interest-rather-than-blog-objects-all-in-django-rest-framework
# Here we define that class, where verify backend will take its inventory
class LIBRARY_VERIFY(APIView):
    serializer_class = InventorySerializer
    #lookup_field = "id" # is the id
    def get(self, request, pk, *args, **kwargs): #pk is the path-parameter
        inventory_id = pk # param from URL
        inventory_object = get_object_or_404(Inventory,pk=inventory_id)
        serializer = InventorySerializer(inventory_object, 
                                    context={'request': request})
        data_to_response = self.group_per_sheet(serializer.data)
        return Response(data_to_response)   
    
    def group_per_sheet(self,data):
        response_dict={}
        #INITIALIZE THE DICT
        for component in data['components']:
            response_dict[component['SHEET_TYPE']] = []    
        #Add the components 
        for component in data['components']:
            response_dict[component['SHEET_TYPE']] += [dict(component)]
        return response_dict
        # to do --> this functio group by the inventory


#take all the components of a technology
#/api/component/variable
#variable: take sheet type values
class Components_by_technology(APIView):
    #define http methods:
    def get(self,request,Technology_key):
        items = Component.objects.filter(SHEET_TYPE=Technology_key) # filter to fetch the python objects you want
        components = ComponentSerializer(items,many=True)           # serialize the components -> taking the serialize indide it .data have the dicts
        return Response(components.data)                            # return response
             
#FOR Verify App (do not touch)
class Inventory_technologies(APIView):
    def get(self,request):
        technologies = []
        items = Component.objects.all()
        components = ComponentSerializer(items,many=True)
        for comp in components.data:
            if comp['SHEET_TYPE'] not in technologies:
                technologies.append(comp['SHEET_TYPE'])
        return Response(technologies)
    
#FOR Verify App (do not touch)
class Specific_inventory_plus_default(APIView):
    def get(self,request,pk):
        #take the inventory:
        inventory =  get_object_or_404(Inventory,pk=pk)
        #take its components:
        component_inventory = ComponentSerializer(inventory.components,many=True).data # list of dicts 
        #filter if somehow exist a MAIN INVENTORY ELEMENT
        component_inventory_1 = list(filter(lambda i: i['IS_MAIN_INVENTORY']!=True, component_inventory)) # put a lamda expression and an iterable
        #take all the default components:
        components_default = Component.objects.filter(IS_MAIN_INVENTORY = True)
        component_inventory_2 = ComponentSerializer(components_default,many=True).data   #list of dicts
        result = {"custom":component_inventory_1,"default":component_inventory_2}
        #result = component_inventory_1 + component_inventory_2 (fetch all without formating) / every component_inventory is a list of dicts
        return Response(result)

class only_main_inventory(APIView):
    def get(self,request):
        all_main_objects = Component.objects.filter(IS_MAIN_INVENTORY=True)
        objects_main = ComponentSerializer(all_main_objects,many=True)
        return Response(objects_main.data)

#for Verify App
class inventory_without_components(APIView):
    def get(self,request):
        inventory_obj = Inventory.objects.all()
        result_inventory = InventorySerializer(inventory_obj,many=True).data #returns LIST of dicts
        for elem in result_inventory:
            del elem['components']
        return Response(result_inventory)

#for Verify Calculatons app
class find_fuel_factors_specific_country(APIView):
    def get(self,request,country):
        fuel_json = {'pef':{},'co2':{}}
        fuel_factors = Factor.objects.filter(country=country) #returns many records --> queryset > 1
        fuel_factors_data =  FactorSerializer(fuel_factors,many=True).data
        if fuel_factors_data:
            for elem in fuel_factors_data:
                fuel_json['pef'][elem['fuel']] = elem['primary_energy_factor']
                fuel_json['co2'][elem['fuel']] = elem['co2_factor']
            return Response(fuel_json)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


#Create Components from Excell form - LCI APP:
class CreateComponentFromExcell(APIView):
    def post(self, request):
        components_list = request.data
        components_serializer = ComponentSerializer(data=components_list, many=True)

        if components_serializer.is_valid():
            components_serializer.save()
            return Response(components_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(components_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#check if the user is staff user:
class IsAdminUser(APIView):
    def get(self,request):
        return Response({'is_admin': request.user.is_staff}) 



###### login redirect: this solves the problem with the use of the Middleware:
from django.shortcuts import render
from pathlib import Path
def homepage_view(request):
    CURRENT_DIRECTORY = Path(__file__).parent.absolute()
    print('----------------',CURRENT_DIRECTORY)
    FILE = f'{CURRENT_DIRECTORY}/../../templates/index.html'
    print(FILE)
    return render(request, FILE)  # Vue.js entry point