import requests
import json
import base64

#REGISTRADORES 
REGISTRYS = ["192.168.122.10"]

auth_data = {
    "username": "narciso",
    "password": "2001"
}
auth_data_encoded = base64.b64encode(json.dumps(auth_data).encode()).decode()

ADRESS = 'https://192.168.122.190:7766'
USERNAME = 'narciso'
PASSWORD = '2001'
TLS_VALUE =  False
#URL
CREATE_VOLUME = "volumes/create"
GET_VOLUMES = "volumes"
GET_VOLUME = "volumes/"#<name>
CREATE_CONTAINER = "containers/create"
START_CONTAINER = "containers" #<ID>/start


#Retorna as Credencias de Autenticacao
def getAuth():
    # Configurar as informações de conexão
    username = USERNAME
    password = PASSWORD
    # Autenticar com o servidor proxy reverso Nginx
    auth = requests.auth.HTTPBasicAuth(username, password)
    return auth

#cria o volume
def createVolume(auth, volumeData):
    response = requests.post(f"{ADRESS}/"+CREATE_VOLUME,
                             auth=auth,
                             json=volumeData, verify=TLS_VALUE)
    if response.status_code == 201:
        print("Volume Criado com sucesso ")
        return response.json()
    else:
        return {"response":response.status_code}
    
#getvolumes
def getVolumes(auth):
    response = requests.get(f"{ADRESS}/"+GET_VOLUMES, auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"response":response.status_code}
    
#get one volume
def getVolume(auth,name):
    response = requests.get(f"{ADRESS}/"+GET_VOLUME+"/"+str(name), auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"response":response.status_code}

#delete volume
def deleteVolume(auth,name):
    response = requests.delete(f"{ADRESS}/"+GET_VOLUME+"/"+str(name), auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 204:
        return response.json()
    else:
        return {"response":response.status_code}
    
#criar container se sincronizaçao
def createContainer(auth, container_detais, container_params):
    response = requests.post(f"{ADRESS}/"+CREATE_CONTAINER,auth=auth,
                             params=container_params,json = container_detais,
                             headers = {'Content-Type': 'application/json'},
                             stream=True,
                             verify=TLS_VALUE)
    if response.status_code == 201:
        #ver o progresso do pull
        print("Container Criado Com Sucesso")
        ip = (ADRESS.split(":")[1])[2:]
        return (startContainer(auth,container_params['name']),ip)
    else:
        print(response)
        return {"response":response.status_code}

#start container    
def startContainer(auth,container_name):
    response = requests.post(f"{ADRESS}/"+START_CONTAINER+"/"+container_name+"/start",auth=auth,
                             verify=TLS_VALUE)
    if response.status_code == 204:
        #ver o progresso do pull
        print("Iniciado Com Sucesso")
        return {"response":response.status_code}
    else:
        print(response)
        return {"response":response.status_code}