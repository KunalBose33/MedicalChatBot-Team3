""" replace this with Azure AI Search ingestion.
"""
from pathlib import Path
kb_path = Path(__file__).parents[1] / "app" / "kb"
print(f"Loaded KB documents:")
for p in sorted(kb_path.glob("*.md")):
    print(" -", p.name)
print("Done. (No Azure required for this step.)")
