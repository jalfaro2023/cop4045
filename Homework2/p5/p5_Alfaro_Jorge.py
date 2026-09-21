"""Problem 5: weather observations, statistics and outliers.

Input is headerless CSV: station,date,temperature. Dates use
%I:%M:%S %p %m/%d/%Y. Output CSV contains station,min,max,mean.
Run: python p5_Alfaro_Jorge.py observations.csv statistics.csv
"""

import csv
from datetime import datetime
import sys

DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
Observations = dict[str, list[tuple[str, float]]]
Statistics = dict[str, tuple[float, float, float]]


def read_observations(filename: str) -> tuple[Observations, list[tuple[int, str]]]:
    """Read valid observations in chronological order and report bad lines.

    The first valid observation for a station and parsed date wins.
    File-access errors propagate to the caller.
    """
    observations, errors, seen = {}, [], set()
    with open(filename, encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            try:
                row = next(csv.reader([line], strict=True))
                if len(row) != 3:
                    raise ValueError("Expected station,date,temperature.")
                station, date, text = (field.strip() for field in row)
                if not station:
                    raise ValueError("Station cannot be empty.")
                timestamp = datetime.strptime(date, DATE_FORMAT)
                temperature = float(text)
                if not -100.0 <= temperature <= 150.0:
                    raise ValueError("Temperature must be between -100 and 150.")
                key = (station, timestamp)
                if key in seen:
                    raise ValueError("Duplicate station/date observation.")
                seen.add(key)
                observations.setdefault(station, []).append((date, temperature))
            except (ValueError, csv.Error) as error:
                errors.append((line_number, str(error)))
    for records in observations.values():
        records.sort(key=lambda item: datetime.strptime(item[0], DATE_FORMAT))
    return observations, errors


def station_statistics(observations: Observations) -> Statistics:
    """Map each nonempty station to its minimum, maximum and mean."""
    statistics = {}
    for station, records in observations.items():
        if records:
            temperatures = [temperature for _, temperature in records]
            statistics[station] = (min(temperatures), max(temperatures),
                                   sum(temperatures) / len(temperatures))
    return statistics


def station_outliers(observations: Observations) -> dict[str, tuple[str, float, float]]:
    """Map stations whose latest value exceeds their mean to (date, value, mean).

    Observations must be chronologically sorted, as read_observations returns.
    """
    statistics = station_statistics(observations)
    return {station: (*records[-1], statistics[station][2])
            for station, records in observations.items()
            if records and records[-1][1] > statistics[station][2]}


def write_statistics(filename: str, statistics: Statistics) -> None:
    """Write stations alphabetically, with all numbers to one decimal place."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["station", "min", "max", "mean"])
        for station in sorted(statistics):
            writer.writerow([station, *(f"{value:.1f}"
                                        for value in statistics[station])])


def main() -> int:
    """Read command-line paths, report results and handle file-access errors."""
    print("Student: Jorge Alfaro | FAU ID: Z23697022 | Problem 5")
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 1
    try:
        observations, errors = read_observations(sys.argv[1])
        statistics = station_statistics(observations)
        print("Statistics (minimum, maximum, mean)")
        for station in sorted(statistics):
            values = ", ".join(f"{value:.1f}" for value in statistics[station])
            print(f"{station}: {values}")
        print("Outliers (date, temperature, mean)")
        outliers = station_outliers(observations)
        for station, (date, value, mean) in sorted(outliers.items()):
            print(f"{station}: {date}, {value:.1f}, {mean:.1f}")
        for line, message in errors:
            print(f"Rejected line {line}: {message}")
        write_statistics(sys.argv[2], statistics)
        return 0
    except (OSError, UnicodeError) as error:
        print(f"Could not access the weather data: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
