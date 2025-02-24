import asyncio
import json
import socket

import httpx
import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic.dataclasses import dataclass
from pydantic.v1.json import pydantic_encoder

from mypcmonitor.exporter.collectors import (CpuMetricCollector,
                                             MemoryMetricCollector,
                                             NetworkMetricCollector,
                                             StorageMetricCollector)
from mypcmonitor.models import ExporterInstance, InstanceCollectors


@dataclass
class ServerConfig:
    ip_addr: str
    port: int


class Exporter:
    def __init__(
        self,
        master: ServerConfig,
        host="0.0.0.0",
        port=8000,
        hostname: str | None = None,
    ):
        self.host = host
        self.port = port
        self.hostname = hostname if hostname else socket.gethostname()
        self.master = master

        self.app = FastAPI()
        self.router = APIRouter()
        self.setup_routes()
        self.app.include_router(self.router)
        self.server = uvicorn.Server(uvicorn.Config(self.app, host=host, port=port))
        self.collectors = InstanceCollectors(
            cpu=CpuMetricCollector(),
            memory=MemoryMetricCollector(),
            storage=StorageMetricCollector(),
            network=NetworkMetricCollector(),
        )

    def setup_routes(self):
        @self.app.on_event("startup")
        async def startup_event():
            async def register_master():
                await asyncio.sleep(3)
                me = ExporterInstance(
                    ip_addr=self.host, port=self.port, hostname=self.hostname
                )
                url = f"http://{self.master.ip_addr}:{self.master.port}/register"
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url, json=json.loads(json.dumps(me, default=pydantic_encoder))
                    )
                    print(response.json())

            # To run the task in background after the server accepting requests
            asyncio.create_task(register_master())

        @self.router.get("/metric/{metric_type}")
        def get_metric(metric_type: str):
            if not hasattr(self.collectors, metric_type):
                raise HTTPException(status_code=404, detail="No such metric")
            collector = getattr(self.collectors, metric_type)
            return collector.get_metrics()

        @self.router.get("/health")
        def health_check():
            return {"status": "ok"}

    def start(self):
        self.collectors.start()
        self.server.run()
        self.collectors.stop()

    def stop(self):
        self.server.should_exit = True
