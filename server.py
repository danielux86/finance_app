from concurrent import futures
from cachetools import TTLCache

import hashlib
import logging
import re
import grpc
import financeapp_pb2
import financeapp_pb2_grpc
import MySQLdb
import os

# Database connection
def db_connection():
    try:
        connection = MySQLdb.connect(
            host=os.getenv('MYSQL_HOST', 'mysqldb'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER', 'server'),
            password=os.getenv('MYSQL_PASSWORD', '1234'),
            database=os.getenv('MYSQL_DATABASE', 'financeapp')
        )
        return connection
    except MySQLdb.Error as err:
        print("Error: ", err)
        return None

# Verifica formato email
def formato_corretto(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

# Genera id univoco
def genera_id(request, nome):
    hash = hashlib.sha256()
    hash.update(f"{nome}{request.email}{request.ticker}".encode('utf-8'))
    return hash.hexdigest()

# Creazione cache
cache = TTLCache(maxsize=100, ttl=30)

class Operation(financeapp_pb2_grpc.OperationServicer):

    def __init__(self):
        self.connection = db_connection()
        if self.connection is not None:
            self.cursor = self.connection.cursor()
        else:
            self.cursor = None
            
    def RegistraUtente(self, request, context):
        if not formato_corretto(request.email):
            return financeapp_pb2.Conferma(conferma=False, messaggio="Email non valida.")
        
        id = genera_id(request, "registrazione")
        if id in cache:
            return financeapp_pb2.Conferma(conferma=True, messaggio="Operazione già effettuata.")

        if self.cursor:
            try:
                self.cursor.execute("INSERT INTO utenti (email, ticker) VALUES (%s, %s)", (request.email, request.ticker))
                cache[id] = True
                self.connection.commit()
                return financeapp_pb2.Conferma(conferma=True, messaggio="Registrazione effettuata.")
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.Conferma(conferma=False)    
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.Conferma(conferma=False)

    def AggiornaTicker(self, request, context):
        id = genera_id(request, "aggiornamento")
        if id in cache:
            return financeapp_pb2.Conferma(conferma=True, messaggio="Operazione già effettuata.")
        
        if self.cursor:
            try:
                self.cursor.execute("UPDATE utenti SET ticker = %s WHERE email = %s", (request.ticker, request.email))
                cache[id] = True
                self.connection.commit()
                return financeapp_pb2.Conferma(conferma=True, messaggio="Ticker aggiornato.")
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.Conferma(conferma=False)
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.Conferma(conferma=False)
        
    def CancellaUtente(self, request, context):
        if self.cursor:
            try:
                self.cursor.execute("DELETE FROM utenti WHERE email = %s", (request.email,))
                self.cursor.execute("DELETE FROM data WHERE email = %s", (request.email,))
                self.connection.commit()
                return financeapp_pb2.Conferma(conferma=True, messaggio="Utente cancellato.")
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.Conferma(conferma=False)
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.Conferma(conferma=False)
        
    def RecuperaValore(self, request, context):
        if self.cursor:
            try:
                self.cursor.execute("SELECT valore FROM data WHERE email = %s ORDER BY timestamp DESC LIMIT 1", (request.email,))
                risultato = self.cursor.fetchone()
                if risultato:
                    print(f"Valore ottenuto: {risultato[0]}")
                    return financeapp_pb2.Valore(valore=risultato[0])
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Ticker not found')
                    return financeapp_pb2.Valore(valore='')
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.Valore(valore=0.0)
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.Valore(valore=0.0)
    
    def CalcolaMediaValori(self, request, context):
        if self.cursor:
            try:
                self.cursor.execute("""SELECT AVG(valore) FROM data WHERE email = %s AND ticker = 
                                    (SELECT ticker FROM data WHERE email = %s ORDER BY timestamp DESC LIMIT 1) 
                                    ORDER BY timestamp DESC LIMIT %s""", (request.email, request.email, request.numeroDati))
                risultati = self.cursor.fetchone()
                if risultati:
                    print(f"Valore ottenuto: {round(risultati[0], 2)}")
                    return financeapp_pb2.Valore(valore=risultati[0])
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Ticker not found')
                    return financeapp_pb2.Valore(valore=0.0)
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.Valore(valore=0.0)
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.Valore(valore=0.0)
    


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    financeapp_pb2_grpc.add_OperationServicer_to_server(Operation(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Echo Service started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()