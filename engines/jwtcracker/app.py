import os
from os.path import isfile, join
import shutil

from base_engine.engine import Engine, Assets, BaseOptions
from base_engine.utils import execute_cmd


class Options(BaseOptions):
    tokens: list[str]


class JwtCracker(Engine):
    def start_scan(self, assets: Assets, options: Options, scan):
        results = []
        base_dir = scan["scan_id"]
        os.mkdir(base_dir)
        f = open(f"{base_dir}/tokens.txt", "w")
        f.write("\n".join(options.tokens))
        f.close()
        wordlists = [
            f for f in os.listdir("./wordlists") if isfile(join("./wordlists", f))
        ]
        for wordlist in wordlists:
            output = execute_cmd(
                f"./bin/gojwtcrack -t {base_dir}/tokens.txt -d ./wordlists/{wordlist}"
            )
            output = output.stdout.split(b"\t")
            if len(output) > 1:
                results.append({"token": output[1], "secret": output[0]})
        shutil.rmtree(base_dir)

        return results

    def example_reponse(self):
        return {"token": "ey...", "secret": "secret_key"}


engine = JwtCracker(Options, False)
