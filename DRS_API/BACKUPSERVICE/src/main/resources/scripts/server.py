from flask import Flask, jsonify, request
from dockerClient import *
import json

app = Flask(__name__)

#GET volumes
@app.route('/volumes/list', methods=['GET'])
def getVols():
    return jsonify(getVolumes(getAuth()))

#get one volume
@app.route('/volumes/get/<volumename>', methods=['GET'])
def getVol(volumename):
    return jsonify(getVolume(getAuth(),volumename))

#create volume
@app.route('/volumes/create', methods=['POST'])
def createNewVolume():
    vol = (request.get_json()['json'])[0]
    vol = json.loads(vol)
    vol_details = {
        "Name": vol["nome"],
        "Driver": "local",
        "Labels": 
        {
            "com.example.some-label": vol["label"],
            "com.example.some-other-label": vol["label"]
        }
    }
    return jsonify(createVolume(getAuth(),vol_details))


#create container de sincronizacao
@app.route('/containersinc/create', methods=['POST','GET'])
def creatCon():
    cont = (request.get_json()['json'])[0]
    #image =  dict(image)
    cont = json.loads(cont)
    #print(cont)
    container_params = {
        "name" : cont["name"]
    }
    container_details = {
        "Image": "ubuntussh", #se é um container de sincronizaçao entao a imagem é essa
        "Hostname":cont["hostname"],
        "Detach": True,
        "PublishAllPorts": False,
        "Env": 
	[

	    f"NEW_USER={cont['username']}",
	    f"NEW_USER_PASSWORD={cont['password']}"

	],
        "ExposedPorts": { #deixar as portas mapeadas mesmo que o servico nao esteja a escuta
            "22/tcp": {},
        },
        "HostConfig": {
                    "Binds": [
                        f"{cont['volume']}:/home/{cont['username']}/data"
                    ],
                    "RestartPolicy": {
                        "Name": "always"
                    },
                    "PortBindings": { #mapear as portas quando o servico estiver a escuta},
                            "22/tcp": [
                            {
                                "HostIp": "",
                                "HostPort": "0" #permitir que o docker escolha a porta
                            }
                            ]
                    }
                
        }
    }
    
    print(container_details)
    
    
    #print(container_details)
    res = createContainer(getAuth(),container_detais=container_details,container_params=container_params)
    data =res[0]
    return jsonify(data)

#crate container database
@app.route('/containerdb/create', methods=['POST','GET'])
def creatConDB():
    cont = (request.get_json()['json'])[0]
    #image =  dict(image)
    cont = json.loads(cont)
    #print(cont)
    container_params = {
        "name" : cont["name"]
    }
    container_details = {
        "Image": cont["dbimage"], #se é um container de sincronizaçao entao a imagem é essa
        "Detach": True,
        "Hostname":cont["hostname"],
        "PublishAllPorts": False,
        "Cmd": [
                    "bash",
                    "-c",
                    f"useradd -m -s /bin/bash {cont['username']} && echo '{cont['username']}:{cont['password']}' | chpasswd && usermod -aG sudo {cont['username']} && /usr/sbin/sshd -D"
                ],
        "ExposedPorts": { #deixar as portas mapeadas mesmo que o servico nao esteja a escuta
            "22/tcp": {},
            "3306/tcp": {},
            "5432/tcp": {},
            "27017/tcp": {},
        },
        "HostConfig": {
                    "Binds": [
                        f"{cont['volume']}:{cont['dir']}"
                    ],
                    "RestartPolicy": {
                        "Name": "always"
                    },
                    "PortBindings": { #mapear as portas quando o servico estiver a escuta},
                            "22/tcp": [
                            {
                                "HostIp": "",
                                "HostPort": "0" #permitir que o docker escolha a porta
                            }
                            ],
                            "3306/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0"#mysql
                                }
                            ],
                            "5432/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0"#postgres
                                }
                            ],
                            "27017/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0"#postgres
                                }
                            ],
                    }
                
        }
    }
    
    print(container_details)
    
    #print(container_details)
    res = createContainer(getAuth(),container_detais=container_details,container_params=container_params)
    data =res[0]
    
    comannd = {
        "AttachStdin": True,
        "AttachStdout": True,
        "AttachStderr": True,
        "Tty": True,
        "Cmd": ["chown", "-R", "1000:1000", f"{cont['dir']}"],
    }
    #if (data["response"]==204):
    #    data = execContainer(getAuth(),cont["name"],comannd)
    
    return jsonify(data)


# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True,port=5001)
