# prepare_dataset.py
import csv
import json

INPUT_FILE = "data/emails.csv"
OUTPUT_FILE = "data/emails.json"

def build_expected(category, text):
    if category == "spam":
        return [
            {"type": "classify", "value": "spam"},
            {"type": "archive"}
        ]

    if category == "urgent":
        return [
            {"type": "classify", "value": "urgent"},
            {"type": "prioritize", "value": "high"},
            {"type": "escalate"}
        ]

    if category == "support":
        return [
            {"type": "classify", "value": "support"},
            {"type": "prioritize", "value": "high"},
            {"type": "reply", "content": "We are looking into your issue"}
        ]

    return [
        {"type": "classify", "value": "general"},
        {"type": "archive"}
    ]


def map_category(label, text):
    text = text.lower()

    if label == "spam":
        return "spam"

    if "urgent" in text or "asap" in text:
        return "urgent"

    if "issue" in text or "help" in text:
        return "support"

    return "general"


emails = []

with open(INPUT_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        text = row.get("text") or ""
        label = row.get("label", "ham")

        category = map_category(label, text)
        expected = build_expected(category, text)

        emails.append({
            "id": str(i),
            "subject": text[:50],
            "body": text,
            "sender": f"user{i}@mail.com",
            "category": category,
            "priority": "high" if category in ["urgent", "support"] else "low",
            "expected_actions": expected
        })

emails = emails[:120]

with open(OUTPUT_FILE, "w") as f:
    json.dump(emails, f, indent=2)

print("✅ Advanced dataset ready!")