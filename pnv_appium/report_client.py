import os

import requests

BASE = os.getenv("REPORT_BASE_URL", "http://127.0.0.1:4723")


def set_test_info(test_name: str, test_status: str, error: str = "error"):
    """POST /setTestInfo"""
    url = f"{BASE}/setTestInfo"
    payload = {"testName": test_name, "testStatus": test_status, "error": error}
    r = requests.post(url, json=payload, timeout=15)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return r.text


def get_report():
    """GET /getReport"""
    url = f"{BASE}/getReport"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return r.text


def delete_report_data():
    """DELETE /deleteReportData"""
    url = f"{BASE}/deleteReportData"
    r = requests.delete(url, timeout=15)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return r.text
