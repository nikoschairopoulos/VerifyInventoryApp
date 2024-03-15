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
#from inventory.api.permissions import IsAdminUserOrReadOnly


class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    #permission_classes = [IsAuthenticated]

class InventoryViewSet(ModelViewSet):
    queryset=Inventory.objects.all()
    serializer_class = InventorySerializer
    #permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) #Additionally author is added (this is added procedure after serializer) (not implemented at serializer)


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
             

class Inventory_technologies(APIView):
    def get(self,request):
        technologies = []
        items = Component.objects.all()
        components = ComponentSerializer(items,many=True)
        for comp in components.data:
            if comp['SHEET_TYPE'] not in technologies:
                technologies.append(comp['SHEET_TYPE'])
        return Response(technologies)
    

class Specific_inventory_plus_default(APIView):
    def get(self,request,pk):
        #take the inventory:
        inventory =  get_object_or_404(Inventory,pk=pk)
        #take its components:
        component_inventory_1 = ComponentSerializer(inventory.components,many=True).data # list of dicts 
        #take all the default components:
        components_default = Component.objects.filter(IS_MAIN_INVENTORY = True)
        component_inventory_2 = ComponentSerializer(components_default,many=True).data   #list of dicts
        result = {"custom":component_inventory_1,"default":component_inventory_2}
        #result = component_inventory_1 + component_inventory_2 (fetch all without formating) / every component_inventory is a list of dicts
        return Response(result)


