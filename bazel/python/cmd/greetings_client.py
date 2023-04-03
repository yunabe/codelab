import grpc

from python.utils import greetings
from proto import greetings_pb2
from proto import greetings_pb2_grpc

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = greetings_pb2_grpc.GreetingsServiceStub(channel)
    req = greetings_pb2.GreetingRequest()
    req.name = 'grpc'
    print(stub.Hello(req))


if __name__ == '__main__':
    main()
