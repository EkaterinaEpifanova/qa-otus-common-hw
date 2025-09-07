"""
Report from 'ps aux'.
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Process:
    user: str
    cpu: float
    mem: float
    command: str


def run_ps_aux() -> list[str]:
    """Execute 'ps aux'."""
    result = subprocess.run(
        ["ps", "aux"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().splitlines()


def parse_ps_aux(lines: list[str]) -> list[Process]:
    """Parse result 'ps aux'."""
    procs: list[Process] = []
    if not lines:
        return procs

    # Ignore the title
    for line in lines[1:]:
        # Expected params: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
        params = line.split(None, 10)
        if len(params) < 11:  # seems suspicious, should be 11 params
            continue
        user = params[0]
        try:
            cpu = float(params[2])
            mem = float(params[3])
        except ValueError:
            continue
        command = params[10]
        procs.append(Process(user=user, cpu=cpu, mem=mem, command=command))
    return procs


def build_report(procs: list[Process]) -> str:
    """Build the report."""
    total_processes = len(procs)
    users = sorted({p.user for p in procs})

    # Count processes by user and top mem and cpu
    user_counts: dict[str, int] = {}
    top_mem: tuple[float, str] = (0.0, "")
    top_cpu: tuple[float, str] = (0.0, "")
    for p in procs:
        user_counts[p.user] = user_counts.get(p.user, 0) + 1
        if p.mem > top_mem[0]:
            top_mem = (p.mem, p.command)
        if p.cpu > top_cpu[0]:
            top_cpu = (p.cpu, p.command)

    # Total
    total_cpu = sum(p.cpu for p in procs)
    total_mem = sum(p.mem for p in procs)

    # Sort users by process
    sorted_user_counts = sorted(user_counts.items(), key=lambda kv: (-kv[1], kv[0]))

    lines: list[str] = []
    lines.append("System Status Report:")
    users_str = ", ".join("'{}'".format(u) for u in users)
    lines.append(f"System users: {users_str}")
    lines.append(f"Processes running: {total_processes}\n")

    lines.append("User processes:")
    for user, count in sorted_user_counts:
        lines.append(f"{user}: {count}")
    lines.append("")

    lines.append(f"Total memory used: {total_mem:.1f}%")
    lines.append(f"Total CPU used: {total_cpu:.1f}%")

    return "\n".join(lines)


def save_report(report_text: str, directory: Path | None = None) -> Path:
    """Save report to txt file."""
    directory = directory or Path.cwd()
    filename = datetime.now().strftime("%d-%m-%Y-%H:%M-scan.txt")
    out_path = directory / filename
    out_path.write_text(report_text, encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collection of report ('ps aux')."
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Dir for report (current dir by default).",
    )
    args = parser.parse_args()

    lines = run_ps_aux()
    procs = parse_ps_aux(lines)
    report = build_report(procs)
    print(report)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = save_report(report, out_dir)
    print(f"\nSaved to file: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
