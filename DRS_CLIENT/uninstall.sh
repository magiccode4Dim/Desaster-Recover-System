#!/bin/bash

# Verificar se o script esta sendo executado como super administrador
if [ "$(id -u)" != "0" ]; then
    echo "Este script deve ser executado como superusuário (root)."
    exit 1
fi

# Destativar o servico
systemctl stop aaeewarsmonitor.service
systemctl disable aaeewarsmonitor.service

# Removendo o serviço
rm /etc/systemd/system/aaeewarsmonitor.service

# Recarregando as alterações
systemctl daemon-reload

echo "Desinstalação concluída. O serviço de Monitoramento aaeewarsmonitor foi removido do sistema."
