# PySignal

A Qt style signal implementation that doesn't require QObjects.
Unlike Qt, this must be instantiated as an instance variable and not as a class variable otherwise every instance will share one signal object

This supports class methods, functions, lambdas and partials

## Usage:

```python
def greet(name):
    print "Hello,", name

class Foo(object):
    def __init__(self):
        super(Foo, self).__init__()
        self.started = Signal()
        self.started.connect(greet)
        self.started.emit('Watson')

foo = Foo()
# Hello, Watson
```

## Based on these implementations

http://www.jnvilo.com/cms/programming/python/programming-in-python/signal-and-slots-implementation-in-python

http://www.codeheadwords.com/2015/05/05/emulating-pyqt-signals-with-descriptors