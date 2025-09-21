import pathlib
import random
import string
import sys
import time

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))


def _rand_str(n=6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


@pytest.fixture(name="customer_payload")
def _customer_payload():
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


@pytest.fixture(name="created_customer_id")
def _created_customer_id(db_client, customer_payload):
    cust_id = db_client.create_customer(customer_payload)
    yield cust_id
    try:
        db_client.delete_customer_by_id(cust_id)
    except Exception:
        pass


@pytest.fixture(name="update_payload")
def _update_payload():
    return {
        "firstname": "Test",
        "lastname": "Kate",
        "email": f"kate{_rand_str(4)}@example.test",
        "telephone": "+123123132",
    }


def test_create_customer_and_select_by_id(db_client, customer_payload):
    cust_id = db_client.create_customer(customer_payload)
    row = db_client.get_customer_by_id(cust_id)
    assert row is not None
    assert row["customer_id"] == cust_id
    # cleanup
    assert db_client.delete_customer_by_id(cust_id) == 1
    assert db_client.get_customer_by_id(cust_id) is None


def test_update_existing_customer_basic_fields(db_client, created_customer_id, update_payload):
    cust_id = created_customer_id

    affected = db_client.update_customer_basic_fields(
        cust_id,
        firstname=update_payload["firstname"],
        lastname=update_payload["lastname"],
        email=update_payload["email"],
        telephone=update_payload["telephone"],
    )
    assert affected == 1

    row = db_client.get_customer_by_id(cust_id)
    assert row is not None
    assert row["firstname"] == update_payload["firstname"]
    assert row["lastname"] == update_payload["lastname"]
    assert row["email"] == update_payload["email"]
    assert row["telephone"] == update_payload["telephone"]


def test_update_nonexistent_customer(db_client, update_payload):
    affected = db_client.update_customer_basic_fields(
        999_999_999,
        firstname=update_payload["firstname"],
        lastname=update_payload["lastname"],
        email=update_payload["email"],
        telephone=update_payload["telephone"],
    )
    assert affected == 0


def test_delete_existing_customer(db_client, customer_id):
    assert db_client.get_customer_by_id(customer_id) is not None
    affected = db_client.delete_customer_by_id(customer_id)
    assert affected == 1
    assert db_client.get_customer_by_id(customer_id) is None


def test_delete_nonexistent_customer(db_client):
    affected = db_client.delete_customer_by_id(999_999_998)
    assert affected == 0
