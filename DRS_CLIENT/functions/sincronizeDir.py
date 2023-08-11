from .commun import getSSHcred
import subprocess
import subprocess
import time
import pexpect


def sincronize(sshcreds,localpah,remotepah,ssh_password):
    rsync_command = f'rsync -avz --delete -e "ssh -p {sshcreds["port"]}" {localpah} {sshcreds["user"]}@{sshcreds["ip"]}:{remotepah}'
    child = pexpect.spawn(rsync_command)
    child.expect('password:')
    child.sendline(ssh_password)
    child.interact()
  

def sincronizeDirs(secunds):
    try:
        localpah =  input("Local Path: ")
        remotepah =  input("Remote Path: ")
        sshcreds =  getSSHcred()
        rsync_command = f'rsync -avz -e "ssh -p {sshcreds["port"]}" {localpah} {sshcreds["user"]}@{sshcreds["ip"]}:{remotepah}'
        subprocess.run(rsync_command, shell=True)
        print("Introduza a sua Password do Servidor remoto novamente")
        password  = input("SSH_password: ")
        while True:
            sincronize(sshcreds, localpah, remotepah, password)
            print("[#]SINCRONIZAÇÃO FEITA")
            time.sleep(secunds)  # Aguarda 5 minutos antes da próxima sincronização
    except Exception as e:
        return f"<ERROR: {str(e)}>"