from fastapi import FastAPI
from pydantic import BaseModel
import threading
from abc import ABC, abstractmethod
import uuid
import re
from enum import Enum
from fastapi_socketio import SocketManager
import asyncio
from fastapi.responses import FileResponse
from datetime import datetime


class BaseOptions(BaseModel):
    metadata: list


class Assets(BaseModel):
    values: list[str]


class ScanStatus(Enum):
    RUNNING = "running"
    FINISHED = "finished"


class EngineStatus(Enum):
    READY = "ready"
    ERROR = "error"


class Engine(ABC):
    def __init__(self, scan_option: BaseModel = None, use_assets=True):
        self._scans = {}
        self.app = FastAPI()
        self.socket_manager = SocketManager(
            app=self.app, mount_location="/socket.io", socketio_path=""
        )
        if scan_option:
            self.scan_options = scan_option
        else:
            self.scan_options = BaseOptions
        self._setup_routes()
        self.use_assets = use_assets

    def _setup_routes(self):
        @self.app.get("/favicon.ico", include_in_schema=False)
        async def favicon():
            return FileResponse("favicon.ico")

        @self.app.get("/")
        async def get_status():
            options = {}
            for (
                attribut_name,
                attribut_type,
            ) in self.scan_options.__annotations__.items():
                if "typing.Optional" in str(attribut_type):
                    options[attribut_name] = {
                        "type": re.findall(r"\[(.*?)\]", str(attribut_type))[0],
                        "required": False,
                    }
                elif issubclass(attribut_type, Enum):
                    options[attribut_name] = {
                        "type": "enum",
                        "values": [e.value for e in attribut_type],
                        "required": True,
                    }
                else:
                    options[attribut_name] = {
                        "type": attribut_type.__name__,
                        "required": True,
                    }

            return {
                "engine": self.__class__.__name__,
                "status": self.get_status(),
                "options": options,
                "need_assets": self.use_assets,
                "example_response": self.example_reponse(),
            }

        @self.app.post("/start/")
        async def start_task(assets: Assets, options: self.scan_options):
            scan_id = str(uuid.uuid4())
            self._scans[scan_id] = {
                "scan_id": scan_id,
                "results": [],
                "status": ScanStatus.RUNNING,
                "started_at": datetime.now(),
                "finished_at": None,
                "metadata": self.scan_options.metadata,
            }
            thread = threading.Thread(
                target=asyncio.run,
                args=(
                    self._start_thread(assets=assets, options=options, scan_id=scan_id),
                ),
            )
            self._scans[scan_id]["thread"] = thread
            thread.start()

            return {"scan_id": scan_id}

        @self.app.get("/scans/")
        async def get_scans():
            await self._update_scans()
            return {
                "finished_jobs": [
                    t
                    for t in self._scans
                    if self._scans[t]["status"] == ScanStatus.FINISHED
                ],
                "running_jobs": [
                    t
                    for t in self._scans
                    if self._scans[t]["status"] == ScanStatus.RUNNING
                ],
            }

        @self.app.get("/scans/{scan_id}")
        def get_job_result(scan_id):
            scan = self._get_scan_by_id(scan_id)
            if scan["status"] != ScanStatus.FINISHED:
                return {"error": f"scan is {scan['status']}"}

            return self.get_job_result(scan_id)

        @self.app.delete("/scans/{scan_id}")
        def delete_job_result(scan_id):
            scan = self._get_scan_by_id(scan_id)
            if not scan:
                return {"error": "scan not found"}

            self._scans.pop(scan_id)
            return {"success": "ok"}

    def get_job_result(self, scan_id):
        scan = self._get_scan_by_id(scan_id)
        if not scan:
            return {"error": "scan not found"}

        results = scan["results"]
        started_at = scan["started_at"]
        finished_at = scan["finished_at"]
        return {
            "results": results,
            "from": self.__class__.__name__,
            "id": scan_id,
            "started_at": started_at,
            "finished_at": finished_at,
        }

    async def _update_scans(self):
        ct = threading.current_thread()
        for scan_id in self._scans:
            scan = self._get_scan_by_id(scan_id)
            t = scan["thread"]
            if ct == t or (
                not t.is_alive() and scan["status"] is not ScanStatus.FINISHED
            ):
                scan["status"] = ScanStatus.FINISHED
                scan["finished_at"] = datetime.now()

                await self.socket_manager.emit("scan-finished", scan_id)

    def _get_scan_by_id(self, scan_id):
        return self._scans.get(scan_id, None)

    async def _start_thread(self, assets: Assets, options, scan_id):
        scan = self._get_scan_by_id(scan_id)
        scan["results"] += self.start_scan(assets, options, scan)
        await self._update_scans()
        return True

    def get_status(self) -> EngineStatus:
        return EngineStatus.READY

    @abstractmethod
    def start_scan(self, assets: Assets, options, scan):
        pass

    @abstractmethod
    def example_reponse(self):
        pass
