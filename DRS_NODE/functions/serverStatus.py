import psutil


old_upload = 0
old_download = 0

def get_current_network_usage():
    network_stats = psutil.net_io_counters(pernic=True)
    upload_bytes = 0
    download_bytes = 0

    for interface, stats in network_stats.items():
        upload_bytes += stats.bytes_sent
        download_bytes += stats.bytes_recv

    upload_mbps = upload_bytes / (1024 * 1024)
    download_mbps = download_bytes  / (1024 * 1024)

    return [upload_mbps, download_mbps]


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
    netdata = get_current_network_usage()
    return {
        "cpu":cpu_usage,
        "memory":memory_usage,
        "disc":disk_usage,
        "totalup":round(netdata[0],2),
        "totaldown":round(netdata[1],2)        
    }

#GET PC INFO
def getMachineInfo():
    # Número de núcleos do processador
    num_cores = psutil.cpu_count(logical=False)  # Número de núcleos físicos
    num_cores_logicos = psutil.cpu_count(logical=True)  # Número de núcleos lógicos
    frequencia_atual = psutil.cpu_freq().current / 1000.0  # Frequência atual em GHz
    memoria = psutil.virtual_memory()
    frequencia = round(frequencia_atual, 2)  # Arredonda para 2 casas decimais
    memoria = round(memoria.total / (1024 ** 3), 2)
    return {
        "fcores":num_cores,
        "vcores":num_cores_logicos,
        "freq":frequencia,
        "men":memoria
    }