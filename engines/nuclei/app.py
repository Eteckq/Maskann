from pydantic import BaseModel
import sys
import os
from os.path import isfile, join
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(sys.path[0])))
from base_engine.engine import Engine, Assets
from base_engine.utils import execute_cmd


class Options(BaseModel):
    tokens: list[str]


class Nuclei(Engine):
    def start_scan(self, assets: Assets, options: Options, scan):
        results = []
        output = execute_cmd(f"./bin/nuclei")
        results.append(output)
        return results

    def example_reponse(self):
        return {"token": "ey...", "secret": "secret_key"}


engine = Nuclei(Options, False)
