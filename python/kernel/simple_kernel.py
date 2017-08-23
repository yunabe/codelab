# A simple jupyter kernel in python
# Ref:
#  http://jupyter-client.readthedocs.io/en/latest/wrapperkernels.html
#
# Notes:
#  This kernel demonstrates do_shutdown is not executed while do_execute is running.
#  I guess it's due to the API restrict of ZMQStream.on_recv. But not sure.

from ipykernel.kernelapp import IPKernelApp
from ipykernel.kernelbase import Kernel

import sys
import time

class SimpleKernel(Kernel):
    implementation = 'SimpleKernel'
    implementation_version = '1.0'
    language_info = {
        'name': 'txt',
    }
    banner = "Simple Kernel"
    
    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        print >> sys.__stderr__, 'do_execute is invoked'
        try:
            stream_content = {'name': 'stdout', 'text': code + '\n'}
            self.send_response(self.iopub_socket, 'stream', stream_content)
            for i in xrange(10):
                msg = '%s %d' % (code, i)
                print >> sys.__stderr__, msg
                self.send_response(
                    self.iopub_socket, 'stream',
                    {'name': 'stdout', 'text': msg + '\n'})
                time.sleep(1)
        except KeyboardInterrupt:
            self.send_response(
                    self.iopub_socket, 'stream',
                    {'name': 'stderr', 'text': 'Interrupted'})
         
        print >> sys.__stderr__, 'end of do_execute'
        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
        }

    def do_shutdown(self, restart):
        print >> sys.__stderr__, 'do_shutdown is invoked'
        super(SimpleKernel, self).do_shutdown(restart)


def main():
    print >> sys.__stderr__, 'Starting SimpleKernel'
    IPKernelApp.launch_instance(kernel_class=SimpleKernel)
    print >> sys.__stderr__, 'SimpleKernel is terminated'

if __name__ == '__main__':
    main()
