"""Evidence-record schema for §2.7 review programs.

Constitutional basis
--------------------
CONSTITUTION.md §2.7 (review provenance: verified identity + locator +
retrieval timestamp), §5.3 (citations carry a traceable locator), §11
(reproducibility).

Why a schema at all
-------------------
Task 31's register was a bare list of dicts. Nothing checked that a record had
a source, that its confidence value was one of the three the rubric defines, or
that a figure carrying a headline had a locator behind it. Three defects got
through — two transposed figures and a transposed DOI — and none of them were
exotic. They were the ordinary consequence of a register with no shape.

This module gives the register a shape and makes §2.7 mechanically checkable
before a build runs, rather than after a reader notices.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Fields every record must carry. These are the extraction fields a review
# brief asks for; a record missing one cannot be assessed by a reader.
REQUIRED = (
    "id", "category", "study", "year", "source", "geography", "subregion",
    "population", "shock", "welfare_indicator", "estimate", "methodology",
    "identification", "limitations", "confidence", "evidence_type",
)

# Present but allowed to be empty: a gray-literature record has no DOI, and a
# record still on the source queue has no locator yet.
OPTIONAL = ("url", "doi", "locator", "notes")

CONFIDENCE_VALUES = ("High", "Medium", "Low")


@dataclass
class Problem:
    record_id: str
    field_name: str
    message: str
    blocking: bool = True

    def __str__(self) -> str:
        mark = "BLOCK" if self.blocking else "warn "
        return f"[{mark}] {self.record_id}.{self.field_name}: {self.message}"


@dataclass
class ValidationResult:
    problems: list[Problem] = field(default_factory=list)

    @property
    def blocking(self) -> list[Problem]:
        return [p for p in self.problems if p.blocking]

    @property
    def ok(self) -> bool:
        return not self.blocking

    def report(self) -> str:
        if not self.problems:
            return "Schema OK — every record well formed."
        return "\n".join(str(p) for p in self.problems)


def validate(records: list[dict]) -> ValidationResult:
    """Check a register against the §2.7 record shape."""
    result = ValidationResult()
    seen_ids: set[str] = set()

    for rec in records:
        rid = rec.get("id") or "<no id>"

        if rid in seen_ids:
            result.problems.append(
                Problem(rid, "id", "duplicate record id"))
        seen_ids.add(rid)

        for key in REQUIRED:
            value = rec.get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                result.problems.append(
                    Problem(rid, key, "required field missing or empty"))

        conf = rec.get("confidence")
        if conf and conf not in CONFIDENCE_VALUES:
            result.problems.append(Problem(
                rid, "confidence",
                f"{conf!r} is not one of {CONFIDENCE_VALUES}"))

        if not rec.get("url") and not rec.get("doi"):
            result.problems.append(Problem(
                rid, "url",
                "record has neither a URL nor a DOI, so its identity cannot "
                "be verified at all (§2.7a)"))

        year = rec.get("year")
        if isinstance(year, int) and not (1900 <= year <= 2100):
            result.problems.append(
                Problem(rid, "year", f"implausible year {year}"))

        # Not blocking: a record may legitimately sit in the register awaiting
        # a locator. §2.7 bars it from the synthesis, not from the register.
        if not rec.get("locator"):
            result.problems.append(Problem(
                rid, "locator",
                "no locator — barred from headline, table, figure, and "
                "synthesis use until one exists (§2.7b)",
                blocking=False))

        unknown = set(rec) - set(REQUIRED) - set(OPTIONAL)
        for key in sorted(unknown):
            result.problems.append(Problem(
                rid, key, "unrecognized field", blocking=False))

    return result


def citable(rec: dict, verified_ids: set[str]) -> bool:
    """May this record's figures appear in a headline or synthesis sentence?

    §2.7 requires both halves: verified identity *and* a locator. Either alone
    is insufficient, which is the whole point — a resolving citation can still
    be the wrong citation, and a located number can still be the wrong number.
    """
    return bool(rec.get("locator")) and rec.get("id") in verified_ids
