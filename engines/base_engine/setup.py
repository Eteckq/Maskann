from setuptools import setup

setup(
    name="base_engine",
    version="0.1.1",
    description="Base engine",
    author="Yohan",
    license="BSD 2-clause",
    packages=["base_engine"],
    install_requires=[
        "fastapi",
        "fastapi-socketio"
        "pydantic",
        "validators",
        "uvicorn"
    ],
)
