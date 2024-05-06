import requests
import json
from time import sleep

class App:
    
    def __init__(self):
        
            self.HOST = '127.0.0.1'
            self.BUFFER_SIZE = 2048
     
    def receber_dados(matricula):
        url = 'http://localhost:59998/enviar_medicao'  # URL do servidor
        headers = {'Content-Type': 'application/json'}
        dados = json.dumps(matricula)  # Converter para formato JSON
        response = requests.post(url, headers=headers, data=dados)
        print(response.json())

    def enviar_comando(self, comando, matricula):
        url = f'http://localhost:59998/enviar_comando/{comando}/{matricula}'  # URL do servidor
        #headers = {'Content-Type': 'application/json'}
        response = requests.get(url)
        print(response.json())
        
    def pedir_medicao(self,matricula):
        url = f'http://localhost:59998/receber_medicao/{matricula}'  # URL do servidor
        #headers = {'Content-Type': 'application/json'}
        response = requests.get(url)
        print(response.json())

if __name__ == '__main__':
    app = App()
    #comando = {"fonte": "app", "tipo": "receber_medicao","matricula":"1"}
    app.enviar_comando("desligar",1)
    sleep(60)
    app.enviar_comando("ligar",1)
    