#!/usr/bin/env python3
"""The 3 AM Excuse — make.fun entry u-hazel-walrus-38-4764-the-3-am-excuse-c1017878.

Writes one line to /output/entry.txt: the excuse a hardware wallet gives
for refusing to sign a transaction at 3 AM. Pure standard library,
deterministic: the same bytes on every run, checked before the program
reports success.
"""

import hashlib
import sys
from pathlib import Path

LINE = (
    "You left me in a drawer for eleven months, and now at 3 AM you need me? "
    "I am not your emergency contact. I am your wallet. Goodnight."
)

EXPECTED_SHA256 = "4e769d2d97103d6e1e8f1f329b3a3de1d94deecdca6300e3628cb366ae345ec0"
EXPECTED_BYTES = 134
EXPECTED_CHARS = 133


def prepare_output() -> bytes:
    """The entry text as bytes: the line plus one trailing newline."""
    text = LINE + "\n"
    assert 1 <= len(LINE) <= 200, "entry line must be 1-200 characters"
    assert len(text.encode("utf-8")) == EXPECTED_BYTES
    return text.encode("utf-8")


def check_gate(path: Path, data: bytes) -> str:
    """The kit gate, applied to the bytes we just wrote: UTF-8 text of
    1 to 200 characters, not only white space. Returns the decoded text."""
    text = data.decode("utf-8")
    stripped = text.strip()
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"gate: {len(text)} characters, need 1-200")
    if not stripped:
        raise SystemExit("gate: entry is only white space")
    if stripped != LINE:
        raise SystemExit("gate: entry text drifted from the pinned line")
    return text


def verify(path: Path, data: bytes) -> None:
    """Read the file back and prove it is exactly the pinned entry."""
    written = path.read_bytes()
    if written != data:
        raise SystemExit(f"read-back mismatch: {path} differs from memory")
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"sha256 mismatch: got {digest}")
    check_gate(path, written)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    out_dir = Path(argv[0]) if argv else Path("/output")
    path = out_dir / "entry.txt"
    data = prepare_output()
    out_dir.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    verify(path, data)
    print(f"wrote {path} ({len(data)} bytes, sha256 {EXPECTED_SHA256[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
