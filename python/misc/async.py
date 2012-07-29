import commands
import threading


tree = ('+',
       ('*', 3, 4),
       ('-', 10, ('*',
                  2,
                  3)))

large_tree = 1
for i in xrange(15):
    large_tree = ('+', large_tree, large_tree)

deep_tree = 1
for i in xrange(1000):
    deep_tree = ('+', deep_tree, 1)


def sync_multiply(x, y):
    return int(commands.getoutput('sleep 1; expr %d "*" %d' % (x, y)))


def eval(tree):
    if not isinstance(tree, tuple):
        return tree
    op = tree[0]
    if op == '+':
        return evalAdd(tree[1], tree[2])
    elif op == '-':
        return evalSub(tree[1], tree[2])
    elif op == '*':
        return evalMul(tree[1], tree[2])
    else:
        raise Exception('Unexpected op')


class EvalThread(threading.Thread):
    def __init__(self, tree):
        threading.Thread.__init__(self)
        self.tree = tree

    def run(self):
        self.result = eval(self.tree)


def evalAdd(left, right):
    left_thread = EvalThread(left)
    left_thread.start()
    right_result = eval(right)
    left_thread.join()
    return left_thread.result + right_result

def evalSub(left, right):
    left_thread = EvalThread(left)
    left_thread.start()
    right_result = eval(right)
    left_thread.join()
    return left_thread.result - right_result

def evalMul(left, right):
    left_thread = EvalThread(left)
    left_thread.start()
    right_result = eval(right)
    left_thread.join()
    return sync_multiply(left_thread.result, right_result)

print 'eval(tree) ==', eval(tree)

###########################################

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


class EvalTask(object):
    def start(self, cont, args):
        tree = args
        if not isinstance(tree, tuple):
            cont.done(tree)
            return
        op = tree[0]
        if op == '+':
            task = AddTask()
        elif op == '-':
            task = SubTask()
        elif op == '*':
            task = MulTask()
        else:
            raise Exception('Unexpected op')
        args = (tree[1], tree[2])
        cont.call(task, args, 'wait')

    def resume(self, cont, state, response):
        assert state == 'wait'
        cont.done(response)


class AddTask(object):
    def start(self, cont, args):
        left, right = args
        cont.call(EvalTask(), left, 'left')
        cont.call(EvalTask(), right, 'right')
        self.left_result = None
        self.right_result = None

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_result = response
        else:
            self.right_result = response
        if self.left_result is not None and self.right_result is not None:
            cont.done(self.left_result + self.right_result)


class SubTask(object):
    def start(self, cont, args):
        left, right = args
        cont.call(EvalTask(), left, 'left')
        cont.call(EvalTask(), right, 'right')
        self.left_result = None
        self.right_result = None

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_result = response
        else:
            self.right_result = response
        if self.left_result is not None and self.right_result is not None:
            cont.done(self.left_result - self.right_result)

class MulTask(object):
    def start(self, cont, args):
        left, right = args
        cont.call(EvalTask(), left, 'left')
        cont.call(EvalTask(), right, 'right')
        self.left_result = None
        self.right_result = None

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_result = response
        else:
            self.right_result = response
        if self.left_result is not None and self.right_result is not None:
            async_multiply(self.left_result, self.right_result,
                           lambda res: cont.sync_done(res))


class Controller(object):
    def __init__(self, runner, task, callstack):
        self.__runner = runner
        self.__task = task
        self.__stack = callstack

    def call(self, task, args, state):
        stack = ((self.__task, state), self.__stack)
        self.__runner.push_call(stack, task, args)

    def done(self, response):
        self.__runner.push_done(self.__stack, response)

    def sync_call(self, task, args, state):
        stack = ((self.__task, state), self.__stack)
        self.__runner.sync_push_call(stack, task, args)

    def sync_done(self, response):
        self.__runner.sync_push_done(self.__stack, response)


class Runner(object):
    def __init__(self, task, args):
        # tasks is FIFO to run tasks in DFS way.
        # To run tasks in BFS way, use collections.deque.
        self.__tasks = [('call', None, task, args)]
        self.response = None
        self.done = False
        self.__sync_tasks = []
        self.__cond = threading.Condition()

    def run(self):
        if not self.__tasks:
            self.__cond.acquire()
            while not self.__sync_tasks:
                self.__cond.wait()
            self.__tasks = self.__sync_tasks
            self.__sync_tasks = []
            self.__cond.release()

        while self.__tasks:
            self.run_internal()

    def __push_task(self, task):
        self.__tasks.append(task)

    def __sync_push_task(self, task):
        self.__cond.acquire()
        self.__sync_tasks.append(task)
        self.__cond.notify()
        self.__cond.release()

    def push_call(self, callstack, subtask, args):
        self.__push_task(('call', callstack, subtask, args))

    def sync_push_call(self, callstack, subtask, args):
        self.__sync_push_task(('call', callstack, subtask, args))

    def push_done(self, callstack, response):
        self.__push_task(('done', callstack, response))

    def sync_push_done(self, callstack, response):
        self.__sync_push_task(('done', callstack, response))

    def run_internal(self):
        task = self.__tasks.pop()
        type = task[0]
        stack = task[1]
        if type == 'call':
            f = task[2]
            cont = Controller(self, f, stack)
            f.start(cont, task[3])
        else:
            # 'done'
            response = task[2]
            if not stack:
                self.response = response
                self.done = True
            else:
                parent_stack = stack[1]
                task, state = stack[0]
                cont = Controller(self, task, parent_stack)
                task.resume(cont, state, response)


runner = Runner(EvalTask(), tree)
while runner.response is None:
    runner.run()
print 'runner.response =', runner.response
