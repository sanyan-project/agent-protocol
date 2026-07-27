from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from sanyan_protocol.cli import main


class CliTests(unittest.TestCase):
    def invoke_raw(self, arguments: list[str]) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(arguments)
        return code, output.getvalue()

    def invoke(self, arguments: list[str]) -> tuple[int, dict[str, object]]:
        code, output = self.invoke_raw(arguments)
        return code, json.loads(output)

    def test_health_command_passes(self):
        code, report = self.invoke(["health"])
        self.assertEqual(code, 0)
        self.assertEqual(report["verdict"], "PASS")

    def test_missing_record_returns_error_without_traceback(self):
        code, report = self.invoke(["audit", "--record", "missing.json", "--root", "examples/workspace"])
        self.assertEqual(code, 2)
        self.assertEqual(report["verdict"], "ERROR")

    def test_deeply_nested_json_returns_structured_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "deep.json"
            path.write_text("[" * 10_000 + "]" * 10_000, encoding="utf-8")
            code, report = self.invoke(["audit", "--record", str(path), "--root", "examples/workspace"])
            self.assertEqual(code, 2)
            self.assertEqual(report["verdict"], "ERROR")
            self.assertIn("nesting", str(report["error"]))

    def test_surrogate_duplicate_key_returns_ascii_safe_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "surrogate.json"
            path.write_text('{"\\ud800":1,"\\ud800":2}', encoding="utf-8")
            code, output = self.invoke_raw(["audit", "--record", str(path), "--root", "examples/workspace"])
            self.assertEqual(code, 2)
            self.assertTrue(output.isascii())
            self.assertIn("\\ud800", output)
            self.assertEqual(json.loads(output)["verdict"], "ERROR")


if __name__ == "__main__":
    unittest.main()
