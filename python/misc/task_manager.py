import threading

class Controller(object):
    def __init__(self, runner, task, callstack):
        self.__runner = runner
        self.__task = task
        self.__stack = callstack

    def call(self, task, state):
        stack = ((self.__task, state), self.__stack)
        self.__runner.push_call(stack, task)

    def done(self, response):
        self.__runner.push_done(self.__stack, response)

    def sync_call(self, task, state):
        stack = ((self.__task, state), self.__stack)
        self.__runner.sync_push_call(stack, task)

    def sync_done(self, response):
        self.__runner.sync_push_done(self.__stack, response)


class Runner(object):
    def __init__(self, task):
        # tasks is FIFO to run tasks in DFS way.
        # To run tasks in BFS way, use collections.deque.
        self.__tasks = [('call', None, task, None)]
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

    def push_call(self, callstack, subtask):
        self.__push_task(('call', callstack, subtask))

    def sync_push_call(self, callstack, subtask):
        self.__sync_push_task(('call', callstack, subtask))

    def push_done(self, callstack, response):
        self.__push_task(('done', callstack, response))

    def sync_push_done(self, callstack, response):
        self.__sync_push_task(('done', callstack, response))

    def __handle_exception(self, f, stack):
        if hasattr(f, 'dispose'):
            f.dispose()
        while stack:
            task, _ = stack[0]
            stack = stack[1]
            if hasattr(task, 'dispose'):
                task.dispose()

    def run_internal(self):
        task = self.__tasks.pop()
        type = task[0]
        stack = task[1]
        if type == 'call':
            f = task[2]
            cont = Controller(self, f, stack)
            try:
                f.start(cont)
            except:
                self.__handle_exception(f, stack)
                raise
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
                try:
                    task.resume(cont, state, response)
                except:
                    self.__handle_exception(task, parent_stack)
                    raise
