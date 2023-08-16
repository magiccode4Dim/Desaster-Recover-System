from flask import Flask, jsonify, request
from dockerClient import *
import json

app = Flask(__name__)

@app.route('/registry/list', methods=['GET'])
def getRess():
    return jsonify(getRegistrys())

@app.route('/containers/list', methods=['GET'])
def getCo():
    return jsonify(getContainers(getAuth()))
@app.route('/container/<id>', methods=['GET'])
def getCon(id):
    return jsonify(getContainerByID(getAuth(),id))
@app.route('/images/list', methods=['GET'])
def getIm():
    return jsonify(getImages(getAuth()))

@app.route('/images/pull', methods=['POST'])
def pullIm():
    image = (request.get_json()['json'])[0]
    #image =  dict(image)
    image = json.loads(image)
    print(image)
    
    return jsonify(pullImage(getAuth(),image))
@app.route('/container/create', methods=['POST','GET'])
def creatCon():
    cont = (request.get_json()['json'])[0]
    #image =  dict(image)
    cont = json.loads(cont)
    #print(cont)
    container_params = {
        "name" : cont["name"]
    }
    container_details = {
        "Image": cont["image"],
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
            "80/tcp": {},
            "443/tcp": {},
            "5000/tcp": {},
            "3306/tcp": {},
            "5432/tcp": {},
            "6000/tcp": {},
            "27017/tcp": {},
        },
        "HostConfig": {
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
                            "80/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0" #porta web
                                }
                            ],
                            "443/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0" #porta https
                                }
                            ],
                            "5000/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0"#default
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
                            "6000/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0"#default
                                }
                            ],
                            "27017/tcp": [
                                {
                                    "HostIp": "",
                                    "HostPort": "0"#default
                                }
                            ]
                    }
                
        }
    }
    
    print(container_details)
    
    
    #print(container_details)
    res = createContainer(getAuth(),container_detais=container_details,container_params=container_params)
    data =res[0]
    try:
        ssh_p = data["NetworkSettings"]["Ports"]["22/tcp"][0]["HostPort"]
        http_p = data["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
        https_p = data["NetworkSettings"]["Ports"]["443/tcp"][0]["HostPort"]
        mysql_p = data["NetworkSettings"]["Ports"]["3306/tcp"][0]["HostPort"]
        postgres_p = data["NetworkSettings"]["Ports"]["5432/tcp"][0]["HostPort"]
        default1_p = data["NetworkSettings"]["Ports"]["5000/tcp"][0]["HostPort"]
        default2_p = data["NetworkSettings"]["Ports"]["6000/tcp"][0]["HostPort"]
    except Exception as e:
        print(e)
        return jsonify(data)
    return jsonify({"ssh_p":ssh_p,
                    "http_p":http_p,
                    "https_p":https_p,
                    "mysql_p":mysql_p,
                    "postgres_p":postgres_p,
                    "default1_p":default1_p,
                    "default2_p":default2_p,
                    "ip":res[1]     
                    })
@app.route('/container/start/<id>', methods=['POST'])
def creatSta(id):
    return str(startContainer(getAuth(),id))
#delete container
@app.route('/container/delete/<id>', methods=['POST'])
def delConainer(id):
    return jsonify(deleteContainer(getAuth(),id))

@app.route('/container/commit', methods=['POST'])
def commitContainerAsIMa():
    containerdata = (request.get_json()['json'])[0]
    containerdata = json.loads(containerdata)
    print(containerdata)
    image_name = {
        'repo':containerdata['nome'],
        'tag':containerdata['tag']
        }
    container_config = {"container":containerdata['containerID']}
    return jsonify(commitContainer(getAuth(),image_name=image_name, container_id=container_config))
    
#push image to registry
@app.route('/image/push', methods=['POST'])
def pushImagetoRegistry():
    data = (request.get_json()['json'])[0]
    data = json.loads(data)
    headers = {
        "X-Registry-Auth": auth_data_encoded
    }
    return jsonify(pushImage(getAuth(),data["nome"],headers))
    
    



# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
