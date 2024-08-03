# -*- coding: utf-8 -*-
import paramiko

# Configurar as informações de conexão
host = '192.168.122.190'  # Endereço IP do servidor remoto
port = 22  # Porta SSH (padrão: 22)
username = 'narciso'
password = '2001'
remote_file = '/home/narciso/tlscerts/nginx-certificate.crt'  # Caminho do arquivo remoto
local_file = './certificates/runner.crt'  # Caminho onde o arquivo será salvo localmente

# Criar uma instância do cliente SSH
client = paramiko.SSHClient()

# Configurar a política de aceitação do host (opcional)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Conectar ao servidor remoto
client.connect(hostname=host, port=port, username=username, password=password)

# Abrir um canal SFTP
sftp = client.open_sftp()

# Baixar o arquivo remoto
sftp.get(remote_file, local_file)

# Fechar a conexão SFTP e SSH
sftp.close()
client.close()

print(f'O arquivo foi baixado com sucesso em: {local_file}')
