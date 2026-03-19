from __future__ import annotations
import csv
import json
from datetime import date, datetime
from pathlib import Path
from domain.entities.job_offer import JobOffer


class JobOfferETL:
    REQUIRED_COLUMNS = {"offer_id", "title", "description", "industry", "published_at", "company", "location"}

    def load_dataframe(self, source: str) -> list[dict]:
        path = Path(source)
        if path.suffix.lower() == ".csv":
            with path.open("r", encoding="utf-8", newline="") as handler:
                rows = list(csv.DictReader(handler))
        elif path.suffix.lower() == ".json":
            rows = json.loads(path.read_text(encoding="utf-8"))
        else:
            raise ValueError(f"Unsupported source format: {path.suffix}")

        if not rows:
            return []
        missing = self.REQUIRED_COLUMNS.difference(rows[0].keys())
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")

        deduplicated: dict[str, dict] = {}
        for row in rows:
            deduplicated[row["offer_id"]] = row
        return list(deduplicated.values())

    def preprocess(self, rows: list[dict]) -> list[dict]:
        clean_rows: list[dict] = []
        for row in rows:
            item = dict(row)
            item["description"] = " ".join((item.get("description") or "").split())
            item["title"] = (item.get("title") or "").strip()
            value = item.get("published_at")
            item["published_at"] = value if isinstance(value, date) else datetime.fromisoformat(str(value)).date()
            clean_rows.append(item)
        return clean_rows

    def to_entities(self, rows: list[dict]) -> list[JobOffer]:
        return [JobOffer(**record) for record in rows]

    def export_records(self, records: list[dict], output_path: str) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == ".json":
            path.write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")
            return
        if not records:
            path.write_text("", encoding="utf-8")
            return
        with path.open("w", encoding="utf-8", newline="") as handler:
            writer = csv.DictWriter(handler, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
