import hashlib

from pydantic.dataclasses import dataclass

from mypcmonitor.collectors import BaseMetricCollector
from mypcmonitor.models import (CpuMetric, NetworkMetric, RamMetric,
                                StorageMetric)


@dataclass(frozen=True)
class ExporterInstance:
    ip_addr: str
    port: int
    hostname: str

    @property
    def id(self):
        unique_string = f"{self.ip_addr}:{self.port}:{self.hostname}"
        return hashlib.md5(unique_string.encode()).hexdigest()


class InstanceCollectors:
    cpu: BaseMetricCollector[CpuMetric]
    memory: BaseMetricCollector[RamMetric]
    storage: BaseMetricCollector[StorageMetric]
    network: BaseMetricCollector[NetworkMetric]
    started = False

    def __init__(
        self,
        cpu: BaseMetricCollector[CpuMetric],
        memory: BaseMetricCollector[RamMetric],
        storage: BaseMetricCollector[StorageMetric],
        network: BaseMetricCollector[NetworkMetric],
    ):
        self.cpu: BaseMetricCollector[CpuMetric] = cpu
        self.memory: BaseMetricCollector[RamMetric] = memory
        self.storage: BaseMetricCollector[StorageMetric] = storage
        self.network: BaseMetricCollector[NetworkMetric] = network
        self.started = False

    def start(self):
        print("Collectors starting")
        self.cpu.start()
        self.memory.start()
        self.storage.start()
        self.network.start()
        self.started = True

    def stop(self):
        print("Collectors stopping")
        self.cpu.stop()
        self.memory.stop()
        self.storage.stop()
        self.network.stop()

    def get_metrics(self):
        if self.started:
            return {
                "cpu": self.cpu.get_metrics(),
                "memory": self.memory.get_metrics(),
                "storage": self.storage.get_metrics(),
                "network": self.network.get_metrics(),
            }
        return None
