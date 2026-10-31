#!/usr/bin/env python3
"""Tidy creators.csv (fill engagement rate, drop duplicates, sort by score) and write shortlist.md."""

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "creators.csv"
SHORTLIST = HERE / "shortlist.md"


def num(value):
    try:
        return float(str(value).replace(",", "").replace("%", "").strip())
    except ValueError:
        return None


def tier(score):
    if score is None:
        return ""
    if score >= 80:
        return "priority"
    if score >= 65:
        return "strong"
    if score >= 50:
        return "hold"
    return "skip"


def main():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    seen, unique = set(), []
    for row in rows:
        key = (row["platform"].lower(), row["handle"].lower().lstrip("@"))
        if key in seen:
            continue
        seen.add(key)
        followers, likes, comments = num(row["followers"]), num(row["avg_likes"]), num(row["avg_comments"])
        if not row["engagement_rate"] and followers and likes is not None:
            row["engagement_rate"] = f"{(likes + (comments or 0)) / followers * 100:.2f}%"
        if not row["tier"]:
            row["tier"] = tier(num(row["score"]))
        unique.append(row)

    unique.sort(key=lambda r: num(r["score"]) or -1, reverse=True)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(unique)

    lines = [
        "# Creator shortlist",
        "",
        "| # | Handle | Followers | Engagement | Score | Tier | Gift | Status | Why |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate([r for r in unique if (num(r["score"]) or 0) >= 50], 1):
        lines.append(
            f"| {i} | [@{r['handle'].lstrip('@')}]({r['profile_url']}) | {r['followers']} | "
            f"{r['engagement_rate']} | {r['score']} | {r['tier']} | {r['suggested_gift']} | "
            f"{r['status']} | {r['vibe_notes']} |"
        )
    SHORTLIST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(unique)} creators, shortlist written to {SHORTLIST}", file=sys.stderr)


if __name__ == "__main__":
    main()
