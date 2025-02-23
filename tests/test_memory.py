from unittest import TestCase
from mypcmonitor.core.memory import MemoryMetricCollector
from tests.test_collectors import test_collector


class TestMemoryMetricCollector(TestCase):
    def test_collector(self):
        test_collector(MemoryMetricCollector())
