import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "recap.py"


class RecapCliIntegrationTest(unittest.TestCase):
    def write_session(self, path, cwd, messages):
        records = [
            {"type": "session_meta", "payload": {"cwd": cwd}},
        ]
        for message in messages:
            records.append(
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": message}],
                    },
                }
            )
        path.write_text(
            "".join(json.dumps(record) + "\n" for record in records),
            encoding="utf-8",
        )

    def test_list_shows_recent_sessions_for_same_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            older = root / "older.jsonl"
            current = root / "current.jsonl"
            self.write_session(
                older,
                "/tmp/project",
                ["older first request", "follow-up details", "final ask"],
            )
            self.write_session(current, "/tmp/project", ["current request"])
            older.touch()
            current.touch()

            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--sessions-root",
                    str(root),
                    "--cwd",
                    "/tmp/project",
                    "list",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("1. [", result.stdout)
            self.assertIn("older first request / 마지막: final ask", result.stdout)
            self.assertNotIn("current request", result.stdout)

    def test_show_by_index_prints_last_three_messages(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            older = root / "older.jsonl"
            current = root / "current.jsonl"
            self.write_session(
                older,
                "/tmp/project",
                ["first", "second", "third", "fourth"],
            )
            self.write_session(current, "/tmp/project", ["current request"])
            older.touch()
            current.touch()

            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    "--sessions-root",
                    str(root),
                    "--cwd",
                    "/tmp/project",
                    "show",
                    "1",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("SESSION:", result.stdout)
            self.assertIn("USER: second", result.stdout)
            self.assertIn("USER: third", result.stdout)
            self.assertIn("USER: fourth", result.stdout)
            self.assertNotIn("USER: first", result.stdout)


if __name__ == "__main__":
    unittest.main()
