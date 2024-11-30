from __future__ import print_function

import logging

import grpc
import financeapp_pb2
import financeapp_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = financeapp_pb2_grpc.OperationStub(channel)
        op1 = input("Inserisci il primo numero: ")
        op2 = input("Inserisci il secondo numero: ")
        scelta = input("Seleziona l'operazione da eseguire: \n1) Addizione\n2) Sottrazione\n3) Moltiplicazione\n4) Divisione\n")
        if scelta == "1":
            response = stub.Add(financeapp_pb2.OpRequest(op1=int(op1),op2=int(op2)))
            print("Risultato: ", response.res)
        elif scelta == "2":
            response = stub.Sub(financeapp_pb2.OpRequest(op1=int(op1),op2=int(op2)))
            print("Risultato: ", response.res)
        elif scelta == "3":
            response = stub.Mul(financeapp_pb2.OpRequest(op1=int(op1),op2=int(op2)))
            print("Risultato: ", response.res)
        elif scelta == "4":
            response = stub.Div(financeapp_pb2.OpRequest(op1=float(op1),op2=float(op2)))
            print("Risultato: ", response.res)
        else:
            print("Scelta non valida")
    


if __name__ == '__main__':
    logging.basicConfig()
    run()

