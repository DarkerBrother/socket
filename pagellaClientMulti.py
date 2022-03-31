import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json
import pprint

pp=pprint.PrettyPrinter(indent=4)

SERVER_ADDRESS = '127.0.0.2'
SERVER_PORT = 22226
NUM_WORKERS=4

#Versione 1 
def genera_richieste1(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

    #1. Generazione casuale:
    cognome=random.choice(["Gornati","Zaniolo","Peralta","Colombo","Ghidoli"])#di uno studente (valori ammessi: 5 cognomi a caso tra cui il tuo cognome)
    materia=random.choice(["Matematica","Italiano","Inglese","Storia","Geografia"])#di una materia (valori ammessi: Matematica, Italiano, inglese, Storia e Geografia)
    voto=random.randint(1,10)#di un voto (valori ammessi 1 ..10)
    assenze=random.randint(1,5)#   delle assenze (valori ammessi 1..5) 
    #2. comporre il messaggio, inviarlo come json
    messaggio={
        'cognome':cognome,
        'materia':materia,
        'voto':voto,
        'assenze':assenze,
        }
    print("invio dati: "+str(messaggio))
    messaggio=json.dumps(messaggio)
    s.sendall(messaggio.encode("UTF-8"))    
    #esempio: {'studente': 'Studente4', 'materia': 'Italiano', 'voto': 2, 'assenze': 3}
    #3. ricevere il risultato come json: {'studente':'Studente4','materia':'italiano','valutazione':'Gravemente insufficiente'}
    data=s.recv(1024)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        #4 stampare la valutazione ricevuta esempio: La valutazione di Studente4 in italiano è Gravemente insufficiente
        print("la valutazione di "+cognome+" nella materia "+materia+data.decode())
    s.close()

#Versione 2 
def genera_richieste2(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
  #....
  #   1. Generazione casuale di uno studente(valori ammessi: 5 cognomi a caso scelti da una lista)
    cognome=random.choice(["Gornati","Zaniolo","Peralta","Colombo","Ghidoli"])
    pagella={
        cognome:[] 
    }
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
  #   generazione di un voto (valori ammessi 1 ..10)
    list=["Matematica","Italiano","Inglese","Storia","Geografia"]
    for a in list:
        voto=random.randint(1,10)
  #   e delle assenze (valori ammessi 1..5)
        assenze=random.randint(1,5) 
        pagella[cognome].append((a,voto,assenze))
  #   esempio: pagella={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9.5,3), ("Storia",8,2), ("Geografia",8,1)]}
    pp.pprint("invio di:\n"+str(pagella))#per debug
  #2. comporre il messaggio, inviarlo come json
    pagella=json.dumps(pagella)
    s.sendall
    data=s.recv(1024)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print("ricevo: \n"+data.decode())
  #3  ricevere il risultato come json {'studente': 'Cognome1', 'media': 8.0, 'assenze': 8}
    
#Versione 3
def genera_richieste3(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
  #....
  #   1. Per ognuno degli studenti ammessi: 5 cognomi a caso scelti da una lista
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
  #   generazione di un voto (valori ammessi 1 ..10)
  #   e delle assenze (valori ammessi 1..5) 
  #   esempio: tabellone={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9,3), ("Storia",8,2), ("Geografia",8,1)],
  #                       "Cognome2":[("Matematica",7,2), ("Italiano",5,3), ("Inglese",4,12), ("Storia",5,2), ("Geografia",4,1)],
  #                        .....}
    cognome=random.choice(["Gornati","Zaniolo","Peralta","Colombo","Ghidoli"])
    list=["Matematica","Italiano","Inglese","Storia","Geografia"]
    tabellone={}
    for c in cognome:
        pagella=[]
        for m in list:
            voto=random.randint(1,10)
            assenze=random.randint(1,5)
            pagella.append((m,voto,assenze))
        tabellone[c]=pagella
  #2. comporre il messaggio, inviarlo come json
  #3  ricevere il risultato come json e stampare l'output come indicato in CONSOLE CLIENT V.3
    print("Dati inviati al server")
    pp=pprint.PrettyPrinter(indent=4)
    pp.pprint(tabellone)
    tabellone=json.dumps(tabellone)
    s.sendall(tabellone.encode("UTF-8"))
    data=s.recv(1024)
    data=data.decode()
    data=json.load(data)
    print("Dati ricevuti dal server")
    pp.pprint(data)


if __name__ == '__main__':
    start_time=time.time()
    a=0
    #PUNTO A) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)
    while a<=NUM_WORKERS:
        genera_richieste1(a,SERVER_ADDRESS,SERVER_PORT)
        a+=1
    # alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]
    a=0
    # PUNTO B) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3)  
    # tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    while a<=NUM_WORKERS:
        thread=threading.Thread(target=genera_richieste2(a,SERVER_ADDRESS,SERVER_PORT),args=(a,SERVER_ADDRESS,SERVER_PORT,))
        threads.append(thread)
        a+=1
    # avviare tutti i thread e attenderne la fine
    [n.start() for n in threads]
    [n.join() for n in threads]
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    process=[]
    a=0
    # PUNTO C) ciclo per chiamare NUM_WORKERS volte la funzione genera richieste (1,2,3) 
    while a<=NUM_WORKERS:
        process.append(multiprocessing.Process(target=genera_richieste3(a,SERVER_ADDRESS,SERVER_PORT),args=(a,SERVER_ADDRESS,SERVER_PORT,)))
        a+=1
    # tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    # avviare tutti i processi e attenderne la fine
    [process.start() for p in process]
    [process.join() for p in process]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)
    a=0