"""HW3 · walks.py: read the step counter's CSV file and keep only the good rows. Practises
Session 7 (reading a CSV file, cleaning data) and Session 9 (a generator and a decorator)."""

import csv
import re
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from functools import wraps
from pathlib import Path


@dataclass
class Walk:
    """Provided: one walk from the log, cleaned. `steps` is a whole number, 0 or more."""

    date: str
    steps: int
    place: str


def parse_walk(row: dict[str, str]) -> Walk:
    """Turn one row of the CSV file into a Walk, or raise ValueError if the row is bad."""
    date_value = row.get("date")
    date = date_value.strip() if isinstance(date_value, str) else ""
    if not date:
        raise ValueError("date is empty")

    steps_text = row.get("steps")
    if not isinstance(steps_text, str) or re.fullmatch(r"[+-]?[0-9]+", steps_text.strip()) is None:
        raise ValueError(f"steps is not a whole number: {steps_text}") from None
    steps = int(steps_text)
    if steps < 0:
        raise ValueError(f"steps is below 0: {steps_text}")

    place_value = row.get("place")
    place = place_value.strip() if isinstance(place_value, str) else ""
    return Walk(date, steps, place)


def none_on_error(func: Callable) -> Callable:
    """A decorator: the wrapped function returns None instead of raising ValueError."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return None
    return wrapper


def read_rows(path: Path) -> Iterator[dict[str, str]]:
    """Yield the rows of a CSV file one at a time, each as a dict of text."""
    with path.open("r", encoding="utf-8", newline="") as file:
        yield from csv.DictReader(file)


def good_walks(rows: Iterable[dict[str, str]]) -> Iterator[Walk]:
    """Yield a Walk for every good row, one at a time, and skip the bad rows."""
    safe_parse = none_on_error(parse_walk)
    for row in rows:
        walk = safe_parse(row)
        if walk is not None:
            yield walk
