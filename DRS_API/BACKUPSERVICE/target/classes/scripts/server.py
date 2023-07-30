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



# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True,port=5001)
