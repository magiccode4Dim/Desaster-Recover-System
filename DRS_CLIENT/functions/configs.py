from .json_Save import *

def showConfigs():
	try:
		monitorConfig = getJSON("./functions/data/monitorconfig.json")
		sincConfig = getJSON("./functions/data/sinc.json")
		print("==MONITOR CONFIG==")
		print(monitorConfig)
		print("==SINCRONIZER CONFIG==")
		print(sincConfig)
	except Exception as e:
		return f"<ERROR: {str(e)}>"