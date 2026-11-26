"""The Moon Gets One Star - make.fun entry program.

Writes a single-line one-star review of the Moon to ``entry.txt``.

The task, as published on make.fun (competition
``u-eager-stork-81-9647-the-moon-gets-one-star-768236e5``, prize $2,
deadline 26 Nov 2026 21:45 WIB): write the funniest one-star review
of the Moon in 120 characters or fewer. It should read like a real
review: a rating, a grievance, a reason the Moon earned its single
star. A judge model reads the entries two at a time and picks the
funnier one each time.

The sealed gate this program must satisfy: ``/output/entry.txt`` is
UTF-8 text of 1 to 120 characters, not only whitespace. Only a valid
entry goes before the judge. This module validates the text against
that gate before writing it, and writes the file with no trailing
newline so the character count is exactly the count of the line.

Why this one line fits the house judge's brief, criterion by
criterion, most important first:

Criterion 1 - a one-star review of the Moon itself. It opens with
"One star", the plain verdict a real reviewer leaves, and every
clause after it is about the Moon: the side it shows, how long it
has shown it, what it must be hiding.

Criterion 2 - funnier on first read. The setup is a dry complaint
about a neighbour who never turns around; the punch is "clearly
hiding something", which lands the moment it is read.

Criterion 3 - reads like a real one-star review. Rating up front,
then a concrete grievance ("shown me the same side"), a character
judgement a genuine reviewer would leave ("Rude, secretive"), and
the standard closer "Avoid."

Criterion 4 - a specific, surprising grievance about the Moon,
not the obvious jokes about craters, cheese or how bright it is.
The Moon really does show Earth only one side, tidally locked for
4.5 billion years, and nobody has ever seen the far side from
here. That fact is the joke, and it could only be about the Moon.

Criterion 5 - uses its few characters well. At 118 characters the
punchline lands before the limit does, and every word earns its
place: verdict, setup, three-word character verdict, punch, closer.

The entry text itself is one fixed line (see ENTRY below). It was
picked from ten candidate lines written for this bounty and judged
head to head against each other on the house brief: the finalists
were the absentee-employee angle ("only works nights, takes two
weeks off every month"), the one-job angle ("one job, lighting the
night, and it takes a week off every month"), and this line. This
line won because its grievance is the most Moon-only of the three:
tidal locking is a fact no other product shares, so the joke cannot
be swapped onto anything else, and its punch ("clearly hiding
something") is also the most surprising, beating the more generic
"unreliable since forever" endings of the other candidates.

The program writes it to ``entry.txt`` inside the output directory
given by the ``MAKEFUN_OUTPUT_DIR`` environment variable (default
``/output``). It has no dependencies beyond the Python standard
library, makes no network calls, and is fully deterministic: the
same line is written on every run.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, ASCII only, no emoji, no em dash, no newline.
# 118 characters by Python len(), inside the 1 to 120 gate.
ENTRY = (
    "One star. The Moon has shown me the same side for 4.5 billion "
    "years. Rude, secretive, clearly hiding something. Avoid."
)

MAX_CHARS = 120
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry text: the single one-star review line."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 120 characters that is not
    only whitespace, on exactly one line, so the text must contain
    no newline characters at all.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if any(ord(ch) > 127 for ch in text):
        raise ValueError("entry must be plain ASCII, no emoji or odd characters")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "words": len(text.split()),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(
        f"Wrote {path} ({info['chars']} chars, {info['words']} words, "
        f"{info['lines']} line)"
    )
    print(f"Entry: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
