from django.shortcuts import render
from rest_framework.views import APIView
from .models import CustomUser
from inventory.models import Inventory
from rest_framework.response import Response
from .conf import (WORD,KEY)

class CreateUser(APIView):
    def post(self,request):
        data = request.data
        #take project name
        project_name = data['user_email'].split('@')[0]
        
        arguments = {
            'is_superuser':False,
            'username':f'user_{project_name}',
            'first_name':'',
            'last_name':'',
            'email':data['user_email'],
            'is_staff':False,
            'is_active':True
        }
        #create user:
        user_to_add = CustomUser(
            **arguments
        )

        #hash the password:
        user_to_add.set_password(f'{WORD}_{project_name}')
        user_to_add.save()


        #create a blank inventory for this user:
        new_inventory = Inventory(**{
            'author':user_to_add,
            'name':'custom_invnentory: '+f'{project_name}',
            'project_name':'project_name'
        })
        new_inventory.save()

        return Response({'message':f'new LCI user have been created with emai: {arguments["email"]}'})
        

# Create your views here.
