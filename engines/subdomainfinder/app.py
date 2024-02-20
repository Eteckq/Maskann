from pydantic import BaseModel
import sublist3r

from base_engine.engine import Engine, Assets
from base_engine.utils import is_domain


class Options(BaseModel):
    tokens: str


class SubDomainFinder(Engine):
    def start_scan(self, assets: Assets, options: None, scan):
        results = []
        for asset in assets.values:
            if is_domain(asset):
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
