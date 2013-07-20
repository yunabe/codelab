# protoc --python_out=. sample.proto && sed -i -e 's/from google\./from goog./' *_pb2.py

import commands
from optparse import OptionParser
import re
import sys


parser = OptionParser()
parser.add_option("-d", "--dir", dest="protodir",
                  help="copy python files from proto python DIR", metavar="DIR")

NEW_NAME = 'goog'

IMPORT_RE = re.compile(r'from google\.protobuf(?=[\.\s])')

def main():
    options, args = parser.parse_args()
    protodir = options.protodir
    if not protodir:
        print >> sys.stderr, 'Please set --dir'
        sys.exit(1)
    if not protodir.endswith('google'):
        print >> sys.stderr, 'proto dir must be .../google'
        sys.exit(1)
    rc, output = commands.getstatusoutput(
        '/bin/cp -r "%s" goog' % protodir)
    print >> sys.stderr, output
    if rc:
        print >> sys.stderr, 'Failed to copy proto sources.'
        sys.exit(1)
    for pyfile in commands.getoutput('find goog | grep \\.py$').split():
        print >> sys.stderr, 'Rewriting', pyfile
        with open(pyfile, 'r') as reader:
            content = reader.read()
        with open(pyfile, 'w') as writer:
            writer.write(IMPORT_RE.sub('from goog.protobuf', content))
        

if __name__ == '__main__':
    main()
