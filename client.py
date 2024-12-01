from __future__ import print_function

import logging
import os
import grpc
import financeapp_pb2
import financeapp_pb2_grpc



def run():
    server_host = os.getenv('SERVER_HOST', 'server')
    server_port = os.getenv('SERVER_PORT', '50051')
    with grpc.insecure_channel(f'{server_host}:{server_port}') as channel:
        stub = financeapp_pb2_grpc.OperationStub(channel)
        scelta = input("Seleziona l'operazione da eseguire: \n1) Registra utente\n2) Aggiorna ticker\n3) Cancella utente\n4) Recupera valore\n5) Recupera media valori\n0) Esci\n")
        if scelta == "1":
            email = input("Inserisci email: ")
            ticker = input("Inserisci ticker: ")
            response = stub.RegistraUtente(financeapp_pb2.DatiUtente(email=email, ticker=ticker))
            print("Conferma registrazione: ", response.conferma)
        elif scelta == "2":
            email = input("Inserisci email: ")
            ticker = input("Inserisci nuovo ticker: ")
            response = stub.AggiornaTicker(financeapp_pb2.DatiUtente(email=email, ticker=ticker))
            print("Conferma aggiornamento: ", response.conferma)
        elif scelta == "3":
            email = input("Inserisci email: ")
            response = stub.CancellaUtente(financeapp_pb2.Email(email=email))
            print("Conferma cancellazione: ", response.conferma)
        elif scelta == "4":
            email = input("Inserisci email: ")
            response = stub.RecuperaValore(financeapp_pb2.Email(email=email))
            print("Valore ottenuto: ", response.valore)
        elif scelta == "5":
            email = input("Inserisci email: ")
            numeroDati = input("Inserisci il numero di dati: ")
            response = stub.CalcolaMediaValori(financeapp_pb2.Email(email=email, numeroDati=numeroDati))
            print("Media valori ottenuta: ", response.valore)
        else:
            print("Scelta non valida")
    


if __name__ == '__main__':
    logging.basicConfig()
    run()