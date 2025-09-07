import time

from appium.webdriver.common.appiumby import AppiumBy

from report_client import set_test_info, get_report


def _scroll_and_tap_calendar(driver):
    candidates = ["Calendar", "Календарь"]
    for text in candidates:
        try:
            el = driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("{text}")'
            )
            el.click()
            return text
        except Exception:
            pass
    for text in candidates:
        try:
            driver.find_element(AppiumBy.ACCESSIBILITY_ID, text).click()
            return text
        except Exception:
            pass
    raise AssertionError("'Calendar/Календарь' is not found")


def test_open_calendar_from_pnv(driver):
    test_name = "PNV: open Calendar"
    set_test_info(test_name=test_name, test_status="STARTED")

    try:
        _scroll_and_tap_calendar(driver)
        time.sleep(1.0)
        set_test_info(test_name=test_name, test_status="PASSED")
    except Exception as e:
        set_test_info(test_name=test_name, test_status="FAILED")
        raise
    finally:
        try:
            rep = get_report()
            print("REPORT:", rep)
        except Exception as e:
            print("WARN: get_report failed:", e)
