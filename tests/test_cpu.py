from unittest import TestCase
from dataclasses import asdict
from pprint import pprint
import time
from pcmonitor.core.cpu import CpuMetricCollector


class TestCpuMetricCollector(TestCase):
    def test_collector(self):
        collector = CpuMetricCollector()
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
