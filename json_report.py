import json


def write_json_report(page_data, file_name="report.json"):
    pages = sorted(page_data.values(), key=lambda p: p["url"])

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)
