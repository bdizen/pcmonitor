import json
import threading
import time

import requests
import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic.v1.json import pydantic_encoder

from mypcmonitor.master.collectors import RemoteMetricCollector
from mypcmonitor.models import (CpuMetric, ExporterInstance,
                                InstanceCollectors, NetworkMetric, RamMetric,
                                StorageMetric)


class Master:
    def __init__(self, host="0.0.0.0", port=8001):
        self.app = FastAPI()
        self.router = APIRouter()
        self.setup_routes()
        self.app.include_router(self.router)
        self.server = uvicorn.Server(uvicorn.Config(self.app, host=host, port=port))
        self.instances: dict[str, ExporterInstance] = {}
        self.collectors = {}
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self.liveliness = threading.Thread(target=self.unregister)

    def setup_routes(self):
        @self.router.get("/stop/")
        def get_stop():
            return self._stop_event.is_set()

        @self.router.get("/thread/")
        def get_stop():
            if not self.liveliness:
                return None
            return self.liveliness.is_alive()

        @self.router.post("/register")
        def register_instance(instance: ExporterInstance):
            print(instance)
            if instance.id in self.instances:
                return {
                    "status": "failed",
                    "message": f"Machine {instance.hostname} already registered",
                }

            collectors = InstanceCollectors(
                cpu=RemoteMetricCollector[CpuMetric](instance, CpuMetric),
                memory=RemoteMetricCollector[RamMetric](instance, RamMetric),
                storage=RemoteMetricCollector[StorageMetric](instance, StorageMetric),
                network=RemoteMetricCollector[NetworkMetric](instance, NetworkMetric),
            )
            collectors.start()

            with self._lock:
                self.collectors[instance] = collectors
                self.instances[instance.id] = instance
            return {
                "status": "success",
                "message": f"Machine {instance.hostname} registered successfully",
            }

        @self.router.get("/instances/")
        def get_instances(online: bool = False):
            return list(self.instances.values())

        @self.router.get("/instances/{instance}")
        def get_instances(instance: str):
            if instance not in self.instances:
                raise HTTPException(status_code=404, detail="Instance not exists")
            return json.loads(
                json.dumps(self.instances[instance], default=pydantic_encoder)
            )

        @self.router.get("/instances/{instance}/metrics")
        def get_instances(instance: str):
            if instance not in self.instances:
                raise HTTPException(status_code=404, detail="Instance not exists")
            return self.collectors[self.instances[instance]].get_metrics()

        @self.router.get("/instances/{instance}/metrics/{metric_type}")
        def get_instances(instance: str, metric_type):
            if instance not in self.instances or not hasattr(
                self.collectors[self.instances[instance]], metric_type
            ):
                raise HTTPException(status_code=404, detail="Instance not exists")
            return getattr(
                self.collectors[self.instances[instance]], metric_type
            ).get_metrics()

        @self.router.get("/health")
        def health_check():
            return {"status": "ok"}

    def unregister(self):
        while not self._stop_event.is_set():
            with self._lock:
                instances = [instance for instance in self.instances.values()]
                for instance in instances:
                    try:
                        url = f"http://{instance.ip_addr}:{instance.port}/health"
                        response = requests.get(url)
                        data = response.json()
                        if data.get("status") != "ok":
                            print(f"Unregister instance {instance.hostname} is not ok ")
                            self.collectors.pop(instance)
                            self.instances.pop(instance.id)
                            break
                    except requests.RequestException as e:
                        print(f"Unregister instance {instance.hostname} is offline ")
                        self.collectors.pop(instance)
                        self.instances.pop(instance.id)

                time.sleep(1)

    def start(self):
        self.liveliness.start()
        self.server.run()

    def stop(self):
        self._stop_event.set()
        self.server.should_exit = True
