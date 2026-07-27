from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from sanyan_protocol.audit import InvalidRecord, audit_record, load_record


REPOSITORY = Path(__file__).resolve().parents[1]


class AuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = load_record(REPOSITORY / "examples" / "audit_record.json")
        self.root = REPOSITORY / "examples" / "workspace"

    def test_shipped_synthetic_record_passes(self):
        report = audit_record(self.record, self.root)
        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual((report["passed"], report["failed"]), (5, 0))
        self.assertIn("role_identifiers_differ", {item["id"] for item in report["checks"]})

    def test_missing_or_reordered_stage_fails(self):
        for stages in (
            self.record["stages"][:-1],
            list(reversed(self.record["stages"])),
        ):
            with self.subTest(stages=stages):
                record = deepcopy(self.record)
                record["stages"] = stages
                report = audit_record(record, self.root)
                self.assertEqual(report["verdict"], "FAIL")

    def test_executor_cannot_review_itself(self):
        for reviewer in (
            self.record["executor"].upper(),
            f"  {self.record['executor']}  ",
            "ｅｘｅｃｕｔｏｒ－ｄｅｍｏ",
        ):
            with self.subTest(reviewer=reviewer):
                record = deepcopy(self.record)
                record["reviewer"] = reviewer
                report = audit_record(record, self.root)
                self.assertEqual(report["verdict"], "FAIL")

    def test_high_risk_requires_human_approval(self):
        record = deepcopy(self.record)
        record["risk"] = "high"
        report = audit_record(record, self.root)
        self.assertEqual(report["verdict"], "FAIL")
        record["human_approved"] = True
        self.assertEqual(audit_record(record, self.root)["verdict"], "PASS")

    def test_one_invalid_citation_fails_the_whole_gate(self):
        invalid = (
            "source.md:0",
            "source.md:-1",
            "source.md:999",
            "missing.md:1",
            "../audit_record.json:1",
            f"{(self.root / 'source.md').resolve()}:1",
            "source.md:2",
            "source.md:1000001",
            f"source.md:{'1' * 5001}",
            "bad\x00name.md:1",
        )
        for citation in invalid:
            with self.subTest(citation=citation):
                record = deepcopy(self.record)
                record["claims"].append({"text": "Another claim", "citation": citation})
                report = audit_record(record, self.root)
                self.assertEqual(report["verdict"], "FAIL")

    def test_non_utf8_citation_target_fails_without_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "binary.bin").write_bytes(b"\xff\xfe\x00")
            record = deepcopy(self.record)
            record["claims"][0]["citation"] = "binary.bin:1"
            report = audit_record(record, root)
            self.assertEqual(report["verdict"], "FAIL")
            citation_check = next(item for item in report["checks"] if item["id"] == "citations_exist")
            self.assertIn("UTF-8", citation_check["evidence"])

    def test_empty_closeout_is_a_failed_gate_not_a_schema_crash(self):
        record = deepcopy(self.record)
        record["outcome"] = ""
        record["stop_condition"] = ""
        report = audit_record(record, self.root)
        self.assertEqual(report["verdict"], "FAIL")
        closeout = next(item for item in report["checks"] if item["id"] == "closeout_recorded")
        self.assertFalse(closeout["passed"])

    def test_unknown_fields_and_non_string_citation_are_rejected(self):
        record = deepcopy(self.record)
        record["extra"] = True
        with self.assertRaises(InvalidRecord):
            audit_record(record, self.root)
        record = deepcopy(self.record)
        record["claims"][0]["citation"] = 3
        with self.assertRaises(InvalidRecord):
            audit_record(record, self.root)

    def test_invalid_json_is_not_a_record(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text("not-json", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                load_record(path)

    def test_duplicate_json_keys_are_rejected_at_every_object_level(self):
        duplicate_documents = (
            '{"reviewer":"executor-demo","reviewer":"reviewer-demo"}',
            '{"claims":[{"text":"first","text":"second","citation":"source.md:3"}]}',
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            for document in duplicate_documents:
                with self.subTest(document=document):
                    path.write_text(document, encoding="utf-8")
                    with self.assertRaisesRegex(InvalidRecord, "duplicate JSON key"):
                        load_record(path)

    def test_deeply_nested_and_oversized_records_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text("[" * 10_000 + "]" * 10_000, encoding="utf-8")
            with self.assertRaisesRegex(InvalidRecord, "nesting"):
                load_record(path)
            path.write_bytes(b" " * 1_000_001)
            with self.assertRaisesRegex(InvalidRecord, "byte limit"):
                load_record(path)


if __name__ == "__main__":
    unittest.main()
