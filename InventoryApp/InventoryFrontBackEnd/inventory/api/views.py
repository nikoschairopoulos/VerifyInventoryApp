from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from rest_framework import serializers
from inventory.api.serializers import (ComponentSerializer, DeletedComponentSerializer,
                                       InventorySerializer,
                                       FactorSerializer,
                                       CarbonIntensityDataSerializer,
                                       CarbonIntensityDataSerializerYear,
                                       LogsSerializer,
                                       RegressionValuesSerializer,
                                       SimaPro_runsSerializer)

from inventory.models import (Component,
                              Inventory,
                              LoggingComponent,
                              RegressionValues,
                              SimaPro_runs,
                              DeletedComponent)

from users.models import CustomUser

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
import pandas as pd 
from inventory.models import CarbonIntensityData,FactorElectricityYear
# from inventory.api.permissions import IsAdminUserOrReadOnly
from copy import deepcopy
from inventory.VerifyWebAppForm.component_form_reprentation_verify_app import json_form_behaviour
from rest_framework.exceptions import ValidationError
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import ExtractYear
from inventory.utils import get_local_ip


def error404(request):
    raise NotFound(detail="Error 404, page not found", code=404)

class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    #permission_classes = [IsAuthenticated]

    # def perform_destroy(self, instance):
    #     try:
    #         id = self.kwargs['pk']
    #         warning = self.check_for_component_usage(id)    
    #     except Exception as e:
    #         return {'exception':'lci id is not provided at delete request - something went wrong'}
    #     # if there is no warnings delete the components:
    #     if not warning:
    #          instance.delete()
    #          return{'success':{'component has been deleted'}}
    #     message = {f'warn_{index}':warn  for index,warn in enumerate(warning)}
    #     return message
    
    # this is called when a delete request
    # is done -> this method calls perform destroy
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     result = self.perform_destroy(instance)
    #     if 'exception' in result:
    #         return Response(result['exception'],status.HTTP_400_BAD_REQUEST)
    #     #successfull Deletion: 
    #     elif 'success' in result:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     #component has usage -> show warns at vue js modals
    #     else:
    #         return Response(result,status=status.HTTP_400_BAD_REQUEST)
        

        #super().destroy(request, *args, **kwargs)
        #return Response({'message':'hi'},status=400)
    
    # def check_for_component_usage(self,lci_id):
    #     ip = get_local_ip()
    #     response = requests.get(f"http://{ip}:3003/api/stored_lci_ids?component_id={lci_id}")
    #     json_response = response.json()
    #     warnings = []
    #     for key in ('verify_buildings', 'verify_districts', 'verify_district_buildings'):
    #         elements = json_response.get(key,None)
    #         for comp in elements:
    #             temp_dict = {'building_id':comp.get('building_id',None),
    #                         'scenario_id':comp.get('scenario_id',None),
    #                         'building_name':comp.get('building_name',None),
    #                         'scenario_name':comp.get('scenario_name'),
    #                         'district_id':comp.get('district_id',None),
    #                         'district_name':comp.get('district_name',None)
    #                         }
    #             record = {k:v for k,v in temp_dict.items() 
    #                     if v is not None}
    #             warnings.append(record)        
    #     return warnings
    
    

 

class InventoryViewSet(ModelViewSet):
    queryset=Inventory.objects.all()
    serializer_class = InventorySerializer
    # permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) #Additionally author is added (this is added procedure after serializer) 
                                                  #adds the user at validated_data ==> .create(**validated_data)


class FactorViewSet(ModelViewSet):
    queryset = Factor.objects.all()
    serializer_class = FactorSerializer
    #permission_classes = [IsAuthenticated]

class RegressionValuesViewSet(ModelViewSet):
    queryset = RegressionValues.objects.all()
    serializer_class = RegressionValuesSerializer
    permission_classes = [IsAuthenticated]
    #this called form create method when post request is called
    #calls create method of serializer (by default - if you want you can add totaly custom logic)
    # with the validated data
    def perform_create(self,serializer):
        serializer.save()  

class SimaPro_runsViewSet(ModelViewSet):
    queryset = SimaPro_runs.objects.all()
    serializer_class = SimaPro_runsSerializer
    #permission_classes = [IsAuthenticated]
    #this called form create method when post request is called
    #calls create method of serializer (by default - if you want you can add totaly custom logic)
    # with the validated data
    
    #def perform_create(self,serializer):
    #    serializer.save()  
    
    #def create(self, request, *args, **kwargs):
    #    request.data = json.loads(request.data)
    #    super().create(request,*args,**kwargs)

class DeletedComponentsViewSet(ModelViewSet):
    queryset = DeletedComponent.objects.all()
    serializer_class = DeletedComponentSerializer
    
    


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
             
# FOR Verify App (do not touch)
class Inventory_technologies(APIView):
    def get(self,request):
        technologies = []
        items = Component.objects.all()
        components = ComponentSerializer(items,many=True)
        for comp in components.data:
            if comp['SHEET_TYPE'] not in technologies:
                technologies.append(comp['SHEET_TYPE'])
        return Response(technologies)
    
# FOR Verify App (do not touch)
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

class Fetch_Specific_User_Custom_Plus_Defaults(APIView):
    def get(self,request,user_email):
        all_components = []
        try:
            #take current user:
            current_user = CustomUser.objects.get(email=user_email)
            #take all its inventories:
            inventories = current_user.inventories.all()
            #add all custom components of the inventories:
            for inventory in inventories:
                all_components.extend(inventory.components.all()) 
            default_components = Component.objects.filter(IS_MAIN_INVENTORY=True)
            #create overall component List:
            all_components.extend(default_components)
            component_serializer = ComponentSerializer(all_components,many=True)
            print(component_serializer.data)
            #return components
            return Response(component_serializer.data)
        except MultipleObjectsReturned as e:
            return Response(e)

class only_main_inventory(APIView):
    def get(self,request):
        all_main_objects = Component.objects.filter(IS_MAIN_INVENTORY=True)
        objects_main = ComponentSerializer(all_main_objects,many=True)
        return Response(objects_main.data)

# for Verify App
class inventory_without_components(APIView):
    def get(self,request):
        inventory_obj = Inventory.objects.all()
        result_inventory = InventorySerializer(inventory_obj,many=True).data #returns LIST of dicts
        for elem in result_inventory:
            del elem['components']
        return Response(result_inventory)

# for Verify Calculatons app
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


# Create Components from Excell form - LCI APP:
class CreateComponentFromExcell(APIView):
    def post(self, request):
        components_list = request.data
        components_serializer = ComponentSerializer(data=components_list, many=True)

        if components_serializer.is_valid():
            components_serializer.save()
            return Response(components_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(components_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# check if the user is staff user:
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

##### this is (bellow) a view to import excell file with hour electricity factors (converted before to dictionairy) into the Database
##### at the CarbonIntensityData Table

#####################################
#this is for hourly electricity data(post):
#####################################
class ImportElectricityData(APIView):
    def post(self,request):
        #measurements = json.loads(request.data)
        measurements = json.loads(request.data)
        #print(measurements)
        df = pd.DataFrame(measurements)
        #print(df)
        try:
            for index,row in df.iterrows():
                record = CarbonIntensityData(
                    datetime = row['Datetime (UTC)'],
                    country  = row['Country'],
                    zone_name = row['Zone Name'],
                    zone_id = row['Zone Id'],
                    carbon_intensity_gco2_eq_kwh_direct = row['Carbon Intensity gCO₂eq/kWh (direct)'],
                    carbon_intensity_gco2_eq_kwh_lca = row['Carbon Intensity gCO₂eq/kWh (LCA)'],
                    low_carbon_percentage = row['Low Carbon Percentage'],
                    renewable_percentage = row['Renewable Percentage'],
                    data_source = row['Data Source'],
                    data_estimated = row['Data Estimated'],
                    data_estimation_method = row['Data Estimation Method']
                )
                print(row)
                print(index)
                record.save()
                print('------PASS---------')
            data = {'message': 'Success'}
            return Response(data)  # Defaults to HTTP 200 OK
        except Exception as e:
            print(e)
            data = {'error': 'Invalid data'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


#####################################
#this is for hourly electricity data(get):
#####################################
class get_hourly_electricity_fuel_factors(APIView):
    def get(self, request, country, year):
        try:
            queryset = CarbonIntensityData.objects.filter(
                country=country,
                datetime__year=year
            ).order_by('datetime') 
            serializer = CarbonIntensityDataSerializer(queryset, many=True)
            df = pd.DataFrame(serializer.data)
            if df.empty:
                return Response({'error':'no country or year supported --> something went wrong'},status=status.HTTP_404_NOT_FOUND)
            res = df.to_json()
            #is not empty so send it:
            return Response(res)
        except Exception as e:
            return Response({'error':str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR)


#####################################
#this is for yearly electricity data (post):
#####################################
class ImportElectricityDataYearly(APIView):
    def post(self,request):
        try:
            co2_data = request.data
            for element in co2_data:
                record  = FactorElectricityYear(
                    country = element['country'] ,
                    year = element['year'],
                    measurement_co2 = element['measurement']
                )
                #save to DB
                print(element)
                print('--------------')
                record.save()
            data = {'message': 'Success'}
            return Response(data)  # Defaults to HTTP 200 OK
        except Exception as e:
            print(e)
            data = {'error': 'Invalid data'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


#####################################
#this is for yearly electricity data (get):
#####################################
class get_yearly_electricity_fuel_factors(APIView):    
    def get(self,request,country):
            try:
                queryset = FactorElectricityYear.objects.filter(country=country)
                data  = CarbonIntensityDataSerializerYear(queryset,many=True).data
                if queryset.exists():
                    return Response(data)
                else:
                    return Response({'error': f"No data found for country: {country}"}, status=status.HTTP_404_NOT_FOUND)
            #catch any other exception
            except Exception as e :
                return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#####################################
# get countries that have yearly Data:
# get countries that have hourly Data:
#####################################
class get_countries_hourly_yearly_electricity_factors(APIView):
    def get(self,request):
        queryset_hourly =  CarbonIntensityData.objects.values_list('country',flat=True).distinct()
        queryset_yearly =  FactorElectricityYear.objects.values_list('country',flat=True).distinct()
        response_data = {'hourly':queryset_hourly,
                         'yearly':queryset_yearly,
                         'common': list(set(queryset_hourly) & set(queryset_yearly))
                         }
        return Response(response_data)


##############################################
#Take the logs for all components 
#note: here is one to many --> take the component of the log --> take its information --> map to the response as you want
###############################################
class get_components_logs(APIView):
    def get(self,request,lci_id):
        query_set = LoggingComponent.objects.filter(fk_id=lci_id).order_by('-created_at')
        serializer = LogsSerializer(query_set,many=True)
        logs = serializer.data
        response_data = []
        for log in logs:
            response_data.append({'messages':[ {attribute:m for attribute,m in 
                                                json.loads(log['message']).items()}],
                                  'created_at':log['created_at']})
        return Response( response_data )

##############################################
#at this method given specific time window
#will retrieve the pictrure of component
#in order to aquire informations about a components
#values for a specific project
##############################################
class give_picture_of_component_from_timestamp(APIView):

    def get(self,request,lci_id):
        all_reconstructions = self.create_all_reconstructions(lci_id=lci_id)
        return all_reconstructions

    def create_all_reconstructions(self,lci_id):
        try:
            #take the component:
            isinstance = Component.objects.get(pk=lci_id)
            #serialize the component
            component = ComponentSerializer(isinstance).data
            #take its logs:
            query_set = LoggingComponent.objects.filter(fk_id=lci_id).order_by('-created_at') #These are already order by desceding order
            logs = LogsSerializer(query_set,many=True).data
            #add every reconstruction at this list:
            reconstructions = []
            current = component
            #add the current state:
            reconstructions.append({"timestamp":'now','reconstuction':deepcopy(current)})
            ################
            #logs are ordered from the latest to the older
            ################
            for log in logs:
                #Take the message key from log:
                message = json.loads(log['message'])
                #take all old values:
                old_values =  { atribute: message[atribute]['old_value']  
                                for atribute in  message.keys() }
                #replace the current values with the old values:
                current.update(old_values)
                #add the reconstruction to reconstructions list
                reconstructions.append({'timestamp':log['created_at'],
                                        'reconstruction':deepcopy(current)})
            return Response(reconstructions)
        except Exception as e:
            return Response({'error':e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #        
    def go_to_previous_component():
        pass

    #here we want to take in descending order the components
    def group_by_timestamp(self):
        pass


#################################
#At this view, all regression
#are taken for a specific lci id
#################################
class regression_values(APIView):
    def get(self,request,lci_id):
        queryset = RegressionValues.objects.filter(fk=lci_id)
        serializer = RegressionValuesSerializer(queryset,many=True)
        return Response(serializer.data)


################################
#to do: here create one method 
#that given the lci id --> embodied co2, 
#embodied pe , eol_co2 , col_pe (these two will be average of measurement entris prercentages)
################################
'''
class get_embobied_eol_values(APIView):
    def get(self,request,lci_id,rating):
        rating_float = float(rating)
        data =  {   
                    'embodied_co2':rating_float * lci_id,
                    'embodied_pe':rating_float * lci_id,
                    'eol_co2':rating_float * lci_id,
                    'eol_pe':rating_float * lci_id
                }
        
        return Response(data)
'''
        
class get_embobied_eol_values(APIView):
    def get(self,request,lci_id,rating,internal_request=None):
        self.result = {}
        component_rating  = float(rating)
        lci_id = int(lci_id)
        
        queryset = SimaPro_runs.objects.filter(vcomponent_id=lci_id)
        if not queryset:
            return Response({f'message':'there is no simapro runs for lci_id = {lci_id}'},
                            status=status.HTTP_404_NOT_FOUND)
        if component_rating<=0:
            return Response({'message':'rating must be positive number'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # these will insert tuples (rating,embodied)
        # Assume first point is the (0,0)        
        co2_values = []
        pe_values  = []
        
        # take all records into a list of dicts:
        serializer = SimaPro_runsSerializer(queryset,many=True)
        entries_list = serializer.data

        # iterate to take the values for Embodied Co2 and Pe scaling:
        for record in entries_list:
            co2_values.append((record["fu_quantity"],record['stage_A_gwp_kgco2eq']))
            pe_values.append((record["fu_quantity"],record["stage_A_embodied_pe_gj"]))
        
        #Validations:
        #1. if does not have correct format raise exception (not applied)
        #2. if has fake simapro run return all zeros
        #3. if none of 1,2 continue -> is a regural scaling procedure
        check = self.check_points(co2_values=co2_values,pe_values=pe_values)
        if check:
            #if it is a '0 rating' component return 0 at all keys else continue:
            embodied_plus_extra_info = self.fill_with_null_extra_info(lci_id=lci_id)
            return Response(embodied_plus_extra_info)
        
        #continue regression after validations:
        self.continue_regression(co2_values=co2_values,
                                 pe_values=pe_values,
                                 component_rating=component_rating,
                                 entries_for_eol=entries_list[0])
        
        # Add extra info:
        AUTOMATED_FORM_INFO = {f'STAGE_{stage_type}':self.distribute_the_stages([lci_id],stage_type=stage_type) 
                                                    for stage_type in{'A','C'}}
        # Add the FORM 
        self.result.update({'extra_info':AUTOMATED_FORM_INFO})
        #return the result:
        return Response(self.result)

    # is for district heating component etc
    def fill_with_null_extra_info(self,lci_id):
        component = Component.objects.get(pk = lci_id)
        
        # add zeros at embodied - eol
        result = {"embodied_co2": 0,
                     "embodied_pe": 0,
                     "eol_co2": 0,
                     "eol_pe": 0,
                     "eol_co2_ratio" : 0,
                     "eol_pe_ratio":0
                 }
        
        # add null to extra info
        result['extra_info'] =  {
            "STAGE_A": {
                f"{component.name}": {
                    "fu_quantity": None,
                    "stage_A_LCA_version": None,
                    "stage_A_IA_method_GWP": None,
                    "stage_A_IA_method_PE": None,
                    "stage_A_comments": None,
                    "vcomponent_id": None,
                    "stage_A_LCA_DB": None
                }
            },
            "STAGE_C":{
            f"{component.name}": {
                    "fu_quantity": None,
                    "stage_C_LCA_version": None,
                    "stage_C_IA_method_GWP": None,
                    "stage_C_IA_method_PE": None,
                    "stage_C_comments": None,
                    "vcomponent_id": None,
                    "stage_C_LCA_DB": None
                }
            }
        }                    
        return result

    def continue_regression(self,co2_values,pe_values,component_rating,entries_for_eol):
        # Continue making them with asceding order adding (0,0) for regression first point:
        co2_values.append((0,0))
        pe_values.append((0,0))
        # sort the lists in asceding order:
        co2_values_new = self.sort_tuples_by_first_element(co2_values)
        pe_values_new  = self.sort_tuples_by_first_element(pe_values)

        #do regression for each one of co2 and pe
        embodied_co2 = self.do_regression(co2_values_new,component_rating=component_rating)
        embodied_pe  = self.do_regression(pe_values_new,component_rating=component_rating)
        
        self.result.update({
            "embodied_co2": embodied_co2,
            "embodied_pe": embodied_pe *(1000/3.6)
        })
        #set eol:
        self.set_eol(entries_for_eol) # take the first record for EoL because are all the same:


    
    def check_points(self,co2_values,pe_values):
        #raise exception here else None
        #self.has_not_correct_point(co2_values)
        #self.has_not_correct_point(pe_values)
        
        #handle same points in case there are point with same rating:
        #TODO: handle to take the most newer for same rating

        #check if the only simapro run is (0,0) -> is an assumption simapro run for District Heating etc
        has_only_co2_x_0_y_0 = self.get_zero_values_if_only_zero_fu_provided_at_simapro_run(co2_values)
        has_only_pe_x_0_y_0 = self.get_zero_values_if_only_zero_fu_provided_at_simapro_run(pe_values)
        return has_only_pe_x_0_y_0 and has_only_co2_x_0_y_0
        
    
    def get_zero_values_if_only_zero_fu_provided_at_simapro_run(self,values):
        return set(values) == {(0,0)} 


    def do_regression(self,measurements_list,component_rating):
        point = None
        for index, (current_rating, _ ) in enumerate(measurements_list):
            if component_rating <= current_rating and (not point):
                point = index
        
        if point is None:
            #keep the last linear segment:
            point = -1

        x2, x1 = measurements_list[point][0] , measurements_list[point-1][0]
        y2, y1 = measurements_list[point][1] , measurements_list[point-1][1]
        
        embodied_value = self.get_regression_value(y2,y1,x2,x1,
                                                   point = point,
                                                   component_rating = component_rating)
        return embodied_value
    
    def get_regression_value(self,y2,y1,x2,x1,point,component_rating):
        #create_slope:
        try:
            slope = (y2 - y1) / (x2 - x1)
            if point != -1:
                return slope * (component_rating - x1) + y1
            else:
                return (y2 / x2) * component_rating
        except ZeroDivisionError:
            raise ValidationError({'detail': 'Division by zero encountered during regression calculation.'})

    
    def set_eol(self,record):
        embodied_co2, embodied_pe = self.result['embodied_co2'], self.result['embodied_pe']
        # you only need to update for the first record
        # is correct because these are common for 
        # specific lci id 
        self.result.update({
            "eol_co2": record["eol_gwp_pc"] * (embodied_co2/100),
            "eol_pe":record["eol_embodied_pe_pc"] * (embodied_pe/100)
        })
        # Add percentages of eol at results:
        self.result.update({
                        "eol_co2_ratio": record["eol_gwp_pc"],
                        "eol_pe_ratio": record["eol_embodied_pe_pc"]
        })

    
    def sort_tuples_by_first_element(self,tuple_list):
        # Sort the list of tuples by the first element in each tuple
        return sorted(tuple_list, key=lambda x: x[0])

    def distribute_the_stages(self, lci_id, stage_type):
        comp_instance = Component.objects.get(pk=lci_id[0])
        scenario_components =   [ComponentSerializer(comp_instance).data]
        
        result = {}
        attributes_to_include = [
            'LCA_version',
            'IA_method_GWP',
            'IA_method_PE',
            'comments',
            'LCA_DB',
        ]
        
        # create the correct columns to search
        filtered = [f'stage_{stage_type}_' + attr for attr in attributes_to_include] + ['vcomponent_id','fu_quantity']
        #db_index = [index for index,comp in enumerate(filtered) if comp[-2:] == 'DB'][0]
        #filtered[db_index] = f'stage_{stage_type}_LCA_DB' 
        # Iterate over each component in the scenario to distribute stage data
        for component in scenario_components:
            # Apply min function to get the Simapro run with the minimum fu_quantity
            min_simapro_run = min(component['simapro_runs'], key=lambda x: x.get('fu_quantity', float('inf')))
            
            # Update the result with filtered stage data
            result[component['name']] = {
                k: v for k, v in min_simapro_run.items() if k in filtered
            }

        return result


#####################################
# This is a form to add configurations
# for verify web app lci input forms
#####################################
class FormRepresentationVerifyApp(APIView):
    def get(self,request):
        result  = deepcopy(json_form_behaviour)
        result['building_level']['technologies'][-1]['types'] = [{'text':elem['text'],'value':elem['value'],'subtypes':None} 
                                                                for elem in json_form_behaviour['building_level']['technologies']
                                                                if elem['text']!='Building Level - Auxiliary Assets']
        return Response(result)


#####################################
# this gives all components 
# without simapro run
#####################################
class get_all_components_without_simapro_runs(APIView):
    def get(self,request):
        #take all simapro runs FKs:
        simapro_run_set = SimaPro_runs.objects.values_list('vcomponent_id',flat=True)
        #exclude components that have simapro runs:
        components = Component.objects.exclude(id__in = simapro_run_set)
        data = ComponentSerializer(components,many=True).data
        return Response(data)


##########################################
# Get all components for Verify B
# Dataframe - Calculations Modules Creation
##########################################
class GetComponentsForCalculationModule(APIView):
    class ComponentSerializerLocal(serializers.ModelSerializer):
        class Meta:
            model = Component
            fields = '__all__'

    def get(self, request):
        query_set = Component.objects.all()
        # Use the nested serializer class
        serializer = self.ComponentSerializerLocal(query_set, many=True)
        return Response(serializer.data)
    
##########################################
#  Return information about components
#  for the automated forms
'''
STAGE A
- LCA software used
- GWP Impact Assessment Method
- PE Impact Assessment Method
- Database
- Comments

STAGE C
- LCA software used
- GWP Impact Assessment Method
- PE Impact Assessment Method
- Database
- Comments
'''
##########################################

class ReportInfoComponents(APIView):
    def post(self, request):
        # Take JSON (request.data is already parsed to a dictionary)
        form_data = request.data
        
        result = {scenario_name: {'STAGE_A': [], 'STAGE_C': [], 'components': []} for scenario_name in form_data.keys()}

        # Iterate over scenarios
        for scenario_name, components in form_data.items():
            for component in components:
                try:
                    # Fetch component from the database
                    comp_instance = Component.objects.get(pk=component)
                    comp_serializer = ComponentSerializer(comp_instance)
                    result[scenario_name]['components'].append(comp_serializer.data)
                except ObjectDoesNotExist:
                    return Response({'error': 'There is no component with this specific id'}, status=status.HTTP_404_NOT_FOUND)
                except MultipleObjectsReturned:
                    return Response({'error': 'Multiple components found for the same id'}, status=status.HTTP_409_CONFLICT)

            # Distribute the stage data for A and C stages
            for stage_type in {'A', 'C'}:
                components_of_scenario = result[scenario_name]['components']
                result[scenario_name][f'STAGE_{stage_type}'] = self.distribute_the_stages(components_of_scenario, stage_type=stage_type)
            
            # Remove 'components' key from the result for each scenario
            del result[scenario_name]['components']

        return Response(result)
    
    @staticmethod
    def distribute_the_stages(self, scenario_components, stage_type):
        result = {}
        attributes_to_include = [
            'LCA_version',
            'IA_method_GWP',
            'IA_method_PE',
            'comments',
            'LCA_DB',
        ]
        
        # create the correct columns to search
        filtered = [f'stage_{stage_type}_' + attr for attr in attributes_to_include] + ['vcomponent_id','fu_quantity']
        db_index = [index for index,comp in enumerate(filtered) if comp[-2:] == 'DB'][0]
        filtered[db_index] = f'stage_{stage_type}_LCA_DB' 
        # Iterate over each component in the scenario to distribute stage data
        for component in scenario_components:
            # Apply min function to get the Simapro run with the minimum fu_quantity
            min_simapro_run = min(component['simapro_runs'], key=lambda x: x.get('fu_quantity', float('inf')))
            
            # Update the result with filtered stage data
            result[component['name']] = {
                k: v for k, v in min_simapro_run.items() if k in filtered
            }

        return result
    
# This end point returns all hourly 
# factors of a country, order by year
# IN ASCENDING ORDER
class fetch_all_distinct_year_for_hourly_electricity_factors_for_a_country(APIView):
    def get(self,request,country):
        years = (CarbonIntensityData.objects.annotate(year = ExtractYear("datetime")).
                                               values_list("year",flat=True).
                                               distinct().
                                               order_by("year"))
        if years.exists():
            return Response(data = years,status=status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
##########################
'''
this apiview is created to be given a district json
and calculate the environmental and economical analytics
for each component for each sector
'''
##########################
class calculate_district_component_analytics(APIView):
    def calculate_component_analytics(self,component):
        try:
            analytics = {}          
            analytics['name'] = Component.objects.get(id=component["lci_id"]).name
            analytics['verify_id'] = component['id']
            analytics['verify_lci_id'] = component['lci_id']
            analytics['installed_ugs'] = component['installed_ugs']
            print(analytics['name'])
            keys_to_return = ["embodied_co2","embodied_pe","eol_co2","eol_pe"]
            # get the environmental:
            # create an object of another apiview (the service with the embodied calculations)
            embodied_obj = get_embobied_eol_values()
            response = embodied_obj.get(request = None,
                                        lci_id = component['lci_id'],
                                        rating = component['installed_ugs'],
                                        internal_request=True).data
            analytics.update({key:response[key]
                    for key in response if key in keys_to_return})
            # add economics:
            analytics.update({'capex':component['capex'],'annual_maintenance':component['maintenance_cost']})

        except ObjectDoesNotExist:
            print("------------------")
            print(f"error: component with lci_id = {component['lci_id']}, does not exist")
            print("------------------")
            pass
        except KeyError:
            print('glazing component')
        return analytics
    
    def get(self, request):
        # For GET requests, we'll just show the form
        return render(request, '../templates/inventory/input_form.html')
    
    def post(self,request):
        web_json = request.data
        response_data = {}
        scenario_keys = ['base','var']
        for scenario_key in scenario_keys:
            response_data[scenario_key] = {}
            if scenario_key in web_json:
                sector_keys = [key for key in web_json[scenario_key] if '_sector' in key]
                for sector_key in sector_keys:
                    response_data[scenario_key][sector_key] = []
                    # add components:
                    if sector_key == "building_sector":
                        for building in web_json[scenario_key][sector_key]['building']:
                            for technology_key in building['components']:
                                for component in building['components'][technology_key]:
                                     response_data[scenario_key][sector_key].append(self.calculate_component_analytics(component))            
                    else:   
                        sector_components =web_json[scenario_key][sector_key]['components']
                        for component in sector_components:
                            response_data[scenario_key][sector_key].append(self.calculate_component_analytics(component))
        #return Response(data=response_data)
            # Either render to HTML template or return as JSON based on Accept header
        # if 'text/html' in request.headers.get('Accept', ''):
        #     return render(request, 'component_analytics_table.html', {
        #         'data': response_data,
        #     })
        # else:
        #     # Default to JSON response
        #     return Response(data=response_data)
        
        # calucalte_building_components
        # calculate district components
        return render(request,'../templates/inventory/component_analytics_table.html', {
                 'data': response_data,
             })




            
