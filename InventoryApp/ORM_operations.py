import requests


#consume the api
response = requests.get("http://192.168.101.31:3003/api/stored_lci_ids?component_id=3")
warnings = []
json_response = response.json()
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

def check_for_component_usage(lci_id):
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
    #if is empty you can delete the component
    return warnings






# print message:
'''
component is used at the bellow:
    buildings: 
        1.(building_id:10,scenario_id:8,building_name:Demo building,scenario_name:Demo Scenario)
        2.(building_id:10,scenario_id:8,building_name:Demo building,scenario_name:Demo Scenario)
    districts:
        1.
    
    district_buildings:
        1.

'''