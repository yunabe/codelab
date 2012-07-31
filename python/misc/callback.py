import commands
import threading


tree = ('+',
        ('*', 3, 4),
        ('-', 10, ('*',
                   2,
                   3)))

def sync_multiply(x, y):
    return int(commands.getoutput('sleep 1; expr %d "*" %d' % (x, y)))


class AsyncMultiply(threading.Thread):
  def __init__(self, x, y, callback):
    threading.Thread.__init__(self)
    self.x = x
    self.y = y
    self.callback = callback

  def run(self):
      self.callback(sync_multiply(self.x, self.y))


def async_multiply(x, y, callback):
  th = AsyncMultiply(x, y, callback)
  th.start()


def eval(tree, callback):
    if not isinstance(tree, tuple):
        callback(tree)
        return
    op = tree[0]
    if op == '+':
        evalAdd(tree[1], tree[2], callback)
    elif op == '-':
        evalSub(tree[1], tree[2], callback)
    elif op == '*':
        evalMul(tree[1], tree[2], callback)
    else:
        raise Exception('Unexpected op')


def evalAdd(left, right, callback):
    left_result = []
    right_result = []

    def maybe_return_result():
        if left_result and right_result:
            callback(left_result[0] + right_result[0])

    def left_callback(result):
        left_result.append(result)
        maybe_return_result()

    def right_callback(result):
        right_result.append(result)
        maybe_return_result()

    eval(left, left_callback)
    eval(right, right_callback)


def evalSub(left, right, callback):
    left_result = []
    right_result = []

    def maybe_return_result():
        if left_result and right_result:
            callback(left_result[0] - right_result[0])

    def left_callback(result):
        left_result.append(result)
        maybe_return_result()

    def right_callback(result):
        right_result.append(result)
        maybe_return_result()

    eval(left, left_callback)
    eval(right, right_callback)


def evalMul(left, right, callback):
    left_result = []
    right_result = []

    def sync_callback(result):
        global_executor.register(callback, result)

    def maybe_return_result():
        if left_result and right_result:
            async_multiply(left_result[0],
                           right_result[0],
                           sync_callback)

    def left_callback(result):
        left_result.append(result)
        maybe_return_result()

    def right_callback(result):
        right_result.append(result)
        maybe_return_result()

    eval(left, left_callback)
    eval(right, right_callback)


class Executor(object):
    def __init__(self):
        self.__callbacks = []
        self.__cond = threading.Condition()
        self.__exit = False

    def register(self, f, *args, **kwds):
        self.__cond.acquire()
        self.__callbacks.append((f, args, kwds))
        self.__cond.notify()
        self.__cond.release()

    def loop(self):
        while not self.__exit:
            self.__loop_internal()

    def __loop_internal(self):
        self.__cond.acquire()
        while not self.__callbacks:
            self.__cond.wait()
        f, args, kwds = self.__callbacks.pop()
        self.__cond.release()
        f(*args, **kwds)

    def exit_loop(self):
        self.__exit = True


global_executor = Executor()


def printResult(result):
    print 'result ==', result
    global_executor.exit_loop()

global_executor.register(eval, tree, printResult)

print 'start loop'
global_executor.loop()
print 'done'
