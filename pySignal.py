import inspect
import weakref
from functools import partial


class Signal(object):
    """
    A Qt style signal implementation that doesn't require QObjects.
    Unlike Qt, this must be instantiated as an instance variable and not as a class variable
        otherwise every instance will share one signal object

    Usage:

    ```python
    def greet(name):
        print "Hello,", name

    class Foo(object):
        def __init__(self):
            super(Foo, self).__init__()
            self.started = Signal(self)
            self.started.connect(greet)
            self.started.emit('Watson')

    foo = Foo()
    # Hello, Watson
    ```

    Based on these implementations

    http://www.jnvilo.com/cms/programming/python/programming-in-python/signal-and-slots-implementation-in-python

    http://www.codeheadwords.com/2015/05/05/emulating-pyqt-signals-with-descriptors

    """

    def __init__(self):
        super(Signal, self).__init__()
        self._block = False
        self._lambdas = []
        self._partials = []
        self._functions = weakref.WeakSet()
        self._methods = weakref.WeakKeyDictionary()

    def emit(self, *args, **kwargs):
        """
        Calls all the connected slots with the provided args and kwargs unless block is activated
        """

        if self._block:
            return

        for func in self._partials:
            func()

        for func in self._lambdas:
            func(*args, **kwargs)

        for func in self._functions:
            func(*args, **kwargs)

        for obj, funcs in self._methods.items():
            for func in funcs:
                func(obj, *args, **kwargs)

    def connect(self, slot):
        """
        Connects the signal to any callable object
        """
        if isinstance(slot, partial):
            self._partials.append(slot)
        elif hasattr(slot, 'func_name') and slot.func_name == '<lambda>':
            self._lambdas.append(slot)
        elif inspect.ismethod(slot):
            slotSelf = slot.__self__
            self._methods.setdefault(slotSelf, set()).add(slot.__func__)
        else:
            self._functions.add(slot)

    def disconnect(self, slot):
        """
        Disconnects the slot from the signal
        """
        if isinstance(slot, partial):
            self._partials.remove(slot)
        elif hasattr(slot, 'func_name') and slot.func_name == '<lambda>':
            self._lambdas.remove(slot)
        elif inspect.ismethod(slot):
            slotSelf = slot.__self__
            if slotSelf in self._methods:
                self._methods[slotSelf].remove(slot.__func__)

        else:
            if slot in self._functions:
                self._functions.remove(slot)

    def clear(self):
        """Clears the signal of all connected slots"""
        self._functions.clear()
        self._methods.clear()

    def block(self, value):
        """Sets blocking of the signal"""
        self._block = bool(value)

