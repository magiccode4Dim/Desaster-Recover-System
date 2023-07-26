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
GET_CONTAINERS = "containers/json"
GET_IMAGES = "images/json"
PULL_IMAGE  = "images/create"
CREATE_CONTAINER = "containers/create"
START_CONTAINER = "containers" #<ID>/start
#/v1.41/containers/{id}
DELETE_CONTAINER = "containers" #<ID>/
PAUSE_CONTAINER  = "containers" #<ID>/pause
STOP_CONTAINER = "containers" #<ID>/stop
PRUNE_CONTAINER = "containers/prune"
GET_CONTAINER = "containers"  #{id}/json


#IMAGE
IMAGE_DELETE = "images"#<ID>
BUild_DELETE = "build/prune"
COMMIT_CONTAINER = "commit"
RENAME_IMAGE ="images"#<ID>/tag
PUSH_IMAGE = "images"#<ID>/push


#Retorna as Credencias de Autenticacao
def getAuth():
    # Configurar as informações de conexão
    username = USERNAME
    password = PASSWORD
    # Autenticar com o servidor proxy reverso Nginx
    auth = requests.auth.HTTPBasicAuth(username, password)
    return auth
#Retorna a lista de containers
def getContainers(auth):
    response = requests.get(f"{ADRESS}/"+GET_CONTAINERS, auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"responde":response.status_code}
#retorna um container com um id
def getContainerByID(auth,id):
    response = requests.get(f"{ADRESS}/"+GET_CONTAINER+"/"+str(id)+"/json", auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        res = response.json()
        res["access"] = (ADRESS.split(":")[1])[2:]
        return res
    else:
        return (None,response.status_code)
#retorna a lista de images
def getImages(auth):
    response = requests.get(f"{ADRESS}/"+GET_IMAGES, auth=auth, verify=TLS_VALUE)
    # Verificar o status da resposta
    if response.status_code == 200:
        return response.json()
    else:
        return (None,response.status_code)
#faz o pull de uma imagem
def pullImage(auth, image):
    response = requests.post(f"{ADRESS}/"+PULL_IMAGE,auth=auth, params=image, stream=True, verify=TLS_VALUE)
    if response.status_code == 200:
        #ver o progresso do pull
        for chunk in response.iter_content(chunk_size=4096):
            print(chunk)  # Aqui você pode processar os dados do "pull" conforme necessário
        return {"response":200}
    else:
        return {"response":response.status_code}
#apaga uma imagem
def removeImage(auth,image_id):
    response = requests.delete(f"{ADRESS}/"+IMAGE_DELETE+"/"+image_id,auth=auth, verify=TLS_VALUE)
    if response.status_code == 200:
        print("Imagem Apagada com Sucesso")
        pruneBuildCache(auth)
    else:
        return (None,response.status_code)
#remove buildCash
def pruneBuildCache(auth):
    response = requests.post(f"{ADRESS}/"+BUild_DELETE,auth=auth, verify=TLS_VALUE)
    if response.status_code == 200:
        print("Arquivos resultantes de compilacao APgados")
    else:
        return (None,response.status_code)

#cria um container
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
#dar start ao container
def startContainer(auth,container_name):
    response = requests.post(f"{ADRESS}/"+START_CONTAINER+"/"+container_name+"/start",auth=auth,
                             verify=TLS_VALUE)
    if response.status_code == 204:
        #ver o progresso do pull
        print("Iniciado Com Sucesso")
        return getContainerByID(auth,container_name)
    else:
        print(response)
        return {"response":response.status_code}
#apagar um container
def deleteContainer(auth,container_name):
    pauseContainer(auth,container_name)
    stopContainer(auth,container_name)
    response = requests.delete(f"{ADRESS}/"+DELETE_CONTAINER+"/"+container_name,auth=auth,
                             verify=TLS_VALUE)
    pruneContainers(auth)
    if response.status_code == 204:
        #ver o progresso do pull
        print("Apagado Com Sucesso")
        
    else:
        print(response)
        return (None,response.status_code)
#pausar um container
def pauseContainer(auth,container_name):
    response = requests.post(f"{ADRESS}/"+PAUSE_CONTAINER+"/"+container_name+"/pause",auth=auth,
                             verify=TLS_VALUE)
    if response.status_code == 204:
        #ver o progresso do pull
        print("Parado Com Sucesso")
    else:
        print(response)
        return (None,response.status_code)
#fazer stop
def stopContainer(auth,container_name):
    response = requests.post(f"{ADRESS}/"+STOP_CONTAINER+"/"+container_name+"/stop",auth=auth,
                             verify=TLS_VALUE)
    if response.status_code == 204:
        #ver o progresso do pull
        print("Parado Com Sucesso")
    else:
        print(response)
        return (None,response.status_code)
#limpar os containers pausados
def pruneContainers(auth):
    response = requests.post(f"{ADRESS}/"+PRUNE_CONTAINER,auth=auth,
                             verify=TLS_VALUE)
    if response.status_code == 202:
        #ver o progresso do pull
        print("lIMPO")
    else:
        print(response)
        return (None,response.status_code)

#salvar o container como imagem
def commitContainer(auth, image_name, container_id):
    response = requests.post(f"{ADRESS}/"+COMMIT_CONTAINER,auth=auth,
                             params=container_id,
                             verify=TLS_VALUE)
    if response.status_code == 201:
        #ver o progresso do pull
        print("Container Salvo")
        response_json = response.json()
        container_id = response_json['Id']
        print(container_id)
        id = (container_id[7:])[:12]
        return renameImage(auth,id,newName=image_name)
    else:
        print(response)
        return (None,response.status_code)
#renomeia o container
def renameImage(auth, id, newName):
    url = f'{ADRESS}/images/{id}/tag?repo={newName["repo"]}&tag={newName["tag"]}'
    response = requests.post(url,auth=auth,verify=TLS_VALUE)
    if response.status_code == 201:
        #ver o progresso do pull
        print("Novo Nome Atribuido")
        return {"response":201}
    else:
        print(response)
        return {"response":response.status_code}
def pushImage(auth,name,header):
    response = requests.post(f"{ADRESS}/"+PUSH_IMAGE+"/"+name+"/push",auth=auth,
                             headers=header,
                             verify=TLS_VALUE)
    if response.status_code == 200:
        #ver o progresso do pull
        print("Push Bem Sucedido")
        return {"response":201}
    else:
        print(response)
        return {"response":response.status_code}
#get registrys
def getRegistrys():
    return REGISTRYS
    
    

if __name__ == "__main__":
    """
    image = {
        'fromImage':  'alpine',
        'tag':'latest'
    }
    
    print(pullImage(auth=getAuth(),image=image))
    
    """
    #myubuntuNany
    """
    con =  getContainers(getAuth())
    for c in con:
        print(c)
        print("=========")"""
    
    """
    container_details = {
        'Image': 'nginx',
        'HostConfig': {
            'PortBindings': {
                '80/tcp': [
                    {
                        'HostPort': '8089'
                    }
                ]
            }
        }
    }"""
    
    #create container
    
    
    container_params = {
        "name" : "myubuntuNany"
    }
    container_details = {
        "Image": "ubuntussh",
        "Hostname":container_params["name"],
        "Detach": True,
        "PublishAllPorts": False,
        "PortBindings": {
            "22/tcp": [
            {
                "HostIp": "",
                "HostPort": "2223"
            }
            ]
                },
                "Cmd": [
                    "bash",
                    "-c",
                     "useradd -m -s /bin/bash narciso && echo 'narciso:2001' | chpasswd && usermod -aG sudo narciso && /usr/sbin/sshd -D"
                ]
        }


    
    #startContainer(getAuth(),'myubuntu')
    
    print(createContainer(getAuth(),container_detais=container_details,container_params=container_params))


#REMOVE container

#deleteContainer(getAuth(),container_name=container_params["name"])

#REMOVE IMAGE
#removeImage(getAuth(),"alpine")

#commit  container as imagem

#sudo docker login https://192.168.122.10    

"""
container_id = container_params["name"],  # Substitua pelo ID ou nome do seu contêiner
repository = '192.168.122.10/ubuntucompython'  # Substitua pelo nome do seu repositório e imagem
tag = 'latest'  # Substitua pela tag desejada para a imagem
author = 'Narciso'  # Substitua pelo 
    
image_name = {
        'repo':repository,
        'tag':tag
}

container_config = {"container":container_id}
    

#print(commitContainer(getAuth(),image_name=image_name, container_id=container_config))

#Push image
headers = {
    "X-Registry-Auth": auth_data_encoded
}
print(pushImage(getAuth(),repository,headers))"""