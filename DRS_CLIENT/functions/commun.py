def getSSHcred():
    sshserver = input("SSH_IP : ")
    sshuser = input("SSH_USER : ")
    sshport = input("SSH_PORT : ")
    return {
        "ip":sshserver,
        "user":sshuser,
        "port":sshport
    }