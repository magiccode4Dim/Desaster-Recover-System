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



