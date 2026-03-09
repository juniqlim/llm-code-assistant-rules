import json
import sys
import tempfile
import unittest
from pathlib import Path
import importlib.util

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "recap.py"
spec = importlib.util.spec_from_file_location("recap", SCRIPT_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class RecapUnitTest(unittest.TestCase):
    def write_session(self, records):
        tmp = tempfile.NamedTemporaryFile("w", delete=False)
        with tmp:
            for record in records:
                tmp.write(json.dumps(record) + "\n")
        return Path(tmp.name)

    def test_session_cwd_uses_session_meta(self):
        session = self.write_session(
            [
                {
                    "type": "session_meta",
                    "payload": {"cwd": "/tmp/project"},
                }
            ]
        )

        self.assertEqual(mod.get_session_cwd(session), "/tmp/project")

    def test_collect_user_messages_reads_response_items_and_compacted_history(self):
        session = self.write_session(
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "first request"},
                        ],
                    },
                },
                {
                    "type": "compacted",
                    "payload": {
                        "replacement_history": [
                            {
                                "type": "message",
                                "role": "user",
                                "content": [
                                    {
                                        "type": "input_text",
                                        "text": "older compacted request",
                                    }
                                ],
                            },
                            {
                                "type": "message",
                                "role": "assistant",
                                "content": [
                                    {"type": "output_text", "text": "ignored"}
                                ],
                            },
                        ]
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "latest request"},
                        ],
                    },
                },
            ]
        )

        self.assertEqual(
            mod.collect_user_messages(session),
            [
                "first request",
                "older compacted request",
                "latest request",
            ],
        )

    def test_collect_user_messages_filters_noise(self):
        session = self.write_session(
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "[Request interrupted"},
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "<environment_context>"},
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "# AGENTS.md instructions for /tmp/project",
                            },
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "keep me"},
                        ],
                    },
                },
            ]
        )

        self.assertEqual(mod.collect_user_messages(session), ["keep me"])

    def test_find_candidate_sessions_matches_project_and_excludes_latest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            first = root / "first.jsonl"
            second = root / "second.jsonl"
            other = root / "other.jsonl"
            first.write_text(
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {"cwd": "/tmp/project"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            second.write_text(
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {"cwd": "/tmp/project"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            other.write_text(
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {"cwd": "/tmp/other"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            first.touch()
            second.touch()
            other.touch()

            sessions = mod.find_candidate_sessions(root, "/tmp/project")

            self.assertEqual([item.path for item in sessions], [first])

    def test_summarize_session_uses_first_and_last_user_messages(self):
        session = mod.SessionInfo(
            path=Path("/tmp/session.jsonl"),
            session_id="session-id",
            mtime=0.0,
            cwd="/tmp/project",
            first_user_message="첫 요청은 리드미 확인",
            user_messages=[
                "첫 요청은 리드미 확인",
                "복합 쿠폰 정책 테스트 보강",
                "그래 넣자",
            ],
        )

        self.assertEqual(
            mod.summarize_session(session),
            "첫 요청은 리드미 확인 / 마지막: 그래 넣자",
        )


if __name__ == "__main__":
    unittest.main()
