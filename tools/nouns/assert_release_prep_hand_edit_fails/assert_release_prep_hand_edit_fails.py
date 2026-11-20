"""Known-bad: a hand edit to FINDINGS or DESCRIBE fails the script-match check."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


_RELEASE_LINE = re.compile(
    r"(?:This release line is \*{0,2}v\d+\.\d+\.\d+\*{0,2}\. It is not tagged yet\. "
    r"|release line \*{0,2}v\d+\.\d+\.\d+\*{0,2}, not tagged yet\. )"
)


def _strip_release_line(text: str) -> str | None:
    if _RELEASE_LINE.search(text) is None:
        return None
    return _RELEASE_LINE.sub("", text, count=1)


def _copy_surface(tmp: Path, rel: str) -> None:
    dest = tmp / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes((ROOT / rel).read_bytes())


def _insert_untagged(text: str, version: str) -> str:
    prefix = f"This release line is **v{version}**. It is not tagged yet. "
    if _RELEASE_LINE.search(text):
        return text
    return prefix + text


def main() -> int:
    from nouns.release_prep_surfaces.release_prep_surfaces import (
        DESCRIBE_REL,
        FINDINGS_REL,
        RECORD_REL,
        VERSION_REL,
        line_is_tagged,
        match_errors,
        read_version,
    )

    tmp = Path(tempfile.mkdtemp())
    for rel in (FINDINGS_REL, DESCRIBE_REL, RECORD_REL, VERSION_REL):
        _copy_surface(tmp, rel)
    clean = match_errors(tmp)
    if clean:
        return _fail(f"clean copy should match script output: {clean}")

    version = read_version(ROOT)
    tagged = line_is_tagged(ROOT, version)

    findings = (tmp / FINDINGS_REL).read_text(encoding="utf-8")
    if tagged:
        (tmp / FINDINGS_REL).write_text(_insert_untagged(findings, version), encoding="utf-8")
    else:
        stripped_findings = _strip_release_line(findings)
        if stripped_findings is None:
            return _fail(
                "FINDINGS missing the untagged release-line sentence for the hand-edit landmine"
            )
        (tmp / FINDINGS_REL).write_text(stripped_findings, encoding="utf-8")
    bad_findings = match_errors(tmp)
    if not bad_findings:
        return _fail("hand-edited FINDINGS matched script output")

    _copy_surface(tmp, FINDINGS_REL)
    describe = (tmp / DESCRIBE_REL).read_text(encoding="utf-8")
    if tagged:
        (tmp / DESCRIBE_REL).write_text(_insert_untagged(describe, version), encoding="utf-8")
    else:
        stripped_describe = _strip_release_line(describe)
        if stripped_describe is None:
            return _fail(
                "DESCRIBE missing the untagged release-line sentence for the hand-edit landmine"
            )
        (tmp / DESCRIBE_REL).write_text(stripped_describe, encoding="utf-8")
    bad_describe = match_errors(tmp)
    if not bad_describe:
        return _fail("hand-edited DESCRIBE matched script output")
    print("ASSERT:PASS hand edit to FINDINGS/DESCRIBE fails script-match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
