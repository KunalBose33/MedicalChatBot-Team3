from __future__ import annotations
import io, csv, json, re
from typing import List, Dict
from pathlib import Path
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

DISCLAIMER = "This is educational information only and not medical advice."

# Load extended reference ranges (50+ tests)
REF_PATH = Path(__file__).parent.parent / "config" / "reference_ranges.json"
if REF_PATH.exists():
    with open(REF_PATH, "r") as f:
        REFS = json.load(f)
else:
    REFS = {}

def parse_csv_bytes(b: bytes) -> List[Dict]:
    text = b.decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text)))
    return rows

def parse_fhir_bytes(b: bytes) -> List[Dict]:
    bundle = json.loads(b.decode("utf-8"))
    out = []
    for entry in bundle.get("entry", []):
        res = entry.get("resource", {})
        if res.get("resourceType") == "Observation" and "valueQuantity" in res:
            code = None
            codings = res.get("code", {}).get("coding", [])
            if codings:
                code = codings[0].get("display") or codings[0].get("code")
            out.append({
                "test_name": code or res.get("code", {}).get("text", "Unknown"),
                "value": res["valueQuantity"].get("value"),
                "unit": res["valueQuantity"].get("unit"),
                "sex": None,
                "age": None,
            })
    return out

def parse_pdf_bytes(b: bytes) -> List[Dict]:
    """
    Convert PDF (including scanned) into structured lab test results.
    Looks for lines like 'Glucose 180 mg/dL' or 'Hemoglobin: 13.5 g/dL'
    """
    records = []
    pages = convert_from_bytes(b)

    for page in pages:
        text = pytesseract.image_to_string(page)
        for line in text.splitlines():
            match = re.match(r"([A-Za-z0-9 \-\(\)\/]+)[: ]+([\d\.]+)\s*([A-Za-z\/\^\%\d]+)?", line)
            if match:
                test_name = match.group(1).strip()
                value = match.group(2)
                unit = match.group(3) or ""
                try:
                    records.append({
                        "test_name": test_name,
                        "value": float(value),
                        "unit": unit,
                        "sex": None,
                        "age": None,
                    })
                except ValueError:
                    continue
    return records

def normalize_and_score(rows: List[Dict]) -> Dict:
    per_test = []
    flagged = []

    for r in rows:
        name = (r.get("test_name") or "").strip()
        value = float(r.get("value", 0))
        unit = (r.get("unit") or "").strip()
        sex = (r.get("sex") or "").strip().lower() or None

        status = "unknown"
        reference = None

        if name in REFS:
            entry = REFS[name]
            normal_low, normal_high = None, None

            if isinstance(entry, dict) and "general" in entry:
                normal_low, normal_high = entry["general"]
            elif isinstance(entry, dict) and sex and sex in entry:
                normal_low, normal_high = entry[sex]

            if normal_low is not None and normal_high is not None:
                reference = f"{normal_low}–{normal_high} {entry.get('unit','')}"
                if value < normal_low:
                    status = "low"
                elif value > normal_high:
                    status = "high"
                else:
                    status = "normal"

        per_test.append({
            "test_name": name,
            "value": value,
            "unit": unit,
            "status": status,
            "reference": reference,
        })

        if status in ("low", "high"):
            flagged.append(f"{name}: {value}{unit} ({status})")

    return {"per_test": per_test, "flagged": flagged, "disclaimer": DISCLAIMER}
