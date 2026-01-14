from setuptools import setup, find_packages

setup(
    name="onebullex",
    version="1.0.0",
    description="A production-ready Python client for the OneBullEx Exchange API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Farhan Kardan",
    url="https://github.com/FarhanKardan/OneBullex_python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "websocket-client>=1.3.0",
        "protobuf>=3.19.0",
        "pydantic>=2.0.0",
        "grpcio-tools"
    ],
)
