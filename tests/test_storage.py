from unittest import TestCase

from mypcmonitor.exporter.collectors import DiskMetricCollector, PartitionMetricCollector, StorageMetricCollector
from tests.test_collectors import test_collector


class TestDiskMetricCollector(TestCase):
    def test_collector(self):
        test_collector(DiskMetricCollector("disk0"))

class TestPartitionMetricCollector(TestCase):
    def test_collector(self):
        test_collector(PartitionMetricCollector("/dev/disk3s1s1"))

class TestStorageMetricCollector(TestCase):
    def test_collector(self):
        test_collector(StorageMetricCollector())
