import JavaWrapperOverhead.Calc

LOOP = 1000 * 1000

# time: 5947[ms]
# time: 723[ms]
# time: 1684[ms]

def UseInherits():
    class PyCalc(JavaWrapperOverhead.Calc):
        pass
    for i in xrange(LOOP):
        PyCalc().square(i)

def NoInherits():
    for i in xrange(LOOP):
        JavaWrapperOverhead.Calc().square(i)

def Proxy():
    class PyCalc(object):
        def __init__(self):
            self.__calc = JavaWrapperOverhead.Calc()
        def square(self, n):
            return self.__calc.square(n)
            
    for i in xrange(LOOP):
        PyCalc().square(i)
