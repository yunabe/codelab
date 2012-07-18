
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

class Cont(object):
    def __init__(self):
        self.call_list = []
        self.done_list = []

    def call(self, task, args, state):
        self.call_list.append((task, args, state))

    def done(self, response):
        self.done_list.append(response)


class EvalTask(object):
    def start(self, cont, args):
        tree = args
        if not isinstance(tree, tuple):
            cont.done(tree)
            return
        op = tree[0]
        if op == '+':
            task = AddTask
        elif op == '-':
            task = SubTask
        elif op == '*':
            task = MulTask
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
        cont.call(EvalTask, left, 'left')

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_res = response
            cont.call(EvalTask, self.right, 'right')
        else:
            assert state == 'right'
            cont.done(self.left_res + response)

class SubTask(object):
    def start(self, cont, args):
        left, right = args
        self.right = right
        cont.call(EvalTask, left, 'left')

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_res = response
            cont.call(EvalTask, self.right, 'right')
        else:
            assert state == 'right'
            cont.done(self.left_res - response)

class MulTask(object):
    def start(self, cont, args):
        left, right = args
        self.right = right
        cont.call(EvalTask, left, 'left')

    def resume(self, cont, state, response):
        if state == 'left':
            self.left_res = response
            cont.call(EvalTask, self.right, 'right')
        else:
            assert state == 'right'
            cont.done(self.left_res * response)

class Runner(object):
    def __init__(self, task, args):
        self.tasks = [('call', None, task, args)]
        self.response = None

    def run(self):
        while self.tasks:
            self.run_internal()

    def run_internal(self):
        task = self.tasks[0]
        self.tasks = self.tasks[1:]
        type = task[0]
        stack = task[1]
        cont = Cont()
        if type == 'call':
            f = task[2]()
            f.start(cont, task[3])
        else:
            # 'resume'
            f = task[2]
            f.resume(cont, task[3], task[4])
        for call in cont.call_list:
            self.tasks.append(('call', ((f, call[2]), stack), call[0], call[1]))
        for response in cont.done_list:
            if stack:
                self.tasks.append(('resume', stack[1], stack[0][0], stack[0][1], response))
            else:
                self.response = response


runner = Runner(EvalTask, tree)
runner.run()
print 'runner.response =', runner.response
