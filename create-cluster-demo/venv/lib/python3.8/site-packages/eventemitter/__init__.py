__version__ = "2.1"
__author__ = "Rossen Georgiev"

from collections import defaultdict, OrderedDict
import gevent
from gevent.event import AsyncResult
from gevent.queue import Queue


class EventEmitter(object):
    """
    Implements event emitter using ``gevent`` module.
    Every callback is executed via :meth:`gevent.spawn`.
    """
    __worker = None

    def emit(self, event, *args):
        """
        Emit event with some arguments

        :param event: event identifier
        :type event: any type
        :param args: any or no arguments
        """
        if hasattr(self, '_EventEmitter__callbacks'):
            self.__queue.put((event, args))
            self.__queue.put((None, (event,) + args))

            if self.__worker is None or self.__worker.ready():
                self.__worker = gevent.spawn(self.__emit_worker)

    def __emit_worker(self):
        for event, args in self.__queue:
            if hasattr(self, '_EventEmitter__callbacks'):
                if event in self.__callbacks:
                    for callback, once in list(self.__callbacks[event].items()):
                        if once:
                            self.remove_listener(event, callback)
                        if isinstance(callback, AsyncResult):
                            callback.set(args)
                        else:
                            gevent.spawn(callback, *args)

                        gevent.idle()

            if self.__queue.empty():
                break

    def on(self, event, callback=None, once=False):
        """
        Registers a callback for the specified event

        :param event: event name
        :param callback: callback function

        Can be as function decorator if only ``event`` param is specified.

        .. code:: python

            @instaceOfSomeClass.on("some event")
            def handle_event():
                pass

            instaceOfSomeClass.on("some event", handle_event)

        To listen for any event, use :class:`None` as event identifier.
        """

        if not hasattr(self, '_EventEmitter__callbacks'):
            self.__callbacks = defaultdict(OrderedDict)
            self.__queue = Queue()

        # when used function
        if callback:
            self.__callbacks[event][callback] = once
            return

        # as decorator
        def wrapper(callback):
            self.__callbacks[event][callback] = once
            return callback
        return wrapper

    def once(self, event, callback=None):
        """
        Register a callback, but call it exactly one time

        See :meth:`eventemitter.EventEmitter.on`
        """
        return self.on(event, callback, once=True)


    def wait_event(self, event, timeout=None, raises=False):
        """
        Blocks until an event and returns the results

        :param event: event identifier
        :param timeout: (optional)(default:None) seconds to wait
        :type timeout: :class:`int`
        :param raises: (optional)(default:False) On timeout if ``False`` return ``None``, else raise ``gevent.Timeout``
        :type raises: :class:`bool`
        :return: returns event arguments in tuple
        :rtype: :class:`None`, or :class:`tuple`
        :raises: ``gevent.Timeout``

        Handling timeout

        .. code:: python

            args = ee.wait_event('my event', timeout=5)
            if args is None:
                print "Timeout!"

        """
        result = AsyncResult()
        self.once(event, result)

        try:
            return result.get(True, timeout)
        except gevent.Timeout:
            self.remove_listener(event, result)

            if raises:
                raise
            else:
                return None

    def remove_listener(self, event, callback):
        """
        Removes callback for the specified event

        :param event: event identifier
        :param callback: callback reference
        :type callback: function, method or :class:`gevent.event.AsyncResult`
        """

        if hasattr(self, '_EventEmitter__callbacks'):
            if event in self.__callbacks:
                del self.__callbacks[event][callback]

                if not self.__callbacks[event]:
                    del self.__callbacks[event]

    def remove_all_listeners(self, event=None):
        """
        Removes all registered callbacks, or all
        registered callbacks for a specific event

        :param event: event identifier
        """
        if hasattr(self, '_EventEmitter__callbacks'):
            if event is None:
                self.__callbacks.clear()
            else:
                if event in self.__callbacks:
                    del self.__callbacks[event]

    def count_listeners(self, event):
        """
        Returns a count of how many listeners are
        registered registed for a specific event

        :param event: event identifier
        :returns: number of listeners
        :rtype: int
        """
        if hasattr(self, '_EventEmitter__callbacks'):
            if event in self.__callbacks:
                return len(self.__callbacks[event])

        return 0


