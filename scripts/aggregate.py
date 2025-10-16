#!/usr/bin/env python3
import json, csv, sys
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR  = Path("exports")
OUT_DIR.mkdir(parents=True, exist_ok=True)

rows = []
for p in DATA_DIR.rglob("*.json"):
    try:
        with p.open(encoding="utf-8") as f:
            j = json.load(f)
        prenom  = (j.get("prenom") or "").strip()
        nom     = (j.get("nom") or "").strip()
        magasin = (j.get("magasin") or "").strip()
        ts      = (j.get("timestamp") or j.get("_workerMeta", {}).get("ts") or "").strip()
        rows.append({
            "magasin": magasin,
            "prenom": prenom,
            "nom": nom,
            "timestamp": ts,
            "source": str(p).replace("\\", "/"),
        })
    except Exception as e:
        print(f"[WARN] Skip {p}: {e}", file=sys.stderr)

# tri par date puis par chemin
rows.sort(key=lambda r: (r["timestamp"], r["source"]))

# CSV lisible
csv_path = OUT_DIR / "submissions.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["magasin", "prenom", "nom", "timestamp", "source"])
    w.writeheader()
    w.writerows(rows)

# JSON “plat”
json_path = OUT_DIR / "submissions.json"
with json_path.open("w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print(f"[OK] Écrit: {csv_path} ({len(rows)} lignes) et {json_path}")
