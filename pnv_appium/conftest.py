import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

# Auto-load .env from project root if present
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=False)


def _env(name: str, default=None):
    return os.getenv(name, default)


@pytest.fixture(scope="session")
def appium_server_url():
    return _env("APPIUM_SERVER_URL", "http://127.0.0.1:4723")


@pytest.fixture(scope="session")
def caps():
    device_name = _env("ANDROID_DEVICE_NAME", "emulator-5554")
    # By default expect apk near this project as 'pnv.apk'
    default_apk = os.path.abspath(os.path.join(os.path.dirname(__file__), "pnv.apk"))
    app_path = _env("APP_PATH", default_apk)

    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": device_name,
    }

    # If the apk exists, use it; otherwise rely on appPackage/appActivity from env
    if os.path.exists(app_path):
        caps["appium:app"] = app_path

    app_pkg = _env("APP_PACKAGE")
    app_act = _env("APP_ACTIVITY")

    if app_pkg:
        caps["appium:appPackage"] = app_pkg
    if app_act:
        caps["appium:appActivity"] = app_act

    return caps


@pytest.fixture()
def driver(appium_server_url, caps):
    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote(appium_server_url, options=options)
    yield driver
    driver.quit()
