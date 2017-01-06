__author__ = "Dhruv Govil"
__copyright__ = "Copyright 2016, Dhruv Govil"
__credits__ = ["Dhruv Govil", "John Hood", "Jason Viloria", "Adric Worley", "Alex Widener"]
__license__ = "MIT"
__version__ = "1.1.1"
__maintainer__ = "Dhruv Govil"
__email__ = "dhruvagovil@gmail.com"
__status__ = "Beta"

import inspect
import weakref
from functools import partial


class Signal(object):
    """
    The Signal is the core object that handles connection and emission .
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
                # For class methods, get the class object and call the method accordingly.
                for obj, method in slot.items():
                    method(obj, *args, **kwargs)
            elif isinstance(slot, weakref.ref):
                # If it's a weakref, call the ref to get the instance and then call the func
                # Don't wrap in try/except so we don't risk masking exceptions from the actual func call
                if (slot() is not None):
                    slot()(*args, **kwargs)
            else:
                # Else call it in a standard way. Should be just lambdas at this point
                slot(*args, **kwargs)

    def connect(self, slot):
        """
        Connects the signal to any callable object
        """
        if not callable(slot):
            raise ValueError("Connection to non-callable '%s' object failed" % slot.__class__.__name__)

        if (isinstance(slot, partial) or '<' in slot.__name__):
            # If it's a partial or a lambda. The '<' check is the only py2 and py3 compatible way I could find
            if slot not in self._slots:
                self._slots.append(slot)
        elif inspect.ismethod(slot):
            # Check if it's an instance method and store it with the instance as the key
            slotSelf = slot.__self__
            slotDict = weakref.WeakKeyDictionary()
            slotDict[slotSelf] = slot.__func__
            if slotDict not in self._slots:
                self._slots.append(slotDict)
        else:
            # If it's just a function then just store it as a weakref.
            newSlotRef = weakref.ref(slot)
            if newSlotRef not in self._slots:
                self._slots.append(newSlotRef)

    def disconnect(self, slot):
        """
        Disconnects the slot from the signal
        """
        if not callable(slot):
            return

        if inspect.ismethod(slot):
            # If it's a method, then find it by its instance
            slotSelf = slot.__self__
            for s in self._slots:
                if isinstance(s, weakref.WeakKeyDictionary) and (slotSelf in s) and (s[slotSelf] is slot.__func__):
                    self._slots.remove(s)
                    break
        elif isinstance(slot, partial) or '<' in slot.__name__:
            # If it's a partial or lambda, try to remove directly
            try:
                self._slots.remove(slot)
            except ValueError:
                pass
        else:
            # It's probably a function, so try to remove by weakref
            try:
                self._slots.remove(weakref.ref(slot))
            except ValueError:
                pass

    def clear(self):
        """Clears the signal of all connected slots"""
        self._slots = []

    def block(self, isBlocked):
        """Sets blocking of the signal"""
        self._block = bool(isBlocked)


class ClassSignal(object):
    """
    The class signal allows a signal to be set on a class rather than an instance.
    This emulates the behavior of a PyQt signal
    """
    _map = {}

    def __get__(self, instance, owner):
        tmp = self._map.setdefault(self, weakref.WeakKeyDictionary())
        return tmp.setdefault(instance, Signal())

    def __set__(self, instance, value):
        raise RuntimeError("Cannot assign to a Signal object")


class SignalFactory(dict):
    """
    The Signal Factory object lets you handle signals by a string based name instead of by objects.
    """
    def register(self, name, *slots):
        """
        Registers a given signal
        :param name: the signal to register
        """
        # setdefault initializes the object even if it exists. This is more efficient
        if name not in self:
            self[name] = Signal()

        for slot in slots:
            self[name].connect(slot)

    def deregister(self, name):
        """
        Removes a given signal
        :param name: the signal to deregister
        """
        self.pop(name, None)

    def emit(self, signalName, *args, **kwargs):
        """
        Emits a signal by name if it exists. Any additional args or kwargs are passed to the signal
        :param signalName: the signal name to emit
        """
        assert signalName in self, "%s is not a registered signal" % signalName
        self[signalName].emit(*args, **kwargs)

    def connect(self, signalName, slot):
        """
        Connects a given signal to a given slot
        :param signalName: the signal name to connect to
        :param slot: the callable slot to register
        """
        assert signalName in self, "%s is not a registered signal" % signalName
        self[signalName].connect(slot)

    def block(self, signals=None, isBlocked=True):
        """
        Sets the block on any provided signals, or to all signals

        :param signals: defaults to all signals. Accepts either a single string or a list of strings
        :param isBlocked: the state to set the signal to
        """
        if signals:
            try:
                if isinstance(signals, basestring):
                    signals = [signals]
            except NameError:
                if isinstance(signals, str):
                    signals = [signals]

        signals = signals or self.keys()

        for signal in signals:
            if signal not in self:
                raise RuntimeError("Could not find signal matching %s" % signal)
            self[signal].block(isBlocked)


class ClassSignalFactory(object):
    """
    The class signal allows a signal factory to be set on a class rather than an instance.
    """
    _map = {}

    def __get__(self, instance, owner):
        tmp = self._map.setdefault(self, weakref.WeakKeyDictionary())
        return tmp.setdefault(instance, SignalFactory())

    def __set__(self, instance, value):
        raise RuntimeError("Cannot assign to a Signal object")
