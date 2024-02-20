from pydantic import BaseModel
import pydig
from enum import Enum

from base_engine.engine import Engine, Assets
from base_engine.utils import is_domain


class TypeDig(str, Enum):
    A = "A"
    AAAA = "AAAA"
    CAA = "CAA"
    CNAME = "CNAME"
    DNSKEY = "DNSKEY"
    DS = "DS"
    MX = "MX"
    NS = "NS"
    PTR = "PTR"
    SOA = "SOA"
    SRV = "SRV"
    TLSA = "TLSA"
    TSIG = "TSIG"
    TXT = "TXT"


class Options(BaseModel):
    type_dig: TypeDig

class Dig(Engine):
    def start_scan(self, assets: Assets, options: Options, scan):
        results = []
        for asset in assets.values:
            if is_domain(asset):
                scan_result = pydig.query(asset, options.type_dig)
                results.append(
                    {"asset": asset, "dig_type": options.type_dig, "scan": scan_result}
                )
        return results

    def example_reponse(self):
        return {
            "asset": "yohangastoud.fr",
            "dig_type": "SOA",
            "scan": ["dns20.ovh.net. tech.ovh.net. 2023050700 86400 3600 3600000 300"],
        }


engine = Dig(Options)
