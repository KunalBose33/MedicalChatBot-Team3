from __future__ import annotations
import io, csv, json
from typing import List, Dict

REFS = {
    "HbA1c": {"unit": "%", "ranges": {"normal": (0, 5.7), "prediabetes": (5.7, 6.5), "diabetes": (6.5, 50)}},
    "LDL": {"unit": "mg/dL", "ranges": {"optimal": (0, 100), "borderline": (100, 129), "high": (130, 1000)}},
    "HDL_male": {"unit": "mg/dL", "ranges": {"low": (0, 40), "normal": (40, 1000)}},
    "HDL_female": {"unit": "mg/dL", "ranges": {"low": (0, 50), "normal": (50, 1000)}},
}

DISCLAIMER = "This is educational information only and not medical advice."

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

def normalize_and_score(rows: List[Dict]) -> Dict:
    per_test = []
    for r in rows:
        name = (r.get("test_name") or "").strip()
        value = float(r.get("value", 0))
        unit = (r.get("unit") or "").strip()
        sex = (r.get("sex") or "").strip().lower() or None

        status = "unknown"
        reference = None
        note = None

        if name == "HbA1c":
            ref = REFS["HbA1c"]
            reference = "< 5.7% normal; 5.7–6.4% prediabetes; ≥ 6.5% diabetes"
            if value < 5.7: status = "normal"
            elif value < 6.5: status = "borderline-high"
            else: status = "high"
            note = "Consider diet, activity; follow up with a clinician."
        elif name == "LDL":
            ref = REFS["LDL"]
            reference = "Optimal < 100 mg/dL"
            if value < 100: status = "normal"
            elif value < 130: status = "borderline-high"
            else: status = "high"
            note = "Lifestyle changes are helpful; discuss targets with a clinician."
        elif name == "HDL":
            key = "HDL_male" if sex == "male" else "HDL_female"
            reference = "Male: >=40 mg/dL; Female: >=50 mg/dL"
            if value < (40 if sex == "male" else 50):
                status = "low"
                note = "Low HDL may increase risk; consider exercise and diet."
            else:
                status = "normal"
                note = "HDL in a healthy range."

        per_test.append({
            "test_name": name,
            "value": value,
            "unit": unit,
            "status": status,
            "reference": reference,
            "note": note,
            "source": "kb/lipids.md" if name in ("LDL", "HDL") else "kb/diabetes.md"
        })
    
    summary = "Basic interpretation generated. This is not medical advice."
    return {"summary": summary, "per_test": per_test, "disclaimer": DISCLAIMER}
