import unittest

from task_manager import Runner

class Fib(object):
    def __init__(self, n):
        self.__n = n

    def start(self, cont):
        if self.__n <= 1:
            cont.done(1)
        else:
            cont.call(Fib(self.__n - 1), 1)

    def resume(self, cont, state, response):
        if state == 1:
            self.__res1 = response
            cont.call(Fib(self.__n - 2), 2)
        else:
            cont.done(self.__res1 + response)

class TaskManagerTest(unittest.TestCase):
    def testFib(self):
        runner = Runner(Fib(10))
        runner.run()
        self.assertTrue(runner.done)
        self.assertEquals(89, runner.response)

    def testDispose(self):
        class Dispose(object):
            def __init__(self, depth, log):
                self.__depth = depth
                self.__log = log
                self.__response_count = 0

            def start(self, cont):
                self.__label = cont.state()
                if self.__depth > 1:
                    cont.call(Dispose(self.__depth - 1, self.__log), 'left')
                    cont.call(Dispose(self.__depth - 1, self.__log), 'right')
                else:
                    cont.done(None)

            def resume(self, cont, state, response):
                self.__response_count += 1
                if self.__response_count == 2:
                    cont.done(None)

            def dispose(self):
                self.__log.append('Dispose: depth = %d, state = %s' % (
                        self.__depth, self.__label))

        log = []
        runner = Runner(Dispose(2, log))
        runner.run()
        self.assertEquals(3, len(log))
        self.assertEquals('Dispose: depth = 1, state = right', log[0])
        self.assertEquals('Dispose: depth = 1, state = left', log[1])
        self.assertEquals('Dispose: depth = 2, state = <init>', log[2])
                                                         

    def testDisponseWithException(self):
        class DisposeWithException(object):
            def __init__(self, log):
                self.__log = log

            def start(self, cont):
                cont.call(RaiseException(self.__log), 'child')

            def resume(self, cont, state, response):
                pass

            def dispose(self):
                self.__log.append('dispose:DisposeWithException')

        class RaiseException(object):
            def __init__(self, log):
                self.__log = log

            def start(self, cont):
                raise Exception('This is an exception!')

            def resume(self, cont, state, response):
                pass

            def dispose(self):
                self.__log.append('dispose:RaiseException')

        log = []
        runner = Runner(DisposeWithException(log))
        ok = False
        try:
            runner.run()
        except Exception, e:
            if e.message != 'This is an exception!':
                raise
            else:
                ok = True
        self.assertTrue(ok)
        self.assertEquals(2, len(log))
        self.assertEquals('dispose:RaiseException', log[0])
        self.assertEquals('dispose:DisposeWithException', log[1])

    def testDisponseWithExceptionInResume(self):
        class DisposeWithException(object):
            def __init__(self, log):
                self.__log = log

            def start(self, cont):
                cont.call(RaiseException(self.__log), 'child')

            def resume(self, cont, state, response):
                pass

            def dispose(self):
                self.__log.append('dispose:DisposeWithException')

        class RaiseException(object):
            def __init__(self, log):
                self.__log = log

            def start(self, cont):
                cont.call(Child(self.__log), 'child')

            def resume(self, cont, state, response):
                raise Exception('This is an exception!')

            def dispose(self):
                self.__log.append('dispose:RaiseException')

        class Child(object):
            def __init__(self, log):
                self.__log = log

            def start(self, cont):
                cont.done(None)

            def dispose(self):
                self.__log.append('dispose:Child')

        log = []
        runner = Runner(DisposeWithException(log))
        ok = False
        try:
            runner.run()
        except Exception, e:
            if e.message != 'This is an exception!':
                raise
            else:
                ok = True
        self.assertTrue(ok)
        self.assertEquals(3, len(log))
        self.assertEquals('dispose:Child', log[0])
        self.assertEquals('dispose:RaiseException', log[1])
        self.assertEquals('dispose:DisposeWithException', log[2])


if __name__ == '__main__':
    unittest.main()
