

import sys

from python.utils import greetings
from proto import greetings_pb2

def main():
    # print(sys.path)
    req = greetings_pb2.GreetingRequest()
    req.name = 'world'
    print(greetings.hello(req.name))

if __name__ == '__main__':
    main()
