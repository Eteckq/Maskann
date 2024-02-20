from pydantic import BaseModel

from base_engine.engine import Engine, Assets
from base_engine.utils import execute_cmd


class Options(BaseModel):
    tokens: list[str]


class Nuclei(Engine):
    def start_scan(self, assets: Assets, options: Options, scan):
        results = []
        output = execute_cmd("./bin/nuclei")
        results.append(output)
        return results

    def example_reponse(self):
        return {"token": "ey...", "secret": "secret_key"}


engine = Nuclei(Options, False)
