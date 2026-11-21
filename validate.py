"""Validate two localization CSV files with id and text columns."""
import argparse
import csv
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"@[A-Za-z_][\w.-]*#|#c[0-9a-fA-F]{6}|#[nr]|%(?:\d+\$)?[sdif]|\{\w+\}|\\[nrt]|\r\n|\r|\n")
FIELDS = ["id", "text"]


def read_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        if next(reader, None) != FIELDS:
            raise ValueError(f"{path}: expected header id,text")
        rows = {}
        for row in reader:
            if len(row) != 2:
                raise ValueError(f"{path}:{reader.line_num}: expected two columns")
            row_id, message = row
            if not row_id.strip() or row_id in rows:
                raise ValueError(f"{path}:{reader.line_num}: blank or duplicate ID {row_id!r}")
            rows[row_id] = message
    return rows


def validate(source, target):
    issues = []
    for row_id in sorted(source.keys() - target.keys()):
        issues.append(f"{row_id}: missing translation")
    for row_id in sorted(target.keys() - source.keys()):
        issues.append(f"{row_id}: unexpected ID")
    for row_id in source.keys() & target.keys():
        original, translated = source[row_id], target[row_id]
        if original.strip() and not translated.strip():
            issues.append(f"{row_id}: blank translation")
        expected, actual = TOKEN.findall(original), TOKEN.findall(translated)
        if expected != actual:
            issues.append(f"{row_id}: expected tokens {expected!r}, found {actual!r}")
    return sorted(issues)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("translation", type=Path)
    args = parser.parse_args()
    try:
        issues = validate(read_rows(args.source), read_rows(args.translation))
    except (OSError, ValueError, csv.Error) as exc:
        print(exc, file=sys.stderr)
        return 2
    if issues:
        print("\n".join(issues), file=sys.stderr)
        return 1
    print("PASS: row IDs and protected tokens match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
