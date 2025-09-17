# Python Learning Project

This repository contains a collection of simple Python scripts created as part of a learning journey in Python programming.

## 📚 Contents

- The script `ps_report.py` runs ps aux, parses the output with Python's standard library, 
prints a system usage report (users, process counts, total CPU/memory, top consumers), 
and saves it to a timestamped TXT file.

- The script `log_analyzer.py` analyzes logs of the format
`%h - - %t "%r" %s %b "%{Referer}" "%{User-Agent}" %d`
For **each input file** the following is generated:
- total number of requests;
- number of requests by methods: GET, POST, PUT, DELETE, OPTIONS, HEAD;
- top 3 IP by number of requests;
- top 3 longest requests (method, URL, IP, duration in ms, date/time);
- separate JSON report.

- The dir `pnv_appium` contains test for pnv.apk
- More scripts coming soon as learning progresses...

## ✅ Requirements
- Python 3.10 or higher
- WSL or any Unix-based system

To run `ps_report.py` script on WSL or any Unix-based system:
```bash
python3 ps_report.py
```

To run `log_analyzer.py` script :
```bash
python log_analyzer.py access.log
```