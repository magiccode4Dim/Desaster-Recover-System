

def printAAEElogo():
	print("\n")
	print("  AAAAAA   AAAAAA   EEEEEEEE  EEEEEEEE")
	print(" AA    AA AA    AA EE       EE      ")
	print(" AA    AA AA    AA EE       EE      ")
	print(" AAAAAAAA AAAAAAAA EEEEEEE     EEEEE   ")
	print(" AA    AA AA    AA EE       EE      ")
	print(" AA    AA AA    AA EE       EE      ")
	print(" AA    AA AA    AA EEEEEEEE  EEEEEEEE")
	print("\n")


def printMenu():
	menuop = [
		"COPIAR FICHEIROS PARA SERVIDOR REMOTO",
		"MODO DE MONITORAMENTO",
		"MODO DE SINCRONIZAÇÃO",
		"VER CONFIGURAÇÕES"
	]
	id = 1
	for op in menuop:
		print(f"[{id}] - {op}")
		id+=1

def printStatusInfo():
    print("É POSSIVEL FAZER COM QUE O MONITORAMENTO DO SERVIDOR SEJA FEITO NO BACKGROUND.")
    print("PARA QUE ISSO SEJA POSSIVEL, PRIMEIRO DEVE TER AS CONFIGURAÇÕES EM ORDEM NO ARQUIVO")
    print("./functions/data/monitorconfig.json de SEGUIDA DEVE EXECUTAR OS COMANDOS: ..  ")
    
def printMenuMoni():
	menuop = [
		"MONITORAR INSTANCIA",
		"INFO"
	]
	id = 1
	for op in menuop:
		print(f"[{id}] - {op}")
		id+=1
 
def printSincInfo():
    print("É POSSIVEL FAZER COM A SINCRONIZAÇÃO DE UM DIRECTORIO SEJA FEITA NO BACKGROUND.")
    print("PARA QUE ISSO SEJA POSSIVEL, PRIMEIRO DEVE TER AS CONFIGURAÇÕES EM ORDEM NO ARQUIVO")
    print("./functions/data/sinc.json de SEGUIDA DEVE EXECUTAR OS COMANDOS: ..  ")
    
 
def printMenuSinc():
	menuop = [
		"SINCRONIZAR DIRECTORIOS",
		"INFO"
	]
	id = 1
	for op in menuop:
		print(f"[{id}] - {op}")
		id+=1
 