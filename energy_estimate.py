#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_data.py

Lightweight utilities to read, parse and write energy time-of-use (TOU) data.

Typical usage:
    python -m parse_data --energydata data.csv --output parsed.json

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

def parse_tariff(tariff_path: Path) -> Dict[str, Any]:
    """Parse tariff information from a JSON file."""
    import json
    tariff_path = Path(tariff_path)
    logger.debug("Reading tariff info from %s", tariff_path)
    with tariff_path.open(encoding="utf-8") as fh:
        tariff_info = json.load(fh)
    return tariff_info

def parse_energydata(path: Path) -> List[Dict[str, Any]]:
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
    parser.add_argument("--energydata", "-e", required=True, type=Path, help="Energy Data CSV file")
    parser.add_argument("--tariff", "-t", required=True, type=Path, help="Tariff Info JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        tariff_info = parse_tariff(args.tariff)
        energy_data = parse_energydata(args.energydata)
        print(energy_data)

        price_estimates = compute_price_estimates(energy_data, tariff_info)
        print(price_estimates)
        # parsed = parse_records(rows)
        # write_json(parsed, args.output)
        # logger.info("Finished parsing %s -> %s", args.energydata, args.output)
        return 0
    except Exception:
        logger.exception("Failed to parse data")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())