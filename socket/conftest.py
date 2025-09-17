import os
import socket
import subprocess
import sys
import time

import pytest

HOST = "127.0.0.1"
PORT = 8080


@pytest.fixture(scope="session", autouse=True)
def _server():
    """Run server"""
    server_path = os.path.join(os.path.dirname(__file__), "echo_server.py")
    process = subprocess.Popen([sys.executable, server_path])

    # waiter
    for _ in range(50):
        try:
            with socket.create_connection((HOST, PORT), timeout=0.1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        process.terminate()
        raise RuntimeError(f"The server is not started {HOST}:{PORT}")

    yield

    process.terminate()


@pytest.fixture(scope="session")
def host():
    return HOST


@pytest.fixture(scope="session")
def port():
    return PORT
