"""Copy entry.png (next to this script) into the make.fun output directory."""

import os
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024  # 1 MiB
PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SIG = b"\xff\xd8\xff"


def validate(data: bytes) -> None:
    if not data:
        raise ValueError("entry.png is empty")
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, limit is {MAX_BYTES}")
    if not (data.startswith(PNG_SIG) or data.startswith(JPEG_SIG)):
        raise ValueError("entry.png is neither a PNG nor a JPEG")


def main() -> int:
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        data = src.read_bytes()
        validate(data)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "entry.png").write_bytes(data)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {out_dir / 'entry.png'} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
