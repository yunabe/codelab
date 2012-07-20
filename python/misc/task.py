
tree = ('+',
       ('*', 3, 4),
       ('-', 10, ('*',
                  2,
                  3)))


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

def evalAdd(left, right):
    return eval(left) + eval(right)

def evalSub(left, right):
    return eval(left) - eval(right)

def evalMul(left, right):
    return eval(left) * eval(right)


print 'eval(tree) ==', eval(tree)

###########################################

class Controller(object):
    def __init__(self, runner, task, callstack):
        self.__runner = runner
        self.__task = task
        self.__stack = callstack

    def call(self, task, args, state):
        stack = ((self.__task, state), self.__stack)
        self.__runner.push_call(stack, task, args)

    def done(self, response):
        if self.__stack is None:
            self.__runner.record_done(response)
        else:
            stack = self.__stack[1]
            task, state = self.__stack[0]
            self.__runner.push_resume(stack, task, state, response)


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
        self.right = right
        cont.call(EvalTask(), left, 'left')

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_res = response
            cont.call(EvalTask(), self.right, 'right')
        else:
            assert state == 'right'
            cont.done(self.left_res + response)

class SubTask(object):
    def start(self, cont, args):
        left, right = args
        self.right = right
        cont.call(EvalTask(), left, 'left')

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_res = response
            cont.call(EvalTask(), self.right, 'right')
        else:
            assert state == 'right'
            cont.done(self.left_res - response)

class MulTask(object):
    def start(self, cont, args):
        left, right = args
        self.right = right
        cont.call(EvalTask(), left, 'left')

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_res = response
            cont.call(EvalTask(), self.right, 'right')
        else:
            assert state == 'right'
            cont.done(self.left_res * response)

class Runner(object):
    def __init__(self, task, args):
        self.tasks = [('call', None, task, args)]
        self.response = None
        self.done = False

    def run(self):
        while self.tasks:
            self.run_internal()

    def push_call(self, callstack, subtask, args):
        self.tasks.append(('call', callstack, subtask, args))

    def push_resume(self, callstack, parenttask, state, response):
        self.tasks.append(('resume', callstack, parenttask, state, response))

    def record_done(self, response):
        self.response = response
        self.done = True

    def run_internal(self):
        task = self.tasks[0]
        self.tasks = self.tasks[1:]
        type = task[0]
        stack = task[1]
        if type == 'call':
            f = task[2]
            cont = Controller(self, f, stack)
            f.start(cont, task[3])
        else:
            # 'resume'
            f = task[2]
            cont = Controller(self, f, stack)
            f.resume(cont, task[3], task[4])


runner = Runner(EvalTask(), tree)
runner.run()
print 'runner.response =', runner.response
