from unittest import TestCase

from mypcmonitor.core.network import NetworkMetricCollector
from tests.test_collectors import test_collector


class TestNetworkMetricCollector(TestCase):
    def test_collector(self):
        test_collector(NetworkMetricCollector())
