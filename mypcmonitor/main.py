import typer

from mypcmonitor.exporter.server import Exporter, ServerConfig
from mypcmonitor.master.server import Master
from mypcmonitor.ui.main import PcMonitor
from mypcmonitor.ui.master_client import MasterClient

app = typer.Typer()


@app.command()
def exporter(
    master_host: str = "0.0.0.0",
    master_port: int = 8001,
    host: str = "0.0.0.0",
    port: int = 8000,
    hostname: str = None,
):
    config = ServerConfig(ip_addr=master_host, port=master_port)
    server = Exporter(config, host, port, hostname)
    server.start()


@app.command(name="client")
def textual_ui(master_host: str = "0.0.0.0", master_port: int = 8001):
    client = MasterClient(host=master_host, port=master_port)
    tui = PcMonitor(client)
    tui.run()


@app.command()
def master(host: str = "0.0.0.0", port: int = 8001):
    server = Master(host, port)
    server.start()


if __name__ == "__main__":
    app()
