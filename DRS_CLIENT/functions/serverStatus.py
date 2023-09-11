import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def returnstatus():
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    return {
        "cpu":cpu_usage,
        "memory":memory_usage,
        "disc":disk_usage
    }

def getMachineInfo():
    # Número de núcleos do processador
    num_cores = psutil.cpu_count(logical=False)  # Número de núcleos físicos
    num_cores_logicos = psutil.cpu_count(logical=True)  # Número de núcleos lógicos
    frequencia_atual = psutil.cpu_freq().current / 1000.0  # Frequência atual em GHz
    memoria = psutil.virtual_memory()
    #frequencia = round(frequencia_atual, 2)  # Arredonda para 2 casas decimais
    frequencia  = round(float(f"{frequencia_atual:.2f}"),2)
    memoria = round(memoria.total / (1024 ** 3), 2)
    return {
        "fcores":num_cores,
        "vcores":num_cores_logicos,
        "freq":frequencia,
        "men":memoria
    }

