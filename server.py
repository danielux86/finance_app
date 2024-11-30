from concurrent import futures
import logging

import grpc
import financeapp_pb2
import financeapp_pb2_grpc
import MySQLdb

# Database connection
def db_connection():
    try:
        connection = MySQLdb.connect(
            host="localhost",
            user="server",
            password="1234",
            database="financeapp"
        )
        return connection
    except MySQLdb.Error as err:
        print("Error: ", err)
        return None


class Operation(financeapp_pb2_grpc.OperationServicer):

    def __init__(self):
        self.connection = db_connection()
        if self.connection is not None:
            self.cursor = self.connection.cursor()
        else:
            self.cursor = None

    def Mul(self, request, context):
        if self.cursor:
            try:
                self.cursor.execute("INSERT INTO operations (op1, op2, operation, result) VALUES (%s, %s, %s, %s)", (request.op1, request.op2, "Mul", request.op1 * request.op2))
                self.connection.commit()
                return financeapp_pb2.OpReply(res=request.op1 * request.op2)
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.OpReply()
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.OpReply()

    def Add(self, request, context):
        if self.cursor:
            try:
                self.cursor.execute("INSERT INTO operations (op1, op2, operation, result) VALUES (%s, %s, %s, %s)", (request.op1, request.op2, "Add", request.op1 + request.op2))
                self.connection.commit()
                return financeapp_pb2.OpReply(res=request.op1 + request.op2)
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.OpReply()
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.OpReply()

    def Sub(self, request, context):
        if self.cursor:
            try:
                self.cursor.execute("INSERT INTO operations (op1, op2, operation, result) VALUES (%s, %s, %s, %s)", (request.op1, request.op2, "Sub", request.op1 - request.op2))
                self.connection.commit()
                return financeapp_pb2.OpReply(res=request.op1 - request.op2)
            except MySQLdb.Error as err:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f'Database error: {err}')
                return financeapp_pb2.OpReply()
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Database connection failed')
            return financeapp_pb2.OpReply()
    


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
