from ipsourcebypass import start

from base_engine.engine import Engine, Assets


class IpSourceBypass(Engine):
    def start_scan(self, assets: Assets, options: None, scan):
        results = []
        for asset in assets.values:
            # if is_url(asset):
            scan_result = start(target=asset)
            results.append({"asset": asset, "scan": scan_result})
        return results

    def example_reponse(self):
        return {
            "asset": "http://localhost:3600",
            "scan": [
                {
                    "header": "Client-IP: 127.0.0.1",
                    "status_code": 200,
                    "length": 76,
                    "curl": 'curl -k "http://localhost:3600" -H "Client-IP: 127.0.0.1" ',
                },
                {
                    "header": "Forwarded: 127.0.0.1",
                    "status_code": 201,
                    "length": 76,
                    "curl": 'curl -k "http://localhost:3600" -H "Forwarded: 127.0.0.1" ',
                },
            ],
        }


engine = IpSourceBypass()
