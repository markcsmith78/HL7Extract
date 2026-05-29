#!/usr/bin/env python3

import sys
from pathlib import Path

START_BLOCK = b"\x0b"
END_BLOCK = b"\x1c"
CARRIAGE_RETURN = b"\x0d"


def frame_hl7_message(message: bytes) -> bytes:
    # Remove trailing whitespace/newlines so the MLLP trailer is clean
    message = message.rstrip()

    return START_BLOCK + message + END_BLOCK + CARRIAGE_RETURN


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1.hl7 [file2.hl7 ...]", file=sys.stderr)
        sys.exit(1)

    for filename in sys.argv[1:]:
        path = Path(filename)

        try:
            message = path.read_bytes()
            framed_message = frame_hl7_message(message)

            # Write bytes directly to stdout
            sys.stdout.buffer.write(framed_message)

        except OSError as e:
            print(f"File error with {filename}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
