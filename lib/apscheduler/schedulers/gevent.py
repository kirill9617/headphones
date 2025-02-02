

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.base import BaseScheduler

try:
    from gevent.event import Event
    from gevent.lock import RLock
    import gevent
except ImportError:  # pragma: nocover
    raise ImportError('GeventScheduler requires gevent installed')


class GeventScheduler(BlockingScheduler):
    """A scheduler that runs as a Gevent greenlet."""

    _greenlet = None

    def start(self):
        BaseScheduler.start(self)
        self._event = Event()
        self._greenlet = gevent.spawn(self._main_loop)
        return self._greenlet

    def shutdown(self, wait=True):
        super(GeventScheduler, self).shutdown(wait)
        self._greenlet.join()
        del self._greenlet

    def _create_lock(self):
        return RLock()

    def _create_default_executor(self):
        from apscheduler.executors.gevent import GeventExecutor
        return GeventExecutor()
