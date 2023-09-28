from failover import *
import time
import threading
import os

TIME_TO_RECOVER = int(os.environ.get('TIME_TO_RECOVER')) #2 #tempo necessario para criar um servico assim que um determinado servidor caar
TIME_TO_DELETE =  int(os.environ.get('TIME_TO_DELETE')) #2 #tem necessario para eliminar o servico assim que o servidor levanta
DELETE_STATUS_INTERVAL = int(os.environ.get('DELETE_STATUS_INTERVAL'))  #60 #tempo necessario para apagar o status de todos os servidor na base de dados


#cria os servicos dos servidores que estao offline
def createRecover():
	while  True:
		#pega os que estao offline
		time.sleep(TIME_TO_RECOVER)
		downservers =  whoisdown()
		#print(downservers)
		if(len(downservers)==0):
			continue
		for s in downservers:
			#pega o faiover do servidor que esta down
			fo = getServerFailover(s["id"])
			#print(fo)
			if(fo["services"]==None):
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
			if(fo["services"]==None):
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
