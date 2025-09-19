import pathlib
import random
import string
import sys
import time

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from opencart_db import db


def _rand_str(n=6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


def _new_customer_payload():
    ts = int(time.time())
    return {
        "firstname": f"John{_rand_str(3)}",
        "lastname": f"Doe{_rand_str(3)}",
        "email": f"john{ts}{_rand_str(3)}@example.test",
        "telephone": f"+1{random.randint(100000000, 999999999)}",
        "password": "test_password",
        "status": 1,
        "customer_group_id": 1,
        "store_id": 0,
        "language_id": 1,
    }


@pytest.fixture()
def created_customer_id(connection):
    cust_id = db.create_customer(connection, _new_customer_payload())
    yield cust_id
    try:
        db.delete_customer_by_id(connection, cust_id)
    except Exception:
        pass


def test_create_customer_and_select_by_id(connection):
    cust_id = db.create_customer(connection, _new_customer_payload())
    row = db.get_customer_by_id(connection, cust_id)
    assert row is not None
    assert row["customer_id"] == cust_id
    # cleanup
    assert db.delete_customer_by_id(connection, cust_id) == 1
    assert db.get_customer_by_id(connection, cust_id) is None


def test_update_existing_customer_basic_fields(connection, created_customer_id):
    cust_id = created_customer_id
    new_firstname = "Test"
    new_lastname = "Kate"
    new_email = f"kate{_rand_str(4)}@example.test"
    new_phone = "+123123123"

    affected = db.update_customer_basic_fields(
        connection,
        cust_id,
        firstname=new_firstname,
        lastname=new_lastname,
        email=new_email,
        telephone=new_phone,
    )
    assert affected == 1

    row = db.get_customer_by_id(connection, cust_id)
    assert row["firstname"] == new_firstname
    assert row["lastname"] == new_lastname
    assert row["email"] == new_email
    assert row["telephone"] == new_phone


def test_update_nonexistent_customer(connection):
    affected = db.update_customer_basic_fields(
        connection,
        999_999_999,
        firstname="No",
        lastname="Kate",
        email="nokate@here.test",
        telephone="+321321321",
    )
    assert affected == 0


def test_delete_existing_customer(connection):
    cust_id = db.create_customer(connection, _new_customer_payload())
    assert db.get_customer_by_id(connection, cust_id) is not None
    affected = db.delete_customer_by_id(connection, cust_id)
    assert affected == 1
    assert db.get_customer_by_id(connection, cust_id) is None


def test_delete_nonexistent_customer(connection):
    affected = db.delete_customer_by_id(connection, 999_999_998)
    assert affected == 0
