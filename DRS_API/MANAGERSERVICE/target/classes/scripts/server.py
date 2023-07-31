from flask import Flask, jsonify, request
from dockerClient import *
import json

app = Flask(__name__)

#GET volumes
@app.route('/networks/list', methods=['GET'])
def getVols():
    return jsonify(getNetworks(getAuth()))

#get services
@app.route('/services/list', methods=['GET'])
def getVsER():
    return jsonify(getServices(getAuth()))

#create volume
@app.route('/network/create', methods=['POST'])
def createNewVolume():
    vol = (request.get_json()['json'])[0]
    vol = json.loads(vol)
    vol_details = {
    "Name": vol["nome"],
    "Driver": "overlay",
    "IPAM": {
        "Config": [
            {
                "Subnet": vol["rede"],
                "Gateway": vol["gateway"]
            }
        ]
    }
}
    print(vol_details)
    return jsonify(createNetwork(getAuth(),vol_details))

#create service
@app.route('/service/create', methods=['POST'])
def createServ():
    data = (request.get_json()['json'])[0]
    data = json.loads(data)
    headers = {
        "X-Registry-Auth": auth_data_encoded
    }
    return jsonify(createService(getAuth(),data,headers))

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True,port=5002)
