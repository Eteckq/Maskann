from pydantic import BaseModel
import sys
import os
from os.path import isfile, join
import whois
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(sys.path[0])))
from base_engine.engine import Engine, Assets
from base_engine.utils import is_domain


class Options(BaseModel):
    tokens: str


class WhoIs(Engine):
    def start_scan(self, assets: Assets, options: None, scan):
        results = []
        for asset in assets.values:
            if is_domain(asset):
                scan_result = whois.whois(asset)
                results.append({"asset": asset, "scan": scan_result})
        return results

    def example_reponse(self):
        return {
            "asset": "yohangastoud.fr",
            "scan": {
                "domain_name": "yohangastoud.fr",
                "registrar": "OVH",
                "creation_date": datetime.datetime(2019, 3, 22, 16, 16, 43),
                "expiration_date": datetime.datetime(2025, 3, 22, 16, 16, 43),
                "name_servers": ["dns20.ovh.net", "ns20.ovh.net"],
                "status": [
                    "ACTIVE",
                    "renewPeriod",
                    "active",
                    "associated",
                    "not identified",
                ],
                "emails": ["support@ovh.net", "tech@ovh.net"],
                "updated_date": datetime.datetime(2024, 2, 19, 14, 2, 18, 983790),
            },
        }


engine = WhoIs()
