# PySignal

A Qt style signal implementation that doesn't require QObjects.
This supports class methods, functions, lambdas and partials.

Signals can either be created on the instance or on the class, and can be handled either as objects or by string name.
Unlike PyQt signals, PySignals do not enforce types by default as I believe this is more pythonic.

## Usage:

```python
def greet(name):
    print "Hello,", name

class Foo(object):
    started = ClassSignal()

    def __init__(self):
        super(Foo, self).__init__()
        self.started.connect(greet)
        self.started.emit('Watson')

foo = Foo()
# Hello, Watson
```

## Based on these implementations

http://www.jnvilo.com/cms/programming/python/programming-in-python/signal-and-slots-implementation-in-python

http://www.codeheadwords.com/2015/05/05/emulating-pyqt-signals-with-descriptors