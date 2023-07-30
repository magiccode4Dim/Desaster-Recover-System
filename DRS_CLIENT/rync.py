import subprocess
import time
import pexpect

def rsync_to_docker_volume(node_ip, ssh_port, ssh_username, ssh_password):
    server_A_path = '/home/narciso/mymysql/'
    docker_volume_path = f'/home/narciso/data/'

    rsync_command = f'rsync -avz --delete -e "ssh -p {ssh_port}" {server_A_path} {ssh_username}@{node_ip}:{docker_volume_path}'
    
    #subprocess.run(rsync_command, shell=True)
    child = pexpect.spawn(rsync_command)
    child.expect('password:')
    child.sendline(ssh_password)
    child.interact()
  
    

def main():
    node_ip = '192.168.122.190'
    ssh_port = 38283  # Substitua pelo número da porta SSH do nó do Docker Swarm
    ssh_username = 'narciso'
    ssh_password = '2001'


    while True:
        rsync_to_docker_volume(node_ip, ssh_port, ssh_username, ssh_password)
        print("Sincronização concluída.")
        time.sleep(10)  # Aguarda 5 minutos antes da próxima sincronização

if __name__ == "__main__":
        main()
  

