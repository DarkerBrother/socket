import socket
from threading import Thread
import json

SERVER_ADDRESS="127.0.0.1"
SERVER_PORT=22017
class server():

    def __init__(self,address,port):
        self.address = address
        self.port=port

    def avvia_server(self):
        sock_listen=socket.socket()
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_listen.bind((self.address, self.port))
        sock_listen.listen(5)
        print("Server in ascolto su %s." % str((self.address, self.port)))
        return sock_listen

    def accetta_connessioni(self,sock_listen):
        while True:
            sock_service, addr_client = sock_listen.accept()
            print("\nConnessione ricevuta da " + str(addr_client))
            print("\nCreo un thread per servire le richieste")
            try:
                Thread(target=self.ricevi_comandi, args=(sock_service, addr_client)).start()
            except:
                print("Il thread non si avvia")
                sock_listen.close()

    def ricevi_comandi(self,sock_service, addr_client):
        print("avviato")
        while True:
            dati=sock_service.recv(1024)
            if not dati:
                print("fine dati dal client. Reset")
                break
            dati=dati.decode()
            print("Ricevuto: '%s'" % dati)
            dati=json.loads(dati)
            primoNumero=dati['primoNumero']
            operazione=dati['operazione']
            secondoNumero=dati['secondoNumero']
            ris=""
            if operazione=="+":
                ris=primoNumero+secondoNumero
            elif operazione=="-":
                ris=primoNumero-secondoNumero
            elif operazione=="*":
                ris=primoNumero*secondoNumero
            elif operazione=="/":
                if secondoNumero==0:
                    ris="Non puoi dividere per 0"
                else:
                    ris=primoNumero/secondoNumero
            elif operazione=="%":
                ris=primoNumero%secondoNumero
            else:
                ris="Operazione non riconosciuta"
            ris=str(ris)
            sock_service.sendall(ris.encode("UTF-8"))
        sock_service.close()

s1=server(SERVER_ADDRESS,SERVER_PORT)
sock_lis=s1.avvia_server()
s1.accetta_connessioni(sock_lis)
    
