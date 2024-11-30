Il progetto riguarda lo sviluppo di un'applicazione di gestione delle informazioni finanziarie, basata su un'architettura a microservizi e comunicazione tramite gRPC.
L'applicazione consente la registrazione e gestione degli utenti, l'aggiornamento dei ticker finanziari e la raccolta di dati relativi ai valori azionari.
Utilizzando un database MySQL, i microservizi sono separati in due categorie principali: uno per la gestione degli utenti e uno per la gestione delle informazioni sui ticker azionari.
La comunicazione tra client e server avviene tramite chiamate gRPC, sfruttando i protocolli di serializzazione Protobuf.
Inoltre, il progetto implementa un sistema di cache per garantire l'unicità delle operazioni (at-most-once), evitando chiamate duplicate per le stesse operazioni.
L'applicazione supporta operazioni di registrazione utente, aggiornamento dei ticker, eliminazione degli utenti e recupero dei valori storici e media degli ultimi valori selezionati. 

# **Buils & Deploy:**
**Requisiti**
- Docker
- Python

Procedimento:
1. Effettuare da riga di comando il *git clone* della repository GitHub (https://github.com/danielux86/finance_app)
2. Spostarsi all'interno della cartella clonata e da riga di comando avviare *Docker Compose* con il seguente comando
    *docker compose up --build*
3. Ultimato il building dei container, digitare il comando *docker ps* per visualizzare l'elenco dei container
4. Copiare l'ID corrispondente al container *Client* ed entrare nel container digitando il comando
    *docker exec -it <ID_del_Client> bash
5. Dal container Client avviare il *Client* utilizzando il seguente comando
    *python client.py*
6. Eseguire le istruzioni visualizzate nel terminale


