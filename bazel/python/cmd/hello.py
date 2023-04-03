

import sys

from python.utils import greetings
from proto import greetings_pb2
from proto import greetings_pb2_grpc

def main():
    # print(sys.path)
    req = greetings_pb2.GreetingRequest()
    req.name = 'world'
    print(greetings.hello(req.name))
    print('greetings_pb2:', dir(greetings_pb2))
    print('greetings_pb2_grpc:', dir(greetings_pb2_grpc))

if __name__ == '__main__':
    main()
