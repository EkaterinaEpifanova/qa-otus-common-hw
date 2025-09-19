import os
import pathlib
import sys

import pymysql
import pytest
from pymysql.cursors import DictCursor

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("mariadb")
    group.addoption("--db-host", default=os.getenv("DB_HOST", "127.0.0.1"))
    group.addoption("--db-port", type=int, default=int(os.getenv("DB_PORT", 3306)))
    group.addoption("--db-database", default=os.getenv("DB_NAME", "opencart"))
    group.addoption("--db-user", default=os.getenv("DB_USER", "root"))
    group.addoption("--db-password", default=os.getenv("DB_PASSWORD", ""))


@pytest.fixture(scope="session")
def connection(pytestconfig):
    host = pytestconfig.getoption("--db-host")
    port = pytestconfig.getoption("--db-port")
    db = pytestconfig.getoption("--db-database")
    user = pytestconfig.getoption("--db-user")
    password = pytestconfig.getoption("--db-password")
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db,
        cursorclass=DictCursor,
        autocommit=True,
        charset="utf8mb4",
    )
    try:
        yield conn
    finally:
        conn.close()
