How to set up protobuf for Python GAE

1. Get the latest Protobuf source code
https://code.google.com/p/protobuf/downloads/list

2. Build C++ protobuf
   ./configure --prefix=$YOUR_PREFIX/protobuf && make && make install

3. Build Python protobuf
   cd python; python setup.py build;

4. Run setup.py in this dir in GAE root directory.
   The script executes the following things.
   4.1 Copy proto_src/python/google to GAE root directory as 'goog'.
   4.2 Rename all 'from google.protobuf' with 'from goog.protobuf'.

5. How to compile .proto file for GAE?
   protoc --python_out=. sample.proto && sed -i -e 's/from google\./from goog./' *_pb2.py
