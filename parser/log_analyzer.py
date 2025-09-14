import argparse
import json
import re
from collections import Counter, OrderedDict
from datetime import datetime
from pathlib import Path

METHODS = ("GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD")

# Log example:
# 109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "UA" 7269
REGEX = re.compile(
    r'^(?P<ip>\S+)\s+-\s+-\s+\[(?P<ts>[^\]]+)\]\s+'
    r'"(?P<request>[^"]+)"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\S+)\s+'
    r'"(?P<referer>[^"]*)"\s+"(?P<ua>[^"]*)"\s+'
    r'(?P<duration_ms>\d+)\s*$'
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analys access.log: methods, IP and TOP-3 long requests (ms)."
    )
    parser.add_argument("path", help="Path to access.log file or dir with file")
    parser.add_argument(
        "--pattern", default="*.log",
        help="Pattern for getting file from dir"
    )
    parser.add_argument(
        "--out", default="out",
        help="Path to dir with JSON reports"
    )
    parser.add_argument(
        "--recursive", action="store_true",
        help="Get file from dir recursive."
    )
    return parser.parse_args()


def iter_log_files(path: Path, pattern: str, recursive: bool):
    if path.is_file():
        yield path
        return
    if path.is_dir():
        it = path.rglob(pattern) if recursive else path.glob(pattern)
        for p in it:
            if p.is_file():
                yield p
        return
    raise FileNotFoundError(f"File not found: {path}")


def parse_line(line: str):
    m = REGEX.match(line)
    if not m:
        return None
    request = m.group("request").split()
    method = request[0] if len(request) > 0 else "-"
    url = request[1] if len(request) > 1 else "-"
    return {
        "ip": m.group("ip"),
        "date_brackets": f"[{m.group('ts')}]",
        "method": method,
        "url": url,
        "duration_ms": int(m.group("duration_ms")),
    }


def analyze_file(path: Path):
    """Method counts requests by HTTP methods,
    chooses top 3 IP addresses
    and defines top 3 longest requests"""
    total_requests = 0
    method_counts = {m: 0 for m in METHODS}
    ip_counter = Counter()
    slow = []

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            record = parse_line(line)
            if not record:
                continue
            total_requests += 1
            if record["method"] in method_counts:
                method_counts[record["method"]] += 1
            ip_counter.update([record["ip"]])
            slow.append((record["duration_ms"], record))

    # top_ips by DESC
    top_ips = OrderedDict()
    for ip, count in ip_counter.most_common(3):
        top_ips[ip] = count

    # top_longest
    slow.sort(key=lambda x: x[0], reverse=True)
    top_longest = [
        {
            "ip": request["ip"],
            "date": request["date_brackets"],
            "method": request["method"],
            "url": request["url"],
            "duration": duration,  # миллисекунды
        }
        for duration, request in slow[:3]
    ]

    total_stat = {m: method_counts[m] for m in METHODS}

    result_json = {
        "top_ips": top_ips,
        "top_longest": top_longest,
        "total_stat": total_stat,
        "total_requests": total_requests,
    }
    return result_json


def save_report(obj, out_dir: Path) -> Path:
    """Save report to json file."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = out_dir / f"{ts}-scan.json"

    with out_path.open("w", encoding="utf-8") as w:
        json.dump(obj, w, ensure_ascii=False, indent=2)
    return out_path


def main():
    args = parse_args()
    base = Path(args.path)
    files = list(iter_log_files(base, args.pattern, args.recursive))
    if not files:
        print("There is no .log file")
        return

    out_dir = Path(args.out)
    for f in files:
        stats = analyze_file(f)
        saved_report = save_report(stats, out_dir)
        print(f"Report was created: {saved_report}")


if __name__ == "__main__":
    main()
