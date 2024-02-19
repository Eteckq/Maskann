from pydantic import BaseModel
import sys
import os
from os.path import isfile, join
import shutil
import sublist3r

sys.path.insert(0, os.path.join(os.path.dirname(sys.path[0])))
from base_engine.engine import Engine, Assets
from base_engine.utils import execute_cmd


class Options(BaseModel):
    tokens: str


class SubDomainFinder(Engine):
    def start_scan(self, assets: Assets, options: None, scan):
        results = []
        for asset in assets.values:
            # if is_url(asset):
            scan_result = sublist3r.main(
                asset,
                40,
                "/dev/null",
                ports=None,
                silent=False,
                verbose=False,
                enable_bruteforce=False,
                engines=None,
            )
            results.append({"asset": asset, "scan": scan_result})
        return results

    def example_reponse(self):
        return {
            "asset": "yohangastoud.fr",
            "scan": [
                "www.yohangastoud.fr",
                "adminer.yohangastoud.fr",
                "api.yohangastoud.fr",
            ],
        }


engine = SubDomainFinder()
