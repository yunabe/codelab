from concurrent import futures

import grpc

from python.utils import greetings
from proto import greetings_pb2
from proto import greetings_pb2_grpc

class GreetingsServiceServicer(greetings_pb2_grpc.GreetingsServiceServicer):
    def Hello(self, req, context):
        """Missing associated documentation comment in .proto file."""
        res = greetings_pb2.GreetingResponse()
        res.message = greetings.hello(req.name)
        return res


def main():
    # https://grpc.io/docs/languages/python/basics/#server
    # print(dir(greetings_pb2_grpc))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greetings_pb2_grpc.add_GreetingsServiceServicer_to_server(
       GreetingsServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
