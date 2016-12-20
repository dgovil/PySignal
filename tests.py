from __future__ import print_function
import PySignal
from functools import partial
try:
    import unittest2 as unittest
except:
    import unittest



def testFunc(value):
    """
    A test standalone function for signals to attach onto
    """
    print("Ran for %s" % value)
    SignalTest.checkval = value

class DummySignalClass(object):
     """A dummy class to check for instance handling of signals"""
     cSignal = PySignal.ClassSignal()
     cSignalFactory = PySignal.ClassSignalFactory()

     def __init__(self):
         self.signal = PySignal.Signal()
         self.signalFactory = PySignal.SignalFactory()


class SignalTest(unittest.TestCase):
    checkval = None # A state check for the tests

    def setVal(self, val):
        """A method to test instance settings with"""
        self.checkval = val

    def throwaway(self, *args):
        """A method to throw redundant data into"""
        pass

    def test_partialConnect(self):
        """Tests if signals can connect to partials"""
        partialSignal = PySignal.Signal()
        partialSignal.connect(partial(testFunc, 'Partial'))
        partialSignal.emit()
        self.assertEqual(self.checkval, 'Partial')

    def test_lambdaConnect(self):
        """Tests if signals can be connected to lambdas"""
        lambdaSignal = PySignal.Signal()
        lambdaSignal.connect(lambda value: testFunc(value))
        lambdaSignal.emit('Lambda')
        self.assertEqual(self.checkval, 'Lambda')

    def printer(self, value=2):
        """Dummy printer method for signals to connect to"""
        print("Method called with %s" % value)
        SignalTest.checkval = value

    def test_methodConnect(self):
        """Test if signals can be connected to methods on class instances"""
        methodSignal = PySignal.Signal()
        methodSignal.connect(self.printer)
        methodSignal.emit(value=5)
        self.assertEqual(self.checkval, 5)

    def test_functionConnect(self):
        """Test if signals can be connected to standalone functions"""
        funcSignal = PySignal.Signal()
        funcSignal.connect(testFunc)
        funcSignal.emit("Function")
        self.assertEqual(self.checkval, 'Function')

    def test_signalEmit(self):
        """Test if a signal can be emitted"""
        toSucceed = DummySignalClass()
        toSucceed.signal.connect(self.setVal)
        toSucceed.signal.emit(20)

        self.assertEqual(self.checkval, 20)

    def test_classSignalEmit(self):
        """Test if the class signal can be emitted but also that instances of the class are unique"""
        toSucceed = DummySignalClass()
        toSucceed.cSignal.connect(self.setVal)

        toFail = DummySignalClass()
        toFail.cSignal.connect(self.throwaway)

        toSucceed.cSignal.emit(50)
        toFail.cSignal.emit(80)

        self.assertEqual(self.checkval, 50)

    def test_signalFactoryEmit(self):
        """Test if the signal factory can emit signals"""
        toSucceed = DummySignalClass()
        toSucceed.signalFactory.register('Spam')
        toSucceed.signalFactory['Spam'].connect(self.setVal)

        toSucceed.signalFactory['Spam'].emit(22)

        self.assertEqual(self.checkval, 22)

    def test_cSignalFactoryEmit(self):
        """Test if the class signal factory can emit signals but also that class instances are unique"""
        toSucceed = DummySignalClass()
        toSucceed.cSignalFactory.register('Spam')
        toSucceed.cSignalFactory['Spam'].connect(self.setVal)

        toFail = DummySignalClass()
        toFail.cSignalFactory.register('Spam')
        toFail.cSignalFactory['Spam'].connect(self.throwaway)

        toSucceed.cSignalFactory['Spam'].emit(45)
        toFail.cSignalFactory['Spam'].emit(12)

        self.assertEqual(self.checkval, 45)

    def test_signalBlock(self):
        """Test if the signal factory can block signals"""
        dummy = DummySignalClass()
        dummy.signalFactory.register('Spam', self.setVal)
        dummy.signalFactory['Spam'].emit(105)

        self.assertEqual(self.checkval, 105)

        dummy.signalFactory.block()

        dummy.signalFactory['Spam'].emit(202)
        self.assertNotEqual(self.checkval, 202)



if __name__ == '__main__':
    unittest.main()