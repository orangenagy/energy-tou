#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_data.py

Lightweight utilities to read, parse and write energy time-of-use (TOU) data.

Typical usage:
    python -m parse_data --input data.csv --output parsed.json

This file provides:
- read_csv(path) -> list[dict]
- parse_records(records) -> list[dict]
- write_json(records, path)
- CLI entrypoint main()
"""

import argparse
import csv
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = ["read_csv", "parse_records", "write_json", "main"]

def read_csv(path: Path) -> List[Dict[str, Any]]:
    """Read a CSV file and return a list of row dictionaries."""
    path = Path(path)
    logger.debug("Reading CSV from %s", path)
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        # print(f"this is it: {reader}")
        for row in reader:
            print(f"row: {row}; date is {row['dateTime']}")
        
        # return [dict(row) for row in reader]
        return "test"

def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse energy TOU CSV data")
    parser.add_argument("--input", "-i", required=True, type=Path, help="Input CSV file")
    parser.add_argument("--output", "-o", required=False, type=Path, help="Output JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        rows = read_csv(args.input)
        print(rows)
        # parsed = parse_records(rows)
        # write_json(parsed, args.output)
        logger.info("Finished parsing %s -> %s", args.input, args.output)
        return 0
    except Exception:
        logger.exception("Failed to parse data")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())