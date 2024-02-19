from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from inventory.api.serializers import ComponentSerializer,InventorySerializer
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



                                            ####CUSTOM VIEWS (NON MODELS)####:


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




