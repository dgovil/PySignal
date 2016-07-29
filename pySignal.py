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
        self._slots = []


    def emit(self, *args, **kwargs):
        """
        Calls all the connected slots with the provided args and kwargs unless block is activated
        """

        if self._block:
            return

        for slot in self._slots:
            if not slot:
                continue
            elif isinstance(slot, partial):
                slot()
            elif isinstance(slot, weakref.WeakKeyDictionary):
                for obj, method in slot.items():
                    method(obj, *args, **kwargs)
            elif isinstance(slot, weakref.ref):
                slot()(*args, **kwargs)
            else:
                slot(*args, **kwargs)

    def connect(self, slot):
        """
        Connects the signal to any callable object
        """
        if isinstance(slot, partial) or '<' in slot.__name__:
            self._slots.append(slot)
        elif inspect.ismethod(slot):
            slotSelf = slot.__self__
            slotDict = weakref.WeakKeyDictionary()
            slotDict[slotSelf] = slot.__func__
            self._slots.append(slotDict)
        else:
            self._slots.append(weakref.ref(slot))

    def disconnect(self, slot):
        """
        Disconnects the slot from the signal
        """

        if inspect.ismethod(slot):
            slotSelf = slot.__self__
            for _slot in self._slots:
                if isinstance(_slot, weakref.WeakKeyDictionary) and slotSelf in _slot:
                    self._slots.remove(slot)
        elif slot in self._slots:
                self._slots.remove(slot)

    def clear(self):
        """Clears the signal of all connected slots"""
        self._slots = []

    def block(self, value):
        """Sets blocking of the signal"""
        self._block = bool(value)

