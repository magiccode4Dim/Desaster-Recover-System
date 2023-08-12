from failover import *
import time
import threading

TIME_TO_RECOVER = 2
TIME_TO_DELETE = 2
DELETE_STATUS_INTERVAL =  50


#cria os servicos dos servidores que estao offline
def createRecover():
	while  True:
		#pega os que estao offline
		time.sleep(TIME_TO_RECOVER)
		downservers =  whoisdown()
		for s in downservers:
			#pega o faiover do servidor que esta down
			fo = getServerFailover(s["id"])
			if(fo==None):
				continue
			#cria os servicos dele
			createServices(fo)

#apaga os servicos dos servidores que ja estao online
def deleteRecover():
	while  True:
		#pega os que estao online
		time.sleep(TIME_TO_DELETE)
		upservers =  whoisup(allservs(),whoisdown())
		for s in upservers:
			#pega o faiover do servidor que esta down
			fo = getServerFailover(s["id"])
			if(fo==None):
				continue
			#apaga os servicos dele
			deleteServices(fo)


#apaga os status frequentemente para deixar a base de dados limpa
def deleteStatus():
	while  True:
		time.sleep(DELETE_STATUS_INTERVAL)
		deleteAllstatus()



if __name__ == '__main__':
	recover = threading.Thread(target=createRecover)
	recover.start()
	deleterec = threading.Thread(target=deleteRecover)
	deleterec.start()
	deletes = threading.Thread(target=deleteStatus)
	deletes.start()