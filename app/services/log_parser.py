from datetime import datetime

from app.models.incident import LogEntry


def parse_log_line(line: str) -> LogEntry:
    parts = line.strip().split(" | ")

    if len(parts) != 4:
        raise ValueError(f"Invalid log format: {line}")

    timestamp, level, service, message = parts

    return LogEntry(
        timestamp=datetime.strptime(
            timestamp,
            "%Y-%m-%d %H:%M:%S"
        ),
        level=level,
        service=service,
        message=message,
    )


def parse_log_file(file_path: str) -> list[LogEntry]:
    logs = []

    with open(file_path, "r") as file:
        for line in file:
            if line.strip():
                logs.append(parse_log_line(line))

    return logs
