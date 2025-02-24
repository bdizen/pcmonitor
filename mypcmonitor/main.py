import requests
import typer

from mypcmonitor.exporter.server import Exporter, ServerConfig
from mypcmonitor.master.server import Master
from mypcmonitor.ui.main import PcMonitor
from mypcmonitor.ui.master_client import MasterClient

app = typer.Typer()


@app.command()
def exporter(
    master_host="0.0.0.0", master_port=8001, host="0.0.0.0", port=8000, hostname=None
):
    config = ServerConfig(ip_addr=master_host, port=master_port)
    exporter = Exporter(config, host, port, hostname)
    exporter.start()


@app.command(name="client")
def textual_ui(master_host="0.0.0.0", master_port=8001):
    client = MasterClient(host=master_host, port=master_port)
    tui = PcMonitor(client)
    tui.run()


@app.command()
def master(host="0.0.0.0", port=8001):
    master = Master(host, port)
    master.start()


if __name__ == "__main__":
    app()
