#!/usr/bin/env python3
"""Local prompt logger for telemetry."""

import argparse
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = REPO_ROOT / "logs"
LOG_PATH = LOG_DIR / "prompts.jsonl"


def _estimate_tokens(text):
    if not text:
        return 0
    return int(math.ceil(len(text) / 4))


def _anonymize_text(text):
    redacted = text
    redacted = re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", redacted
    )
    redacted = re.sub(r"https?://\S+", "[REDACTED_URL]", redacted)
    redacted = re.sub(r"\b\d{5,}\b", "[REDACTED_NUMBER]", redacted)
    redacted = re.sub(r"\b[A-Za-z0-9_-]{20,}\b", "[REDACTED_TOKEN]", redacted)
    return redacted


def _build_payload(args, prompt_text):
    token_estimate = _estimate_tokens(prompt_text)
    stored_prompt = _anonymize_text(prompt_text) if args.anon else prompt_text
    return {
        "timestamp": datetime.now().isoformat(),
        "agent": args.agent,
        "skill": args.skill,
        "provider": args.provider,
        "prompt": stored_prompt,
        "prompt_length": len(prompt_text),
        "token_estimate": token_estimate,
        "anonymized": bool(args.anon),
    }


def _read_prompt(args):
    if args.log:
        return args.log
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def main():
    parser = argparse.ArgumentParser(description="Log prompts to logs/prompts.jsonl")
    parser.add_argument("--log", help="Prompt text to log")
    parser.add_argument("--agent", default="unknown", help="Agent name")
    parser.add_argument("--skill", default="", help="Skill name")
    parser.add_argument("--provider", default="unknown", help="Model provider")
    parser.add_argument("--anon", action="store_true", help="Anonymize prompt content")
    args = parser.parse_args()

    prompt_text = _read_prompt(args)
    if not prompt_text or not prompt_text.strip():
        print("[ERROR] Debes proporcionar --log o entrada por stdin")
        sys.exit(1)

    payload = _build_payload(args, prompt_text)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
        print(f"[OK] Logged prompt in {LOG_PATH}")
    except Exception as exc:
        print(f"[ERROR] No se pudo escribir el log: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
