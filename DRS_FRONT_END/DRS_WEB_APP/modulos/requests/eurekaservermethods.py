import requests
import base64
import random

EUREKA_SERVERS = ['localhost:8761']





#retorna o endereço e a porta do microserviço
def get_microservice_address_port( service_name):
    # URL do Eureka Server
    #Escolhe um servidor eureka aleatorio
    server  = random.choice(EUREKA_SERVERS)
    eureka_server_url = 'http://'+server+'/eureka/apps/'

    try:
        # Fazendo uma solicitação GET para o Eureka Server para obter informações sobre o serviço desejado
        response = requests.get(eureka_server_url + service_name, headers={'Accept': 'application/json'})
        response.raise_for_status()

        # Analisando a resposta JSON
        data = response.json()

        # Verificando se há instâncias do serviço disponíveis
        if 'application' in data and 'instance' in data['application']:
            # Extraindo informações de uma das instâncias disponíveis (neste exemplo, usamos a primeira)
            instance = data['application']['instance'][0]
            service_address = instance['ipAddr']
            service_port = instance['port']['$']

            # Retornar o endereço e a porta do serviço encontrado
            return {'address': service_address, 'port': service_port}

        else:
            return {'address': "Indisponivel", 'port': -1}

    except requests.exceptions.RequestException as e:
        return {'address': "Erro ao Connectar", 'port': -1}


#retorna os dados json de um microservico
def get_microservice_data(username, password, ip, port,protocolo,path):
    # Codificar as credenciais em Base64
    credentials = f"{username}:{password}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    # Definir o cabeçalho de autenticação
    headers = {
        'Authorization': f'Basic {credentials_base64}',
        'Accept': 'application/json'  # Define o formato de resposta que você deseja receber (JSON)
    }

    # Construir a URL do microserviço
    url = f"{protocolo}://{ip}:{port}/{path}"  # Altere "/api/" para o endpoint correto do seu microserviço

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # O conteúdo da resposta estará no formato JSON
        data = response.json()
        #print(data)
        return data

    except requests.exceptions.RequestException as e:
        print('Erro na requisição: ', e)
        return None

if __name__=="__main__":
    print(get_microservice_address_port('IMAGE_SERVICE'))
