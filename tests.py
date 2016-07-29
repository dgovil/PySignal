import pySignal
from functools import partial

def greet(name, leaving=False):
    print("%s, %s" % ('Goodbye' if leaving else 'Hello', name))

class Foo(object):
    spam = pySignal.ClassSignal()

    def __init__(self):
        super(Foo, self).__init__()
        # self.spam = pySignal.Signal()

        self.spam.connect(self.greet)
        self.spam.connect(greet)
        self.spam.connect(lambda name, leaving=True: greet('Lambda', leaving=True))
        self.spam.connect(partial(greet, 'partial', leaving=False))


    def greet(self, name, leaving=False):
        greet("Method", leaving)


foo1 = Foo()
foo2 = Foo()

foo1.spam.emit('Watson')
foo2.spam.emit('Sherlock')