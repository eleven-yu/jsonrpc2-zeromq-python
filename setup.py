# Part of the jsonrpc2-zeromq-python project.
# (c) 2012 Wireless Innovation Ltd, All Rights Reserved.
# Please see the LICENSE file in the root of this project for license
# information.

from setuptools import setup

description = "Library for JSON-RPC 2.0 over ZeroMQ"

try:
    long_description = open(os.path.join(os.path.dirname(__file__),
                                         'README.rst')).read()
except Exception:
    long_description = description

setup(
    name = "jsonrpc2-zeromq",
    version = "1.0.0",
    description = description,
    long_description = long_description,
    url = "https://github.com/wiltd/python-jsonrpc2-zeromq",
    classifiers = [
        "Programming Language :: Python :: 2.7",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        ],
    author = "Dan Brown",
    author_email = "dan@danwb.net",
    packages = ["jsonrpc2_zeromq"],
    install_requires=[
        "distribute",
        "pyzmq<2.2",
        ],
    )

