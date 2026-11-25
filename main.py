"""Write the entry line for the make.fun bounty "One Line, One Laugh".

The program holds one joke line in ENTRY, validates it against the bounty's
gate (UTF-8, 1..200 code points, one line, no surrounding white space), and
writes it with a trailing newline to entry.txt inside the output directory.
The output directory is MAKEFUN_OUTPUT_DIR when set, otherwise /output.

It is deterministic: no clock, randomness, network, or third-party packages,
so every run produces the same bytes.
"""

import os
import sys

ENTRY = (
    "My card was declined for a dollar fifty and the machine apologised to me first, "
    "which somehow made it worse."
)

DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"
MAX_LENGTH = 200


def validate_entry(text):
    """Return an error message, or None when text is a valid entry line."""
    if not isinstance(text, str):
        return "entry is not a string"
    if not text.strip():
        return "entry is empty or only white space"
    if not 1 <= len(text) <= MAX_LENGTH:
        return "entry must be 1..%d characters, got %d" % (MAX_LENGTH, len(text))
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if text != text.strip():
        return "entry must not have leading or trailing white space"
    return None


def main():
    error = validate_entry(ENTRY)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILENAME)

    payload = ENTRY + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)

    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != payload:
        print("readback mismatch: %s does not match the entry" % path, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
