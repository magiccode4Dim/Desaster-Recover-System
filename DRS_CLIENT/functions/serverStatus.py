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



