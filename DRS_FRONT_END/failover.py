
from DRS_WEB_APP.modulos.requests.eurekaservermethods import *
from DRS_WEB_APP.modulos.requests.sendRequests import *


WEB_PATH = '/web'

DELETE_STATUS_INTERVAL =  100

STATUS_SERVICE = {
    "name" : 'STATUS_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}

FAILOVER_SERVICE = {
    "name" : 'FAILOVER_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}
MANAGER_SERVICE = {
    "name" : 'MANAGER_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}


#apaga os status frequentemente para nao encher na base de dado
def deleteAllstatus():
    server = get_microservice_address_port(STATUS_SERVICE["name"])
    url = STATUS_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/status/deleteall"
    respo = sendDeleteRequest(json = None,adress=url,username=STATUS_SERVICE["username"], password=STATUS_SERVICE["password"])


#descobrir quais sao os servidores que estao down
def whoisdown():
	serverStatus = get_microservice_address_port(STATUS_SERVICE["name"])
	if(serverStatus['port']!=0):
		srs = get_microservice_data(STATUS_SERVICE["username"],STATUS_SERVICE["password"],serverStatus['address'],serverStatus['port'],STATUS_SERVICE["protocol"],path='drs/api/status/server/whoisdown')
	else:
		srs = None
	return  srs
#todos servidores
def allservs():
	serverStatus = get_microservice_address_port(STATUS_SERVICE["name"])
	if(serverStatus['port']!=0):
		srs = get_microservice_data(STATUS_SERVICE["username"],STATUS_SERVICE["password"],serverStatus['address'],serverStatus['port'],STATUS_SERVICE["protocol"],path='drs/api/status/server/getall')
	else:
		srs = None
	return  srs
#descobrir quais servidores estao up
def whoisup(allservs, downservs):
	upser  = []
	for s in allservs:
		if(s not in downservs):
			upser.append(s)
	return  upser


#buscar o failover de um servidor
def getServerFailover(id):
	server = get_microservice_address_port(FAILOVER_SERVICE["name"])
	if(server['port']!=0):
		srs = get_microservice_data(FAILOVER_SERVICE["username"],FAILOVER_SERVICE["password"],server['address'],server['port'],FAILOVER_SERVICE["protocol"],path='drs/api/failover/getbyserid/'+str(id))
	else:
		srs = None
	return  srs

#liga todos os servicos de um failover
def createServices(failover):
		respons = []
		for s in  failover["services"]:
			server = get_microservice_address_port(MANAGER_SERVICE["name"])
			url = MANAGER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/manager/service/create"
			respo = sendPostRequest(json = s,adress=url
				,username=MANAGER_SERVICE["username"], password=MANAGER_SERVICE["password"])
			respons.append(respo)
		return respons 

#apaga servicos , isso é necessário para poder apagar os serviços dos servidores quee estiverem up
def deleteServices(failover):
	respons = []
	for s in  failover["services"]:
		server = get_microservice_address_port(MANAGER_SERVICE["name"])
		url = MANAGER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/manager/services/delete/"+str(s["Name"])
		respo = sendDeleteRequest(json = None,adress=url,username=MANAGER_SERVICE["username"], password=MANAGER_SERVICE["password"])
		respons.append(respo)
	return respons




if __name__ == '__main__':
	#deleteAllstatus()
	#print(whoisdown())
	fo = getServerFailover("fsfsafsfsafasfas")
	#print(createServices(fo))
	#print(whoisup(allservs(),whoisdown()))
	deleteServices(fo)