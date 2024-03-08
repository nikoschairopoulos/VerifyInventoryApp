import requests

def client():

    #LOGIN:
    credentials = {"username":"admin",
                   "password":"123456"
                   }
    
    response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/",
                              data=credentials)
    print(response.json()['key'])

    token = 'Token '+response.json()['key']
    headers = {'Authorization':token}

    #make the request:
    response = requests.get('http://127.0.0.1:8000/api/component/',headers=headers)
    print(response.status_code)
    print(response.json())



if __name__ == "__main__":
    print(requests.get('http://127.0.0.1:8000/api/inventory/',
                       headers={'Authorization':'Token 5bff5a101277474b47cec46915b6b67998c3ea80'}).json())
