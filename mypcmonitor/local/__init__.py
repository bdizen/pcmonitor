from mypcmonitor.exporter.collectors import CpuMetricCollector
from mypcmonitor.exporter.collectors import MemoryMetricCollector
from mypcmonitor.exporter.collectors import StorageMetricCollector

cpu_collector = CpuMetricCollector()
mem_collector = MemoryMetricCollector()
storage_collector = StorageMetricCollector()