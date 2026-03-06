from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
import unicodedata


def parse_csv_items(raw: str | None) -> list[str]:
    if not raw:
        return []
    items = [item.strip() for item in raw.split(",")]
    return [item for item in items if item]


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", text))


def slugify_title(title: str, enable_slugify: bool = True) -> str:
    cleaned = title.strip()
    if not cleaned:
        return "untitled"

    # Replace unsupported path chars early.
    cleaned = re.sub(r"[\\/:*?\"<>|]", "-", cleaned)

    if not enable_slugify:
        return re.sub(r"\s+", "-", cleaned)

    if contains_cjk(cleaned):
        # Keep CJK readable and only normalize whitespace/hyphen usage.
        return re.sub(r"-+", "-", re.sub(r"\s+", "-", cleaned)).strip("-") or "untitled"

    normalized = unicodedata.normalize("NFKD", cleaned)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    ascii_text = re.sub(r"-+", "-", ascii_text).strip("-")
    return ascii_text or "untitled"


def parse_timezone_offset(offset: str) -> timezone:
    match = re.fullmatch(r"([+-])(\d{2}):(\d{2})", offset)
    if not match:
        raise ValueError("timezone must look like +08:00 or -05:00")

    sign, hours_str, minutes_str = match.groups()
    hours = int(hours_str)
    minutes = int(minutes_str)

    delta = timedelta(hours=hours, minutes=minutes)
    if sign == "-":
        delta = -delta
    return timezone(delta)


def iso_now(offset: str) -> str:
    tz = parse_timezone_offset(offset)
    return datetime.now(tz=tz).replace(microsecond=0).isoformat()


def quote_yaml_str(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def format_yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    quoted = ", ".join(quote_yaml_str(item) for item in items)
    return f"[{quoted}]"
