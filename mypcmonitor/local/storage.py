from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static, Label

from mypcmonitor.local import cpu_collector, storage_collector
from mypcmonitor.models.metrics import DiskMetric, PartitionMetric


class DriveDisplay(Static):
    def update(self, metric: DiskMetric) -> None:
        super().update(f"[bold]Name:[/bold] {metric.disk_name}\n"
                        f"[bold]Type:[/bold] {str(metric.disk_type)}\n"
                        f"[bold]Size:[/bold] {metric.capacity}\n"
                        f"[bold]Read:[/bold] {metric.read_speed}\n" 
                        f"[bold]Write:[/bold] {metric.write_speed}\n"
                        f"[bold]IOPS:[/bold] {metric.iops}"
        )

class PartitionDisplay(Static):
    def update(self, metric: PartitionMetric) -> None:
        super().update(f"[bold]Name:[/bold] {metric.partition_name}\n"
                        f"[bold]Size:[/bold] {metric.capacity}\n"
                        f"[bold]Used:[/bold] {metric.used_space}\n" 
                        f"[bold]Free:[/bold] {metric.free_space}\n"
                        f"[bold]Usage:[/bold] {metric.usage_percent}%\n"
                        f"[bold]Mount point:[/bold] {metric.mount_point}\n"
                        f"[bold]Filesystem:[/bold] {metric.filesystem_type}"
        )

class StorageView(Container):
    def compose(self) -> ComposeResult:
        yield Vertical(
        Label("Disks:"),
        Container(id="disks-container"),
        Label("Partitions:"),
        Container(id="parts-container"))

    def on_mount(self):
        storage_metric = storage_collector.get_metrics()
        disks_container = self.query_one("#disks-container")
        parts_container = self.query_one("#parts-container")
        for disk in storage_metric.disks:
            disks_container.mount(
                Vertical(
                    DriveDisplay(id=disk.disk_name),
                    classes="disk-box"
                )
            )
        for part in storage_metric.partitions:
            parts_container.mount(
                Vertical(
                    PartitionDisplay(id=part.partition_name),
                    classes="part-box"
                )
            )
        self.set_interval(1, self.update_stats)


    def update_stats(self) -> None:
        storage_metric = storage_collector.get_metrics()
        for disk in storage_metric.disks:
            self.query_one(f"#{disk.disk_name}", DriveDisplay).update(disk)
        for part in storage_metric.partitions:
            self.query_one(f"#{part.partition_name}", PartitionDisplay).update(part)
