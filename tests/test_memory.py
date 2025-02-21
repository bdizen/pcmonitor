from unittest import TestCase
from dataclasses import asdict
from pprint import pprint
import time
from pcmonitor.core.memory import MemoryMetricCollector


class TestMemoryMetricCollector(TestCase):
    def test_collector(self):
        collector = MemoryMetricCollector()
        collector.start()

        try:
            while True:
                metrics = collector.get_metrics()
                if metrics:
                    pprint(asdict(metrics))
                time.sleep(1)
        except KeyboardInterrupt:
            collector.stop()
            print("\nStopped metric collection")
