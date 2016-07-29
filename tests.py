import pySignal
from functools import partial

def greet(name, leaving=False):
    print("%s, %s" % ('Goodbye' if leaving else 'Hello', name))

class Foo(object):
    def __init__(self):
        super(Foo, self).__init__()
        self.spam = pySignal.Signal()

        self.spam.connect(self.greet)
        self.spam.connect(greet)
        self.spam.connect(lambda name, leaving: greet('Lambda', leaving=True))
        self.spam.connect(partial(greet, 'partial', leaving=False))
        self.spam.emit("Watson", leaving=True)

    def greet(self, name, leaving=False):
        greet("Method", leaving)


foo = Foo()
