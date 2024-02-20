from pydantic import BaseModel
import json

from base_engine.engine import Engine, Assets
from base_engine.utils import execute_cmd


class Options(BaseModel):
    template: str


class Nuclei(Engine):
    def start_scan(self, assets: Assets, options: Options, scan):
        results = []
        cmd = f"./bin/nuclei -j -t {options.template} "
        for asset in assets.values:
            cmd += f"-u {asset} "
        print(cmd)
        output = execute_cmd(cmd)
        print(output.stdout)
        if output.stdout:
            results.append(json.loads(output.stdout))
        return results

    def example_reponse(self):
        return {
            "template": "http/technologies/nginx/nginx-version.yaml",
            "template-url": "https://github.com/projectdiscovery/nuclei-templates/blob/main/http/technologies/nginx/nginx-version.yaml",
            "template-id": "nginx-version",
            "template-path": "/home/yohan/nuclei-templates/http/technologies/nginx/nginx-version.yaml",
            "info": {
                "name": "Nginx version detect",
                "author": ["philippedelteil", "daffainfo"],
                "tags": ["tech", "nginx"],
                "description": "Some nginx servers have the version on the response header. Useful when you need to find specific CVEs on your targets.",
                "reference": None,
                "severity": "info",
                "metadata": {"max-request": 1},
            },
            "type": "http",
            "host": "https://yohangastoud.fr",
            "matched-at": "https://yohangastoud.fr",
            "extracted-results": ["nginx/1.18.0"],
            "request": "GET / HTTP/1.1\r\nHost: yohangastoud.fr\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0\r\nConnection: close\r\nAccept: */*\r\nAccept-Language: en\r\nX-From-Automation: Patrowl\r\nAccept-Encoding: gzip\r\n\r\n",
            "response": 'HTTP/1.1 200 OK\r\nConnection: close\r\nTransfer-Encoding: chunked\r\nContent-Type: text/html;charset=utf-8\r\nDate: Tue, 20 Feb 2024 15:25:09 GMT\r\nServer: nginx/1.18.0\r\nVary: Accept-Encoding\r\nX-Powered-By: Nuxt\r\n\r\n<!DOCTYPE html>\n<html >\n<head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Yohan Gastoud</title>\n<style>@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;1,400;1,600&display=swap");\n\n/*! tailwindcss v3.3.6 | MIT License | https://tailwindcss.com*/*,:after,:before{border:0 solid #e5e7eb;box-sizing:border-box}:after,:before{--tw-content:""}html{-webkit-text-size-adjust:100%;font-feature-settings:normal;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;font-variation-settings:normal;line-height:1.5;-moz-tab-size:4;-o-tab-size:4;tab-size:4}body{line-height:inherit;margin:0}hr{border-top-width:1px;color:inherit;height:0}abbr:where([title]){-webkit-text-decoration:underline dotted;text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,pre,samp{font-feature-settings:normal;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace;font-size:1em;font-variation-settings:normal}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}table{border-collapse:collapse;border-color:inherit;text-indent:0}button,input,optgroup,select,textarea{font-feature-settings:inherit;color:inherit;font-family:inherit;font-size:100%;font-variation-settings:inherit;font-weight:inherit;line-height:inherit;margin:0;padding:0}button,select{text-transform:none}[type=button],[type=reset],[type=submit],button{-webkit-appearance:button;background-color:transparent;background-image:none}:-moz-focusring{outline:auto}:-moz-ui-invalid{box-shadow:none}progress{vertical-align:baseline}::-webkit-inner-spin-button,::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}blockquote,dd,dl,figure,h1,h2,h3,h4,h5,h6,hr,p,pre{margin:0}fieldset{margin:0}fieldset,legend{padding:0}menu,ol,ul{list-style:none;margin:0;padding:0}dialog{padding:0}textarea{resize:vertical}input::-moz-placeholder,textarea::-moz-placeholder{color:#9ca3af;opacity:1}input::placeholder,textarea::placeholder{color:#9ca3af;opacity:1}[role=button],button{cursor:pointer}:disabled{cursor:default}audio,canvas,embed,iframe,img,object,svg,video{display:block;vertical-align:middle}img,video{height:auto;max-width:100%}[hidden]{display:none}*,:after,:before{--tw-border-spacing-x:0;--tw-border-spacing-y:0;--tw-translate-x:0;--tw-translate-y:0;--tw-rotate:0;--tw-skew-x:0;--tw-skew-y:0;--tw-scale-x:1;--tw-scale-y:1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness:proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width:0px;--tw-ring-offset-color:#fff;--tw-ring-color:rgba(59,130,246,.5);--tw-ring-offset-shadow:0 0 #0000;--tw-ring-shadow:0 0 #0000;--tw-shadow:0 0 #0000;--tw-shadow-colored:0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: }::backdrop{--tw-border-spacing-x:0;--tw-border-spacing-y:0;--tw-translate-x:0;--tw-translate-y:0;--tw-rotate:0;--tw-skew-x:0;--tw-skew-y:0;--tw-scale-x:1;--tw-scale-y:1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness:proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width:0px;--tw-ring-offset-color:#fff;--tw-ring-color:rgba(59,130,246,.5);--tw-ring-offset-shadow:0 0 #0000;--tw-ring-shadow:0 0 #0000;--tw-shadow:0 0 #0000;--tw-shadow-colored:0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: }.container{width:100%}@media (min-width:640px){.container{max-width:640px}}@media (min-width:768px){.container{max-width:768px}}@media (min-width:1024px){.container{max-width:1024px}}@media (min-width:1280px){.container{max-width:1280px}}@media (min-width:1536px){.container{max-width:1536px}}.mx-auto{margin-left:auto;margin-right:auto}.flex{display:flex}.h-full{height:100%}.h-screen{height:100vh}.flex-row{flex-direction:row}.items-center{align-items:center}.justify-center{justify-content:center}.bg-slate-950{--tw-bg-opacity:1;background-color:rgb(2 6 23/var(--tw-bg-opacity))}.pt-4{padding-top:1rem}.text-center{text-align:center}.align-middle{vertical-align:middle}.text-3xl{font-size:1.875rem;line-height:2.25rem}.font-bold{font-weight:700}.text-purple-100{--tw-text-opacity:1;color:rgb(243 232 255/var(--tw-text-opacity))}body,html,label{font-family:Roboto,sans-serif}</style>\n<link rel="modulepreload" as="script" crossorigin href="/_nuxt/entry.e10d8f5f.js">\n<link rel="modulepreload" as="script" crossorigin href="/_nuxt/index.0ce059e2.js">\n<link rel="prefetch" as="script" crossorigin href="/_nuxt/error-404.6ef145c5.js">\n<link rel="prefetch" as="script" crossorigin href="/_nuxt/vue.f36acd1f.e84496e4.js">\n<link rel="prefetch" as="script" crossorigin href="/_nuxt/error-500.b254c8f5.js">\n<script type="module" src="/_nuxt/entry.e10d8f5f.js" crossorigin></script>\n<script id="unhead:payload" type="application/json">{"title":"Yohan Gastoud"}</script></head>\n<body ><div id="__nuxt"><div class="bg-slate-950 h-screen"><div class="flex flex-row justify-center items-center align-middle h-full text-purple-100 container mx-auto pt-4"><h1 class="text-3xl text-center font-bold mx-auto">Hello</h1></div></div></div><script type="application/json" id="__NUXT_DATA__" data-ssr="true">[["Reactive",1],{"data":2,"state":3,"_errors":4,"serverRendered":5,"path":6},{},{},{},true,"/"]</script>\n<script>window.__NUXT__={};window.__NUXT__.config={public:{},app:{baseURL:"/",buildAssetsDir:"/_nuxt/",cdnURL:""}}</script></body>\n</html>',
            "ip": "54.36.189.124",
            "timestamp": "2024-02-20T16:25:09.816099373+01:00",
            "curl-command": "curl -X 'GET' -d '' -H 'Accept: */*' -H 'Accept-Language: en' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0' -H 'X-From-Automation: Patrowl' 'https://yohangastoud.fr'",
            "matcher-status": None,
            "matched-line": None,
        }


engine = Nuclei(Options)
