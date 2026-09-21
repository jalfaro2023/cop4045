"""Run with: python -m unittest -v test_p5.py (from this directory)."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

# Locate the solution even after its student-name placeholders are replaced.
SOURCE = next(Path(__file__).parent.glob("p5_*.py"))
SPEC = importlib.util.spec_from_file_location("weather", SOURCE)
weather = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(weather)


class WeatherTests(unittest.TestCase):
    """Exercise input validation, calculations, output and error handling."""

    def setUp(self) -> None:
        """Create an isolated directory for each test."""
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.input = Path(self.folder.name) / "input.csv"
        self.output = Path(self.folder.name) / "output.csv"

    def read(self, content: str) -> tuple:
        """Write a fixture and return its parsed observations and errors."""
        self.input.write_text(content, encoding="utf-8")
        return weather.read_observations(str(self.input))

    def test_several_stations_and_negative_temperatures(self) -> None:
        """Keep valid observations for distinct stations, including negatives."""
        observations, errors = self.read(
            "North,09:00:00 AM 01/01/2026,-12.5\n"
            "South,09:00:00 AM 01/01/2026,20\n")
        self.assertEqual(errors, [])
        self.assertEqual(set(observations), {"North", "South"})
        self.assertEqual(observations["North"][0][1], -12.5)

    def test_chronological_sort(self) -> None:
        """Sort across years and noon by datetime rather than date text."""
        observations, _ = self.read(
            "A,01:00:00 PM 01/01/2026,3\n"
            "A,11:00:00 PM 12/31/2025,1\n"
            "A,09:00:00 AM 01/01/2026,2\n")
        self.assertEqual([value for _, value in observations["A"]], [1, 2, 3])

    def test_duplicate_observations(self) -> None:
        """Reject repeat station/date pairs and keep the first valid value."""
        observations, errors = self.read(
            "A,09:00:00 AM 01/01/2026,10\n"
            "A,09:00:00 AM 01/01/2026,30\n")
        self.assertEqual(len(observations["A"]), 1)
        self.assertEqual(observations["A"][0][1], 10)
        self.assertEqual(errors[0][0], 2)
        self.assertIn("Duplicate", errors[0][1])

    def test_invalid_ranges_and_nonfinite_values(self) -> None:
        """Accept both range endpoints; reject outside values, NaN and infinity."""
        observations, errors = self.read("".join(
            f"S{i},09:00:00 AM 01/01/2026,{value}\n"
            for i, value in enumerate([-100, 150, -100.1, 150.1, "nan", "inf"])))
        self.assertEqual(set(observations), {"S0", "S1"})
        self.assertEqual([line for line, _ in errors], [3, 4, 5, 6])

    def test_malformed_lines(self) -> None:
        """Report blank lines, wrong fields, invalid dates and bad numbers."""
        observations, errors = self.read(
            "\nA,date\n,09:00:00 AM 01/01/2026,2\n"
            "A,09:00:00 AM 02/30/2026,2\n"
            "A,09:00:00 AM 01/01/2026,hot\n"
            '"unterminated,date,3\n')
        self.assertEqual(observations, {})
        self.assertEqual([line for line, _ in errors], list(range(1, 7)))

    def test_statistics_and_outliers(self) -> None:
        """Check exact statistics and strict greater-than outlier comparison."""
        observations = {"A": [("earlier", -10), ("later", 20)],
                        "B": [("earlier", 20), ("later", 10)],
                        "C": [("only", 5)]}
        self.assertEqual(weather.station_statistics(observations),
                         {"A": (-10, 20, 5), "B": (10, 20, 15), "C": (5, 5, 5)})
        self.assertEqual(weather.station_outliers(observations),
                         {"A": ("later", 20, 5)})

    def test_sorted_output_and_one_decimal(self) -> None:
        """Write lexicographic station order and exactly one decimal digit."""
        weather.write_statistics(str(self.output),
                                 {"Zulu": (1, 2, 1.5), "Alpha": (-5, 0, -2.5)})
        self.assertEqual(self.output.read_text(encoding="utf-8"),
                         "station,min,max,mean\nAlpha,-5.0,0.0,-2.5\n"
                         "Zulu,1.0,2.0,1.5\n")

    def test_missing_files(self) -> None:
        """Propagate access errors from the reader and writer."""
        with self.assertRaises(FileNotFoundError):
            weather.read_observations(str(self.input))
        with self.assertRaises(FileNotFoundError):
            weather.write_statistics(str(self.input / "missing.csv"), {})

    def test_empty_input(self) -> None:
        """Empty input produces empty results without calculation errors."""
        self.assertEqual(self.read(""), ({}, []))
        self.assertEqual(weather.station_statistics({}), {})
        self.assertEqual(weather.station_outliers({}), {})

    def test_main_handles_file_errors_and_usage(self) -> None:
        """Return failure without a traceback for usage and access errors."""
        for arguments in [["weather.py"],
                          ["weather.py", str(self.input), str(self.output)]]:
            with patch.object(weather.sys, "argv", arguments):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(weather.main(), 1)

    def test_main_success(self) -> None:
        """Run the complete command-line workflow and verify its output."""
        self.read("A,09:00:00 AM 01/01/2026,12.5\n")
        with patch.object(weather.sys, "argv",
                          ["weather.py", str(self.input), str(self.output)]):
            with redirect_stdout(io.StringIO()) as terminal:
                self.assertEqual(weather.main(), 0)
        self.assertIn("A: 12.5, 12.5, 12.5", terminal.getvalue())
        self.assertTrue(self.output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
