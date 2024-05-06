import threading
import socket
import json
from time import sleep
from flask import Flask, request, jsonify

app = Flask(__name__)
class Broker:
  
    def __init__(self):
        
        self.HOST = '127.0.0.1'
        self.UDP_PORT= 60000
        self.TCP_PORT= 59999
        self.BUFFER_SIZE = 2048
        self.dispositivos = []
        self.dados_dispositivos = []
    
    def setDispositivos(self,dados):
        self.dispositivos[dados['matricula']] = str(dados)

    def broadcast(self,client):
        while(True):
            sleep(12)
            for matricula, dados in self.dispositivos.items():
        
                    dic_dados = { "matricula" : matricula,"comando":"verificar"}
                    dic_dados_bytes = json.dumps(dic_dados).encode('utf-8')
                    client.sendto(dic_dados_bytes, (self.HOST, self.PORT_ENV))
    def rest(self,app):
        
         app.run(host='127.0.0.1', port = 59998)
    
    def main(self,rest):
        
        
        
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
        socket_udp.bind((self.HOST, self.UDP_PORT))
        socket_tcp.bind((self.HOST, self.TCP_PORT))
        socket_tcp.listen()
            
        
        #print("Broker iniciado com sucesso!")
             
        #except:
            #return print("Erro ao iniciar o Broker!")
        #app.run(host='127.0.0.2', port = 8003)
        thread1 = threading.Thread(target=self.receber_dados, args=[socket_udp])
        thread1.start()
        thread2 = threading.Thread(target=self.conexaoTCP, args=[socket_tcp])
        thread2.start()
        
        thread3 = threading.Thread(target=self.rest, args=[rest])
        thread3.start()

        #thread2= threading.Thread(target=self.broadcast, args=[self.client_udp_env])
        #thread2.start()
        
        
    def receber_dados(self, socket_udp):
        
        while True:
            # Recebe os dados dos dispositivos através da conexão UDP
            dados_udp, HOST_client_udp = socket_udp.recvfrom(self.BUFFER_SIZE)
            msg = dados_udp.decode()
            msg = json.loads(msg)
            
            try:
                matricula = int(msg["matricula"])
                self.dados_dispositivos[matricula-1] = msg
            except:
                self.dados_dispositivos.append(msg)
            
            for i in self.dados_dispositivos:
                print(f'{i}')
            #print("Dados recebidos dispositivo: ", HOST_client_udp)
            #print(msg)
            
    
    def conexaoTCP(self, socket_tcp):
        cont = 0
        while True:
            
            # Aceita a conexão com os sockets dos clientes
            conn_client_tcp, addr_client_tcp = socket_tcp.accept()
            self.dispositivos.append(conn_client_tcp)
            print("Conectado com um cliente TCP em: ", addr_client_tcp)
            cont += 1
            
            dic_dados = {"fonte": "broker", "tipo": "registro","matricula": cont }
            dic_dados_bytes = json.dumps(dic_dados).encode('utf-8')
            conn_client_tcp.sendall(dic_dados_bytes)
            
    @app.route('/enviar_comando/<comando>/<matricula>', methods=['GET'])      
    def enviar_comando(comando,matricula):
        try:
            dispositivo = broker.dispositivos[int(matricula)-1]
            dic_dados = {"fonte": "app", "tipo": "comando","operacao":comando}
            dic_dados_bytes = json.dumps(dic_dados).encode('utf-8')
            dispositivo.sendall(dic_dados_bytes)
            sleep(1)
            dispositivo_dados = broker.dados_dispositivos[int(matricula)-1]
            status = dispositivo_dados["status"]
            msg = f'O dispositivo com a matricula {matricula} está {dispositivo_dados["status"]}'
            return jsonify({"mensagem":msg}), 200
        
        except:
            return jsonify({"mensagem": "Falha na operação"}), 200

    
    @app.route('/receber_medicao/<matricula>', methods=['GET'])
    def receber_medicao(matricula):
        
        try:
            dados = broker.dados_dispositivos[int(matricula)-1]
            return jsonify(dados)
        except:
            return jsonify({"mensagem": "Medição não encontrada!"}), 200
        
broker = Broker()

broker.main(app) 

