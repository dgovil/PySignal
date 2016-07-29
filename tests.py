import pySignal
from functools import partial
try:
    import unittest2 as unittest
except:
    import unittest

def testFunc(value):
    print("Ran for %s" % value)


class SignalTestRunner(unittest.TestCase):

    def test_partialConnect(self):
        partialSignal = pySignal.Signal()
        partialSignal.connect(partial(testFunc, 'Partial'))
        partialSignal.emit()

    def test_lambdaConnect(self):
        lambdaSignal = pySignal.Signal()
        lambdaSignal.connect(lambda value: testFunc(value))
        lambdaSignal.emit('Lambda')

    def testMethod(self, value=2):
        print("Method called with %s" % value)

    def test_methodConnect(self):
        methodSignal = pySignal.Signal()
        methodSignal.connect(self.testMethod)
        methodSignal.emit(value=5)

    def test_functionConnect(self):
        funcSignal = pySignal.Signal()
        funcSignal.connect(testFunc)
        funcSignal.emit("Function")

if __name__ == '__main__':
    unittest.main()