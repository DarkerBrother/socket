#Peralta Sadivar Gian Michael
import socket
import sys
import random
import time
import threading
import multiprocessing
import json#importazione delle librerie necessarie

SERVER_ADDRESS = '127.0.0.1'#impostazione del SERVER_ADDRESS
SERVER_PORT = 22017#impostazione del server port
NUM_WORKERS=2#definizione del numero dei workers
class Client():

    def __init__(self,address,port):
        self.address=address
        self.port=port

    def connessione_server(self,address,port):
        sock_service = socket.socket()
        sock_service.connect((address,port))
        print("Connesso a " + str((address,port)))
        return sock_service

    def invia_comandi(self,sock_service):#creazione metodo "genera_richieste"
        start_time_thread= time.time()#registro il tempo d'inizio

        try:#si inizia sempre con il try, nel caso in cui vada in crash oppure ci sia un errore andiamo con l'except
            s=socket.socket()#creazione del socket
            s.connect((self.address,self.port))#connessione del socket alla porta ed address definiti
            print(f" Connessione al server: {self.address}:{self.port}")#print d'inizio 
        except Exception as e:#eccezione 8entra nel caso in cui il try no va a buon fine)
            print(e)
            print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")#print d'errore
            sys.exit()#uscita dal sistema
        #1. rimpiazzare questa parte con la generazione di operazioni e numeri random, non vogliamo inviare sempre 3+5 
        primoNumero=random.randint(0,5)#creazione della variabile primoNumero mediante random
        operazione=random.choice(["+","*","/","-","%"])#utilizzo di random in un vettore di stringhe
        secondoNumero=random.randint(0,5)#creazione della variabile secondoNumero usando il random

        #2. comporre il messaggio, inviarlo come json e ricevere il risultato
        messaggio={#creazione del messaggio
            'primoNumero':primoNumero,
            'operazione':operazione,
            'secondoNumero':secondoNumero,
        }

        messaggio=json.dumps(messaggio)#conversione del messaggio in un vettore di byte
        s.sendall(messaggio.encode("UTF-8"))#invio del messaggio al server, encriptato con UTF-8
        messaggio=s.recv(1024)#ricavo il risultato inviato dal server
        if not messaggio:#siccome un vettore riporta false, nel caso in cui sia true il server non risponde
            print(f"{threading.current_thread().name}: Server non risponde. Exit")
        else:#nel caso in cui ci sia un vettore stampo il risultato che messaggio decodificato sempre con UTF-8
            print(f"{threading.current_thread().name}: Risultato: {messaggio.decode('UTF-8')}") # trasforma il vettore di byte in stringa
        s.close()#chiusura del socket
        end_time_thread=time.time()#registrazione del tempo di fine
        print(f"{threading.current_thread().name} tempo di esecuzione time=", end_time_thread-start_time_thread)#visualizziamo il tempo di esecuzione

c1=Client(SERVER_ADDRESS,SERVER_PORT)
sock_serv=c1.connessione_server(SERVER_ADDRESS,SERVER_PORT)
c1.invia_comandi(sock_serv)
