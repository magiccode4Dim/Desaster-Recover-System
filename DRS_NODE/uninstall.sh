#!/bin/bash

# Verificar se o script esta sendo executado como super administrador
if [ "$(id -u)" != "0" ]; then
    echo "Este script deve ser executado como superusuário (root)."
    exit 1
fi

# Destativar o servico
systemctl stop aaeewarsnode.service
systemctl disable aaeewarsnode.service

# Removendo o serviço
rm /etc/systemd/system/aaeewarsnode.service

# Recarregando as alterações
systemctl daemon-reload

echo "Desinstalação concluída. O serviço de Monitoramento aaeewarsnode foi removido do sistema."
