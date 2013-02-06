import Embed


class MyImp(Embed.MyInterface):
    def sayHello(self, name):
        print 'Hello %s in Python' % name


class MyChild(Embed.MyClass):
    def __init__(self, name):
        super(MyChild, self).__init__(name)

    def sayHello(self):
        name = self.getName()
        print 'Hello "%s" in Python MyChild' % name


myimp = MyImp()
mychild = MyChild('PyChild')
