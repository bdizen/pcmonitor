from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic
import platform
import threading
import time
from typing import Optional


T = TypeVar('T')

class BaseMetricCollector(ABC, Generic[T]):
    def __init__(self, interval:int = 1):
        self.metric: Optional[T] = None
        self.interval = interval
        self._thread: Optional[threading.Thread] = None
        self._thread_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._metric_ready = threading.Event()
        self.system = platform.system()

    @abstractmethod
    def _collect(self) -> None:
        pass

    def start(self):
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._collect, daemon=True)
            self._thread.start()

    def stop(self, wait = False):
        self._stop_event.set()
        if self._thread and self._thread.is_alive() and wait:
            self._thread.join()

    def get_metrics(self) -> T:
        self._metric_ready.wait()
        with self._thread_lock:
            return self.metric