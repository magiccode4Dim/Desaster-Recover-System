#!/bin/bash

# Verificar se o utilizador é um root
if [ "$(id -u)" != "0" ]; then
    echo "Este script deve ser executado como superusuário (root)."
    exit 1
fi

# Verificando se o caminho do script foi passado como argumento
if [ $# -ne 1 ]; then
    echo "Uso: $0 /caminho/do/script/DRS_NODE/aaee_node.py"
    exit 1
fi

caminho_script="$1"

# Criando o arquivo para o serviço do script
cat <<EOF > /etc/systemd/system/aaeewarsnode.service
[Unit]
Description=Monitoramento  para o Sistema de replicação de aplicações web

[Service]
ExecStart=/usr/bin/python3  $caminho_script
WorkingDirectory=$(dirname "$caminho_script")
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Recarregar o sistema para que possa reconhecer o novo serviço
systemctl daemon-reload

# Habilitar o servico
systemctl enable aaeewarsnode.service

# Iniciar o servico
systemctl start aaeewarsnode.service

echo "Configuração concluída :). Para ver o status do serviço digite o comando: systemctl status aaeewarsnode.service "
