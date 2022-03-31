#nome del file : pagellaServerMulti.py

import socket
from threading import Thread
import json
import pprint

SERVER_ADDRESS = '127.0.0.2'
SERVER_PORT = 22226

#Versione 1 
def ricevi_comandi1(sock_service,addr_client):
    while True:
        data=sock_service.recv(1024)
        print(data)
        if not data: 
            break
        data=data.decode()
        data=json.loads(data)     
        print(data)   
        #1. recuperare dal json studente, materia, voto e assenze
        studente=data['cognome']
        materia=data['materia']
        voto=int(data['voto'])
        assenze=data['assenze']
        #2. restituire un messaggio in json contenente studente, materia e una valutazione testuale :
        # voto < 4 Gravemente insufficiente
        ris=""
        if voto<4:
            ris=" è Gravemente insufficiente"
        # voto [4..5] Insufficiente
        elif voto>4 and voto<5:
            ris=" è insufficiente"
        # voto = 6 Sufficiente
        elif voto==6:
            ris=" è sufficiente"
        # voto = 7 Discreto 
        elif voto==7:
            ris=" è discreta"
        # voto [8..9] Buono
        elif voto>8 and voto<9:
            ris=+" è buona"
        # voto = 10 Ottimo
        elif voto==10:
            ris=" è ottima"
        print("Client V:1")
        sock_service.sendall(ris.encode("UTF-8"))

    sock_service.close()

#Versione 2 
def ricevi_comandi2(sock_service,addr_client):
  #....
  #1.recuperare dal json studente e pagella
    while True:
        data=sock_service.recv(1024)
        if not data:
            break
        data=data.decode()
        data=json.loads(data)
        studente=data.keys()
        print(studente)
        media=0
        cont=0
        assenze=0
        print(studente)
  #2. restituire studente, media dei voti e somma delle assenze :
        for voto in data.values():
            media+=voto[1]
            cont+=1
            assenze+=voto[2]
        data={
        'studente':studente,
        'media':media/cont,
        'assenze':assenze,
        }
        sock_service.sendall(data.encode("UTF-8"))
        print("Client V2")
    sock_service.close()

#Versione 3
def ricevi_comandi3(sock_service,addr_client):

    while True:
        data=sock_service.recv(1024)
        if not data:
            break
        data=data.decode()
        data=json.loads(data)
  #....
  #1.recuperare dal json il tabellone
        pp=pprint.PrettyPrinter(indent=4)
  #2. restituire per ogni studente la media dei voti e somma delle assenze :
        tabellone=[]
        for stud in data:
            pagella=data[stud]
            assenze=0
            media=0
            for i,p in enumerate(pagella):
                media+=int(p[1])
                assenze+=int(p[2])
            media=media/i
            messaggio={'studenti':stud,
            'media':media,
            'assenze':assenze}
            tabellone.append(messaggio)
        print("Dati inviati al client:")
        pp.pprint(tabellone)
        messaggio=tabellone
        messaggio=json.dumps(messaggio)
        sock_service.sendall(messaggio.encode("UTF-8"))
    sock_service.close()
def ricevi_connessioni(sock_listen):
    while True:
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da " + str(addr_client))
        print("\nCreo un thread per servire le richieste ")
        try:
            Thread(target=ricevi_comandi1,args=(sock_service,addr_client)).start()
            #Thread(target=ricevi_comandi2,args=(sock_service,addr_client)).start()
            #Thread(target=ricevi_comandi3,args=(sock_service,addr_client)).start()
        except:
            print("il thread non si avvia")
            sock_listen.close()
        
def avvia_server(SERVER_ADDRESS,SERVER_PORT):
    sock_listen=socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock_listen.bind((SERVER_ADDRESS,SERVER_PORT))
    sock_listen.listen(5)
    print("Server in ascolto su %s." %str((SERVER_ADDRESS,SERVER_PORT)))
    ricevi_connessioni(sock_listen)

if __name__=='__main__':
    avvia_server(SERVER_ADDRESS,SERVER_PORT)