# PNV → Open Calendar (Appium + Reporting)

Goal: In the pnv app, scroll the list to Calendar and open it, then log the test to the reporting service via:
- `GET /getReport`
- `DELETE /deleteReportData`
- `POST /setTestInfo`

The folder includes a minimal pytest pipeline and a report_client.py client to call the listed endpoints.

## 1) Requisites
- Appium 2.x
- uiautomator2 4.x
- appium-reporter-plugin 
- Appium server running with the reporter plugin
- Android device/emulator available
- Python 3.10+

## 2) Install dependencies
```bash
pip install -r requirements.txt
```

## 3) Environment setup
Copy `.env.example` в `.env`
- `APP_PATH=/absolute/path/to/pnv.apk`  
  or place `pnv.apk` next to the tests

Alternative: instead of the APK, set `APP_PACKAGE` and `APP_ACTIVITY`.

Specify the reporting service base URL:
- `REPORT_BASE_URL=http://127.0.0.1:4723`

## 4) Запуск теста
```bash
pytest -s -q
```
