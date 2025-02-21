"""
This module defines metric models for CPU, RAM, and disk metrics.
"""
from dataclasses import dataclass
from enum import Enum

@dataclass
class CoreMetric:
    core_id: int
    usage_percent: float
    clock_speed: float

@dataclass
class CpuMetric:
    cpu_name: str
    architecture: str
    num_cores: int
    usage_percent: float
    clock_speed: float
    temperature: float
    cores: list[CoreMetric]

@dataclass
class RamMetric:
    total_memory: int
    available_memory: int
    used_memory: int
    memory_usage: float
    total_swap: int
    used_swap: int
    swap_usage: float

class DiskType(Enum):
    HDD = "HardDisk"
    SSD = "SolidStateDrive"
    NVME = "NVMe"
    UNKNOWN = "Unknown"

@dataclass
class StorageMetric:
    capacity: int
    used_space: int
    free_space: int
    usage_percent: float

@dataclass
class PartitionMetric(StorageMetric):
    partition_name: str
    mount_point: str
    filesystem_type: str

@dataclass
class DiskMetric(StorageMetric):
    disk_name: str
    disk_type: DiskType
    read_speed: int
    write_speed: int
    iops: int
    partitions: list[PartitionMetric]

@dataclass
class NetworkMetric:
    total_rx: int
    total_tx: int
    rx_speed: int
    tx_speed: int
    packet_lost_percent: float

@dataclass
class NetworkInterfaceMetric(NetworkMetric):
    interface_name: str
    ip_address: str
    mac_address: str
