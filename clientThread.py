#Peralta Sadivar Gian Michael
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=2

def genera_richieste(num,address,port):
    start_time_thread= time.time()
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    #1. rimpiazzare questa parte con la generazione di operazioni e numeri random, non vogliamo inviare sempre 3+5 
    primoNumero=random.randint(0,5)
    operazione=random.choice(["+","*","/","-","%"])
    secondoNumero=random.randint(0,5)

    #2. comporre il messaggio, inviarlo come json e ricevere il risultato
    messaggio={
        'primoNumero':primoNumero,
        'operazione':operazione,
        'secondoNumero':secondoNumero,
    }
    messaggio=json.dumps(messaggio)
    s.sendall(messaggio.encode("UTF-8"))
    messaggio=s.recv(1024)
    if not messaggio:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(f"{threading.current_thread().name}: Risultato: {messaggio.decode('UTF-8')}") # trasforma il vettore di byte in stringa
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} tempo di esecuzione time=", end_time_thread-start_time_thread)

if __name__ == '__main__':#inizio del main
    start_time=time.time()
    # 3 ciclo per chiamare NUM_WORKERS volte la funzione "genera" richieste alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    num = 0
    while num <= NUM_WORKERS:
        genera_richieste(num,SERVER_ADDRESS,SERVER_PORT);
        num+=1
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
    
    start_time=time.time()
    threads=[]
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione "genera_richieste" tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    while num<=NUM_WORKERS:
        thread = threading.Thread(target=genera_richieste(num,SERVER_ADDRESS,SERVER_PORT), args=(num,SERVER_ADDRESS,SERVER_PORT,))
    # ad ogni iterazione appendo il thread creato alla lista threads
        threads.append(thread)
        num+=1
    # 5 avvio tutti i thread
    [n.start() for n in threads]
    [n.join() for n in threads]
            
    # 6 aspetto la fine di tutti i thread 
     
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    process=[]

    num=0
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    while num<=NUM_WORKERS:
        processo = multiprocessing.Process(target=genera_richieste(num,SERVER_ADDRESS,SERVER_PORT), args=(num,SERVER_ADDRESS,SERVER_PORT,))
    # ad ogni iterazione appendo il thread creato alla lista threads
        process.append(processo)
        num+=1
    # 8 avvio tutti i processi
    [p.start() for p in process]
    # 9 aspetto la fine di tutti i processi 
    [p.join() for p in process]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)