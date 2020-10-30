# PySignal

[![Build Status](https://travis-ci.org/dgovil/PySignal.svg?branch=master)](https://travis-ci.org/dgovil/PySignal)

**Deprecated**: I realize this library is used by a few people, but due to contractual limitations, I cannot currently maintain it. I recommend forking and developing the fork if possible. I apologize for the inconvenience.

For prior contributions to this repo, I made my contributions/submissions to this project solely in my personal capacity and am not conveying any rights to any intellectual property of any third parties.

-----

A Qt style signal implementation that doesn't require QObjects.
This supports class methods, functions, lambdas and partials.

Signals can either be created on the instance or on the class, and can be handled either as objects or by string name.
Unlike PyQt signals, PySignals do not enforce types by default as I believe this is more pythonic.

Available under the MIT license.

Check out my website too for more programming and film related content: http://dgovil.com/

## Install

You can install this using pip, though the version on Pypi is outdated

```bash
pip install PySignal
```

This is compatible with Python 2.7+ and 3.x

## Usage:

```python
def greet(name):
    print "Hello,", name

class Foo(object):
    started = ClassSignal()
    classSignalFactory = ClassSignalFactory()
    classSignalFactory.register('Greet')
    

    def __init__(self):
        super(Foo, self).__init__()
        self.started.connect(greet)
        self.started.emit('Watson')

        self.signalFactory = SignalFactory()
        self.signalFactory.register('Greet')
        self.signalFactory['Greet'].connect(greet)
        self.signalFactory['Greet'].emit('Sherlock')
        
        self.classSignalFactory['Greet'].connect(greet)
        self.classSignalFactory['Greet'].emit('Moriarty')
        
        ended = Signal()
        ended.connect(greet)
        ended.emit('Mycroft')

foo = Foo()
# Hello, Watson
# Hello, Sherlock
# Hello, Moriarty
# Hello, Mycroft
```

## Signal Types

There are 4 types of Signals included

* `Signal` is the base implementation of the Signal and can be created on a per instance level.
* `ClassSignal` is an object that can be created as a class variable and will act like a signal.
    This ensures that all instances of your class will have the signal, but can be managed individually.
* `SignalFactory` allows you to have a single signal object on your instance that can generate signals by name.
* `ClassSignalFactory` is the same as a signal factory but lives on the class instead of the instance.

## Why Signals?

Signals allow for creating a callback interface on your object and allows for it to be extended without needing to make a new inherited class.

For example I can define the following

```python
class Foo(object):
    started = ClassSignal()
    ended = ClassSignal()
    
    def run(self):
        self.started.emit()
        # Do my logic here
        self.ended.emit()
```

This does a few things:

* It guarantees that any instances of Foo or it's subclasses will always have the started and ended Signals. This allows for a guaranteed interface.
* It means that when we want to add callbacks to Foo, we can do so on a case by case basis without having to subclass it to call the slots explicitly.

For example:

```python
foo1 = Foo()
foo2 = Foo()

foo1.started.connect(lambda: print("I am foo1"))
foo2.started.connect(lambda: print(42))

foo1.run() # will output I am foo1
foo2.run() # will output 42
```

We can also get the Signal's "sender" - the bound method responsible for emitting the signal, if available.

For example:

```python
bar_run1 = foo1.started.sender() # will output <bound method Foo.run of <__main__.Foo object at ...>>
bar_run2 = foo2.started.sender() # will output <bound method Foo.run of <__main__.Foo object at ...>>

print(bar_run1 == foo1.run) # will output True
print(bar_run1 == foo2.run) # will output False
print(bar_run1 == bar_run2) # will output False
```

Instead of having to subclass `Foo` and implement the new behavior, we can simply reuse the existing Foo class and attach on to its instances.

## What's missing?

The goal of this library is to mimic Qt's callback system without requiring all either end of the signal/slot to be a QObject derivative.

That said in the current state it is missing the following features:

* It does not handle multiple threads. The slots are called in the same thread as the signal.
  This is because I am currently not aware of a way to do this in Python without implementing an equivalent to QObject which I am trying to avoid.
* There is no type checking. Qt requires signals to declare the type of the data they emit. This is great for C++ but I feel it's not very pythonic and so do not implement that behavior.
* You cannot query the sender. In Qt you can check what object sent a signal. Again this relies on inheriting from a QObject and Qt managing states, which are somethings I was trying to avoid. The alternative is that you can send `self` as the first parameter of the signal. e.g. `signal.emit(self, arg1, arg2)` and the slot will need to expect the first argument to be the sender.

If anyone has any suggestions or solutions on how I can overcome these caveats, I'm all ears and very willing to implement it or accept pull requests from other people too

## Comparisons To Other Libraries

There are a few other libraries to compare with that implement Signals. I am not completely familiar with them so please correct me if I am wrong.
These may serve your purposes better depending on what you are doing. The goal of PySignal is first and foremost to be a Qt style signal slot system so the comparisons are written with that in mind.

### [Blinker](https://github.com/jek/blinker)

Blinker appears to implement a very similar signal to slot mechanism. It is inspired by the django signal system.

+ It has a few more convenience methods like temporary connections and the ability to handle dispatch logic based on input
- It does not try and keep the Qt interface naming since it prefers the django system instead
- It does not appear to support partials and lambdas

### [SmokeSignal](https://github.com/shaunduncan/smokesignal/)

SmokeSignal is another django inspired signal system.

* It has a decorator based interface with a focus on slots rather than signals. ie slots listen for a signal rather than a signal calling a list of slots.
+ It has support for one time calls
+ It supports contexts that can fire signals on entry and exit.
- It does not implement a Qt style signal slot interface
- It does not appear to support partials and lambdas.

## Changelog

### 1.1.4

* Final release. This includes bugfixes from various parties but includes no contributions of my own. I am no longer able to maintain this repo. Please fork.

### 1.1.3

* Basic support for retrieving a Signal's "sender", with some test coverage.

### 1.1.1

* Setup.py no longer imports the PySignal module and instead parses it.
* Test Coverage has been expanded to 97%
* Slots can no longer be attached multiple times which used to cause them firing multiple times.
* Using callable to find if slot is lambda

### 1.0.1

* Initial Release


## Based on these implementations

http://www.jnvilo.com/cms/programming/python/programming-in-python/signal-and-slots-implementation-in-python

http://www.codeheadwords.com/2015/05/05/emulating-pyqt-signals-with-descriptors

## Contributors

Many thanks to:

* Alex Widener for cleaning up my setup.py
* Adric Worley for expanding test coverage, cleaning up the code and fixing a duplicate connection bug.
