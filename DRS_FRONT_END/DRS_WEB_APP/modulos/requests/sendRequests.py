import requests
import base64


def sendPostRequest(json,adress,username, password,params=None, TLS_VALUE=False):
    credentials = f"{username}:{password}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    # Definir o cabeçalho de autenticação
    headers = {
        'Authorization': f'Basic {credentials_base64}',
        'Accept': 'application/json',  # Define o formato de resposta que você deseja receber (JSON)
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{adress}",params=params,json = json,headers = headers,verify=TLS_VALUE)
    return response.json()


#delete request
def sendDeleteRequest(json,adress,username, password,params=None, TLS_VALUE=False):
    credentials = f"{username}:{password}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    # Definir o cabeçalho de autenticação
    headers = {
        'Authorization': f'Basic {credentials_base64}',
        'Accept': 'application/json',  # Define o formato de resposta que você deseja receber (JSON)
        'Content-Type': 'application/json'
    }
    response = requests.delete(f"{adress}",params=params,json=json,headers=headers, verify=TLS_VALUE)
    return response.json()