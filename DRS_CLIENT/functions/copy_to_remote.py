from .commun import getSSHcred
import subprocess

def copyToRemote():
    try:
        localpah =  input("Local Path: ")
        remotepah =  input("Remote Path: ")
        sshcreds =  getSSHcred()
        rsync_command = f'rsync -avz -e "ssh -p {sshcreds["port"]}" {localpah} {sshcreds["user"]}@{sshcreds["ip"]}:{remotepah}'
        subprocess.run(rsync_command, shell=True)
        return "<SUCCESS>"
    except Exception as e:
        return f"<ERROR: {str(e)}>"
    
    
    
    