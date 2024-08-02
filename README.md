# DRS - Desaster Recover System
* web aplication replicator
* DDoS defence System
* high availability
* Data replication
* Load Balancer
![](https://github.com/magiccode4Dim/DRS/blob/main/Working.gif)

## Para quê o DRS foi criado?
O DRS foi criado para resolver o problema  da falta de Alta disponibilidade, em aplicações  web implantadas em infraestruturas On-premise. 
Empresas  que mantêm  as suas aplicações  web em infraestruturas  locais, tem a dificuldade  de assegurar  a disponibilidade  das mesmas em situações adversas como corte de corrente eléctrica,  desastres naturais, ataques DDoS, falhar humanas etc.O DRS resolve  o problema porque permite que uma cópia  a nível  dos dados e a nível das aplicações web seja armazenada fora da infraestrutura  local, de tal modo que está, passa a ser ligada somente quando existe indisponibilidade da infraestrutura local (on -promise).

## Descrição do Sistema
* O DRS é um sistema desenvolvido para assegurar a alta  disponibilidade. 
* Permite configurar  uma cópia  de uma determinada aplicação  web em clusteres de servidores. 
* A cópia configurada, será acionada automaticamente,somente  quando  a aplicação  web principal estiver indisponível.
* O DRS tem como base o Docker Engine. Neste sentido, a cópia é configurada em um container Docker através  de um Dockerfile.
* O DRS monitora os servidores que hospedam as aplicações web, através  de uma aplicação  Agente que deve ser previamente  instalada no servidor  de Destino.
* A Cópia  dos dados é  assegurada  por um sistema de replicação  de base de dados.

## Instalação  e Configuração

O DRS mantêm  as cópias  das aplicações web em um cluster de servidores, para assegurar a alta disponibilidade e maior performance. Assim sendo,  o primeiro  passo é  configurar  o Cluster de forma adequada para o DRS.

**Configuração do docker swarm,  docker registry e docker API**:
As configurações  da infraestrutura, estão  presentes no PDF ***infrastrutura.pdf***
