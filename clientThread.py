#Peralta Sadivar Gian Michael
import socket
import sys
import random
import time
import threading
import multiprocessing
import json#importazione delle librerie necessarie

SERVER_ADDRESS = '127.0.0.1'#impostazione del SERVER_ADDRESS
SERVER_PORT = 22225#impostazione del server port
NUM_WORKERS=2#definizione del numero dei workers

def genera_richieste(num,address,port):#creazione metodo "genera_richieste"
    start_time_thread= time.time()#registro il tempo d'inizio
    try:#si inizia sempre con il try, nel caso in cui vada in crash oppure ci sia un errore andiamo con l'except
        s=socket.socket()#creazione del socket
        s.connect((address,port))#connessione del socket alla porta ed address definiti
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")#print d'inizio 
    except:#eccezione 8entra nel caso in cui il try no va a buon fine)
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

if __name__ == '__main__':#inizio del main
    start_time=time.time()#registrazione del tempo d'inizio
    # 3 ciclo per chiamare NUM_WORKERS volte la funzione "genera" richieste alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    num = 0#inizializzazione deell'indice
    while num <= NUM_WORKERS:
        genera_richieste(num,SERVER_ADDRESS,SERVER_PORT);#richiamo del metodo per eseguire i calcoli con il main
        num+=1#incremento del contatore
    end_time=time.time()#registrazione del tempo di fine
    print("Total SERIAL time=", end_time - start_time)#visualizzo il tempo tascorso
    
    start_time=time.time()#registro il tempo d'inizio
    threads=[]#creazione vettore dei threads
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione "genera_richieste" tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    while num<=NUM_WORKERS:
        thread = threading.Thread(target=genera_richieste(num,SERVER_ADDRESS,SERVER_PORT), args=(num,SERVER_ADDRESS,SERVER_PORT,))#assegnazione del metodo genera_richieste assegnando come args i valori necessari
    # ad ogni iterazione appendo il thread creato alla lista threads
        threads.append(thread)#aggiungiamo il thread, ai vettori di threads
        num+=1
    # 5 avvio tutti i thread
    [n.start() for n in threads]#inizio di tutt ii thread in contemporanea mediante un for su una riga delimitato da quadre
    [n.join() for n in threads]#metto in pausa il main
            
    # 6 aspetto la fine di tutti i thread 
     
    end_time=time.time()#registrazione della fine del tempo
    print("Total THREADS time= ", end_time - start_time)#visualizzo il tempo impiegato

    start_time=time.time()#registro il tempo d'inizio
    process=[]#creo il vettore di processi

    num=0#resetto l'indice a 0
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    while num<=NUM_WORKERS:
        processo = multiprocessing.Process(target=genera_richieste(num,SERVER_ADDRESS,SERVER_PORT), args=(num,SERVER_ADDRESS,SERVER_PORT,))#creazione di un processo assegnandogli come target la funzione genera_richieste con args gli eventuali parametri
    # ad ogni iterazione appendo il thread creato alla lista threads
        process.append(processo)#aggiungo il processo al vettore di processi
        num+=1#incremento il contatore
    # 8 avvio tutti i processi
    [p.start() for p in process]#inizio di tutti i processi in contemporanea con un for su una riga
    # 9 aspetto la fine di tutti i processi 
    [p.join() for p in process]#metto in pausa il main
    end_time=time.time()#registro il tempo di fine
    print("Total PROCESS time= ", end_time - start_time)#visualizzo i ltempo impiegato