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

## Sistemas Semelhantes 
O DRS é  semelhante  aos seguintes sistemas:
* Amazon Web Services (AWS) Disaster Recovery;
* Microsoft Azure Site Recovery;
* Google Cloud Platform (GCP) Site-to-Site Disaster Recovery;
* VMware Site Recovery Manager.

Quanto as diferenças  mais marcantes  entre o DRS e as plataformas  acima citadas,primeiro, DRS é  opensource, segundo, utiliza o Docker como base para armazenar a replica da aplicação  web, ao invés  de utilizar uma máquina  virtual.

## I. Configuração da Infraestrutura
As configurações  da infraestrutura, assim como toda base teórica  do projeto, estão  presentes no PDF ***drs.pdf***

## II. Instalação do DRS

Requisitos mínimos de Sistema:
* OS - Ubuntu >= 22.04 LTS ou Debian >= 11 (testado no debian 12);
* CPU - 2.5 Ghz × 4 cores (ou mais);
* RAM - 16 GB ou mais.

Dependências:
* Docker 24.0.2 ou superior;
* Python >= 3.10;
* Java >= 8.0
* maven >= 3.6
* mongo >= 7.0
* mysql >= 8.0

**Instalação**
1. Configure a infraestrutura de acordo com o ficheiro ***drs.pdf*** (os arquivos pdf, encontram-se na raiz do repositório).
2. Instale as dependências acima listadas.
3. Inicialize os dois servidores de base de dados (mysql e mongo), crie uma base de dados em cada um dos servidores (guarde o nome delas), e certifique-se se possui um IP, PORTA e um utilizador válido para aceder a base de dados (**Nota**: se quiser pode rodar os docker-compose.yml presentes no directorio /mongo_and_mysql/ que terá duas base de dados já prontas).
4. Clone o Projecto
5. Altere os Arquivos de configuração:
   * No directorio raiz,mude as credências dos microserviços e base de dados presentes no arquivo ***docker-compose.yml***, de acordo com os dados da sua infraestrutura.
     
   * Mude os valores no ficheiro ***./DRS_WEB_APP/configs/config.json*** de acordo com as credências dos microserviços inseridas no docker-compose.yml. No mesmo ficheiro, altere também,os valores de ***"CLUSTER_NODES"*** e ***"EUREKASERVERS"***. No "CLUSTER_NODES" insira os nomes dos nós do cluster swarm configurado no Passo 1. No "EUREKASERVERS" insira o IP(s) do seu(s) servidor(es) eureka, insirá o endereço e a porta que permita chegar ao serviço ***eureka-server*** presente no docker-compose.yml.
     
   * Mude os arquivos de configuração nos microserviços. Alguns Microserviços, nos directorios ***DRS_API/<microservice_name>/src/main/resources/scripts***, contém o ficheiro ***config.json***. Esse ficheiro também precisa ser modificado de acordo com a infraestrutura.
         * ***"CLUSTERADDRESS"*** representa os endereços dos nós do cluster;
         * ***"MASTERADRESS"*** é o IP e porta do Nó MASTER;
         * ***"DOCKERAPI_USERNAME"*** e ***DOCKERAPI_PASSWORD*** são as credências de acesso para a API docker configurada no nó MASTER;
         * ***"auth_data_json"*** são as mesmas credências do DockerAPI em uma notação diferente;
         * ***"REGISTRYS"*** é o endereço servidor onde consta o docker registry;
         * ***"TLS_VALUE"*** false se o https não estiver habilitado no DockerAPI. 
   
6. Compile a API e os seus microserviços:
* Entre no directório DRS_API, e para cada subdirectorio execute:
```bash
maven clean
maven install
maven package
```
7. Contrua as imagens presentes nos subdirectorios de /Docker/ (Compile de acordo com as orientações escritas em forma de comentário nos Dockerfile's)
   * No directorio /Docker/Javacompython3 execute
```bash
sudo docker build -t openjdk8-and-python3 .
```
8. Com internet ligada, no directorio raiz do projecto, execute:
```bash
sudo docker compose up -d
```
![Screenshot from 2024-08-03 21-17-11](https://github.com/user-attachments/assets/3a09a148-d77d-4b5a-9202-6faab1366e71)

9. Crie um superuser
```bash
sudo docker exec -it desaster-recover-system-aaeewars-frontend-1 python manage.py createsuperuser
```
![Screenshot from 2024-08-03 19-16-33](https://github.com/user-attachments/assets/f7367cfc-4f9e-498d-b4fe-a8da5d791d6c)

10. Acesso o Sistema  em http://localhost:8000, entre com as credências  acima criadas; Desça até ao final da página  da dashboard, e siga as instruções  para instalar o DRS-agente nos servidores  da infraestrutura. 

11. Registre os Nós  da infraestrutura no DRS. Vá  até  **Monitoramento->Adicionar Servidor**,  e adiciona  os nós da infraestrutura com os mesmos nomes presentes no atributo ***"CLUSTER_NODES"*** do arquivo ***./DRS_WEB_APP/configs/config.json***.

**NOTA**: O DRS AINDA NÃO ESTÁ PRONTO PARA SER UTILIZADO EM PRODUÇÃO, POR ENQUANTO É APENAS UMA PROVA DE CONCEITO QUE PODE SER INSTALADA E TESTADA EM AMBIENTE LOCAL.
## SCREENSHOTS
![Screenshot from 2024-08-03 21-32-48](https://github.com/user-attachments/assets/861104e7-9d24-4be8-a013-7b0538c891a4)
![Screenshot from 2024-08-03 21-34-34](https://github.com/user-attachments/assets/ccbc4a73-fd5b-493a-821c-a0305b5a7034)
![Screenshot from 2024-08-03 21-35-14](https://github.com/user-attachments/assets/f9782a1f-8cbb-4478-a7ff-f9786febe794)
![Screenshot from 2024-08-03 21-35-26](https://github.com/user-attachments/assets/db8f32b4-9fb8-4b78-999f-7653897e3338)

## Simulação do DRS
De modo a fazer a prova de conceito, o DRS foi utilizado para replicar uma aplicação web que se encontrava em uma infraestrutura on-promise. A aplicação web é denominada crudphp e ela foi desenvolvida em pHp e utiliza Postgres como base de dados. Após a replicação e configuração dos demais componentes, foi simulada uma falha no servidor da aplicação web que o desligou, com o objetivo de ver o sistema de failover do DRS. O DRS por sua vez, através  dos mecanismos programados, detectou a falha e logo iniciou a aplicação web de failover.Todos os screenshots sobre as simulações, estão descritas no arquivo ***simulacao.pdf***.

**BY narcisopascoal97@gmail.com**

