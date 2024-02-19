import validators
import subprocess

def is_url(url: str):
    return validators.url(url)

def is_ip(url: str):
    return validators.ipv4(url)

def is_domain(url: str):
    return validators.domain(url)

def execute_cmd(cmd: str):
    return subprocess.run(cmd.split(' '), stdout=subprocess.PIPE)