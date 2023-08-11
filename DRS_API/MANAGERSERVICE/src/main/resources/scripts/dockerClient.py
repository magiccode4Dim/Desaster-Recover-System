import requests
import json
import base64

#CLUSTER ADDRESS
ADDRS = ["192.168.122.71","192.168.122.248","192.168.122.127"] 

#REGISTRADORES 
REGISTRYS = ["192.168.122.10"]

auth_data = {
    "username": "narciso",
    "password": "2001"
}
auth_data_encoded = base64.b64encode(json.dumps(auth_data).encode()).decode()

ADRESS = 'https://192.168.122.71:7766'
USERNAME = 'narciso'
PASSWORD = '2001'
TLS_VALUE =  False
#URL
CREATE_NET = "networks/create"
GET_NETSWO = "networks"
GET_VOLUME = "volumes/"#<name>
CREATE_SERVICE = "services/create"
GET_SERVICE = "services"
SERVICE_UPDATE = "services" #{id}/update


#Retorna as Credencias de Autenticacao
def getAuth():
    # Configurar as informações de conexão
    username = USERNAME
    password = PASSWORD
    # Autenticar com o servidor proxy reverso Nginx
    auth = requests.auth.HTTPBasicAuth(username, password)
    return auth

#cria o  Network
def createNetwork(auth, netdata):
    response = requests.post(f"{ADRESS}/"+CREATE_NET,
                             auth=auth,
                             json=netdata, verify=TLS_VALUE)
    return {"response":response.status_code}
    
#getvolumes
def getNetworks(auth):
    response = requests.get(f"{ADRESS}/"+GET_NETSWO, auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"response":response.status_code}
    
#criar container se sincronizaçao
def createService(auth, data, header):
    response = requests.post(f"{ADRESS}/"+CREATE_SERVICE,auth=auth,
                             json = data,
                             headers = header,
                             verify=TLS_VALUE)
    if response.status_code == 201:
        #ver o progresso do pull
        print("Servico Criado Com Sucesso")
        #ip = (ADRESS.split(":")[1])[2:]
        #return (startContainer(auth,container_params['name']),ip)
        return {"response":response.status_code}
    else:
        print(response)
        return {"response":response.status_code}


#getvolumes
def getServices(auth):
    response = requests.get(f"{ADRESS}/"+GET_SERVICE, auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"response":response.status_code}

#get service by id
def getService(auth,id):
    response = requests.get(f"{ADRESS}/"+GET_SERVICE+"/"+str(id), auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        data = response.json()
        data["clusterips"] = ADDRS
        return data
    else:
        return {"response":response.status_code}

#service update
def serviceUpdate(auth,id,data,version):
    #print(f"{ADRESS}/{SERVICE_UPDATE}/{id}/update?version={version}")
    response = requests.post(f"{ADRESS}/{SERVICE_UPDATE}/{id}/update?version={version}",
        auth=auth,json=data, verify=TLS_VALUE)
    #print(response)
    return {"response":response.status_code}

#delete service
def serviceDelete(auth,id):
    #print(f"{ADRESS}/{SERVICE_UPDATE}/{id}/update?version={version}")
    response = requests.delete(f"{ADRESS}/{SERVICE_UPDATE}/{id}",
        auth=auth, verify=TLS_VALUE)
    #print(response)
    return {"response":response.status_code}