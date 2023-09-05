#menu
from graph.toprint import *
import os
from functions.copy_to_remote import copyToRemote
from functions.sincronizeDir import sincronizeDirs
from functions.monitorMode import startMonitorMode
from functions.configs import showConfigs
import sys
import time

#chama a funcao 
def choose(option):
    if(option==1):
        return copyToRemote()
    elif(option==2):
        printMenuMoni()
        op =  int(input("WARS_MENU>MONITOR> "))
        if(op==1):
            return startMonitorMode()
        elif(op==2):
            printStatusInfo()
    elif(option==3):
        printMenuSinc()
        op =  int(input("WARS_MENU>SINCRONIZER> "))
        if(op==1):
           sec =  int(input("A sincronização deve ser feita a cada quantos secundos? "))
           return sincronizeDirs(sec)
        elif(op==2):
            printSincInfo()
    elif(option==4):
      showConfigs()
    else:
        return "Opção Invalida"

#funcao main
def main():
	printAAEElogo()
	while(True):
			printMenu()
			try:
				op =  int(input("WARS_MENU> "))
			except ValueError as e:
				print("Invalido")
				continue
			except KeyboardInterrupt as e:
				print("Bye")
				exit(0)
			os.system("clear")
			try:
				print(choose(op))
			except KeyboardInterrupt as e:
				os.system("clear")


if __name__ == '__main__':
	try:
		if(sys.argv[1]=="-monitorar" or sys.argv[1]=="-m" ):
			while True:
				startMonitorMode()
				time.sleep(1)
			
	except IndexError as e:
		main()
