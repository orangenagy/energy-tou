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
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = ["read_csv", "parse_records", "write_json", "main"]

# globals
hourly_rates = {}
tariff_name = ""
standing_charge = ""

def parse_tariff(tariff_path: Path) -> Dict[str, Any]:
    """Parse tariff information from a JSON file."""
    import json
    tariff_path = Path(tariff_path)
    logger.debug("Reading tariff info from %s", tariff_path)
    with tariff_path.open(encoding="utf-8") as fh:
        tariff_info = json.load(fh)

    # print(tariff_info["standing_charge"])

    hourly_rates = {}

    for k, v in tariff_info["rates"].items():
        # print(f"Rate {k}: {v['rate_per_kwh']}p per kwh for time periods:")
        for time_period in v["time_periods"]:
            format = "%H:%M"
            time_from_str = time_period.split("-")[0].strip()
            time_to_str = time_period.split("-")[1].strip()

            time_from = datetime.strptime(time_from_str, format)
            time_to = datetime.strptime(time_to_str, format)

            if time_to < time_from:
                time_to += timedelta(days=1)

            time_difference = time_to - time_from

            # print(f"From {time_from.time()} to {time_to.time()} was {time_difference} hours at rate {v['rate_per_kwh']}p per kwh")
    
            current_time = time_from
            while current_time < time_to:
                hour = current_time.time().strftime('%H:%M')
                hourly_rates[hour] = v['rate_per_kwh']
                # print(f"Hour: {hour}")
                current_time += + timedelta(minutes=30)  # Increment by 30 minutes


    sorted_hours = sorted(hourly_rates.keys())
    for hour in sorted_hours:
        print(f"{hour}: {hourly_rates[hour]}p")


    tariff_name = tariff_info["tariff_name"]
    standing_charge = tariff_info["standing_charge"]

    # tariff_dict = {
    #     hourly_rates := hourly_rates,
    #     tariff_name := tariff_info["tariff_name"],
    #     standing_charge := tariff_info["standing_charge"]
    # }

    return tariff_info

def parse_energydata(path: Path) -> Dict[str, Any]:
    """Read a CSV file and return a list of row dictionaries."""
    path = Path(path)

    logger.debug("Reading CSV from %s", path)

    usage = {}
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        # print(f"this is it: {reader}")
        # for row in reader:
        #     print(f"row: {row}; date is {row['dateTime']}")
        # for row in reader:
        #     usage{row['dateTime']} := row['kWh']

        return [dict(row) for row in reader]

def calculate_usage(energy_data):
    for usage in energy_data:
        print(f"this is it {usage["kWh"]} for {usage["dateTime"]}")


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
        # print(tariff_info)

        energy_data = parse_energydata(args.energydata)
        # print(energy_data)

        usage = calculate_usage(energy_data)

        # price_estimates = compute_price_estimates(energy_data, tariff_info)
        # print(price_estimates)

        # logger.info("Finished parsing %s -> %s", args.energydata, args.output)
        return 0
    except Exception:
        logger.exception("Failed to parse data")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())