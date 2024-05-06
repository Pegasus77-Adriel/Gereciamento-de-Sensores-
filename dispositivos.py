import socket
import json
import threading
from random import randint
from datetime import datetime
from time import sleep
import sys
import curses



class Dispositivo:
    
    def __init__(self):
            # Gera um número aleatório de 2 dígitos para a matrícula
            self.matricula = randint(1, 99)
            # Status significa se o dispositivo está ligado ou desligado 
            self.status = "Ligado"
            self.matricula = None
            self.temperatura = 35
            self.umidade = 50 
            self.HOST = '127.0.0.1'
            self.UDP_PORT = 60000
            self.TCP_PORT= 59999
            self.intervalo_envio = 10
            self.BUFFER_SIZE = 2048
            self.socket_udp = None
            self.socket_tcp = None
            self.monitorar = False
            #self.client_udp_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
    def main(self):
        try:
            socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_udp = socket_udp
            self.socket_tcp = socket_tcp
            
        except:
           return print("Falha na inicialização do dispositivo")
       
    
        thread1 = threading.Thread(target=self.enviar_dados, args=[socket_udp])
        thread1.start()
        thread2 = threading.Thread(target=self.conexaoTCP, args=[socket_tcp])
        thread2.start()
        
    
    def conexaoTCP(self, socket_tcp):
        socket_tcp.connect((self.HOST,self.TCP_PORT))
        
        while True:
            mensagem = socket_tcp.recv(self.BUFFER_SIZE)
            dados = mensagem.decode('utf-8')
            if not dados:
                pass
            else:
                print("Mensagem recebida:", dados)
                dados = json.loads(dados)
                self.tratar_comandos(dados)
                
    def tratar_comandos(self, dados):
       
        if (dados["fonte"] == "broker" and dados["tipo"] == "registro"):
            self.matricula = dados["matricula"]
            
            print(f'Dispositivo inicializado com sucesso!')
            
        elif (dados["fonte"] == "app" and dados["tipo"] == "comando"):
            self.setStatus(dados["operacao"])
        
            
    def setStatus(self, status):
        
        if(status == "desligar"):
            self.status = "Desligado"
            
        elif(status == "ligar"):
            self.status = "Ligado"
            
        data_hora_atuais = datetime.now()
        data_hora = data_hora_atuais.strftime('%d-%m-%Y %H:%M:%S')

        dic_dados = { "matricula" : self.matricula, "status" : self.status, "temperatura": str(self.temperatura) +'°C' , "umidade":str(self.umidade) + '%', "data_hora" : data_hora}
        dic_dados_bytes = json.dumps(dic_dados).encode('utf-8')
                
        self.socket_udp.sendto(dic_dados_bytes, (self.HOST, self.UDP_PORT))
        
        print(f'Status do dispositivo atualizado para {self.status}!')
        
    def setTemperatura(self):
        
        n = randint(1,2)
        temp = randint(0,3)
        
        if(n == 1):
            temp = temp * (-1)   
        
        self.temperatura = self.temperatura + (temp)
    
    def setUmidade(self):
        
        n = randint(1,2)
        umidade = randint(0,6)
        
        if(n == 1):
            umidade = umidade * (-1)   
        
        self.umidade = self.umidade + (umidade)
    
       
    def enviar_dados(self, client_env):
        
        while(True):
            sleep(self.intervalo_envio)
            if(self.status == "Ligado"):
            
                dispositvo.setTemperatura()
                dispositvo.setUmidade()
                data_hora_atuais = datetime.now()
                data_hora = data_hora_atuais.strftime('%d-%m-%Y %H:%M:%S')
                
                dic_dados = { "matricula" : self.matricula, "status" : self.status, "temperatura": str(self.temperatura) +'°C' , "umidade":str(self.umidade) + '%', "data_hora" : data_hora}
                dic_dados_bytes = json.dumps(dic_dados).encode('utf-8')
                
                client_env.sendto(dic_dados_bytes, (self.HOST, self.UDP_PORT))
                
                print("Mensagem enviada: ", dic_dados)
            
            
    def receber_dados(self, client_rec):
        
          while True:
            # Recebe os dados dos dispositivos através da conexão UDP
            dados_udp, HOST_client_udp = client_rec.recvfrom(self.BUFFER_SIZE)
            msg = dados_udp.decode()
            msg = json.loads(msg)
            
            print("Dados recebidos dispositivo: ", HOST_client_udp, "Mensagem: ", msg)
            

def exibir_opcoes():
    print("\n===== Bem-vindo ao Menu =====\n")
    print("Escolha uma das opções abaixo:")
    print("1. Monitorar entrada e saida de dados")
    print("2. Alterar tempo de amostragem ")
    print("3. Ligar")
    print("4. Desligar\n")


    
dispositvo = Dispositivo()
dispositvo.main()
exibir_opcoes()
    

