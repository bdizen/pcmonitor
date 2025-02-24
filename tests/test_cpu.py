from unittest import TestCase

from mypcmonitor.exporter.collectors import CpuMetricCollector
from tests.test_collectors import test_collector


class TestCpuMetricCollector(TestCase):
    def test_collector(self):
        test_collector(CpuMetricCollector())
