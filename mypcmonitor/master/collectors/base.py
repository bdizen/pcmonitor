import time
from typing import Generic, TypeVar

import requests

from mypcmonitor.collectors import BaseMetricCollector
from mypcmonitor.exporter import metric_endpoint_map
from mypcmonitor.models.master import ExporterInstance

T = TypeVar("T")


class RemoteMetricCollector(BaseMetricCollector[T], Generic[T]):
    def __init__(
        self, instance: ExporterInstance, metric_class, endpoint="", interval: int = 1
    ):
        super().__init__(interval=1)
        self.instance = instance
        self.endpoint = metric_endpoint_map[metric_class]
        self.metric_class = metric_class

    def _collect(self) -> None:
        while not self._stop_event.is_set():
            # Get metrics from remote instance
            try:
                metric = self._get_remote_metrics()
            except requests.RequestException as e:
                print(e.request.url)
                print(f"Collector {T} of {self.instance.hostname} stop working")
                self._stop_event.set()
                continue
            with self._thread_lock:
                self.metric = metric
                self._metric_ready.set()
            time.sleep(self.interval)

    def _get_remote_metrics(self):
        url = f"http://{self.instance.ip_addr}:{self.instance.port}/metric/{self.endpoint}"
        print(url)
        response = requests.get(url)
        print(response)
        return self.metric_class(**response.json())
