"""
Stream-ingest a large PDF into text chunks with page range + progress.
Writes each chunk immediately (no big lists in memory).

Usage examples:
  python scripts/ingest_pdf.py "C:\\path\\to\\gale.pdf"
  python scripts/ingest_pdf.py "C:\\path\\to\\gale.pdf" --start 1 --end 40
"""
import sys, re, json, argparse
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).parents[1]
OUTDIR = ROOT / "app" / "kb_chunks"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Tune these
CHUNK_SIZE = 2000   # characters per chunk (bigger = fewer files, faster)
OVERLAP    = 100    # characters to keep from the previous chunk

def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def write_chunk(manifest_fh, chunk_id: int, text: str):
    fname = OUTDIR / f"gale_chunk_{chunk_id:04d}.txt"
    fname.write_text(text, encoding="utf-8")
    rec = {
        "id": f"gale_chunk_{chunk_id:04d}",
        "file": fname.name,
        "source": "gale_pdf",
        "url": None,
        "chars": len(text),
    }
    manifest_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

def ingest_pdf(pdf_path: Path, start: int | None, end: int | None):
    if not pdf_path.exists():
        print(f"[ERROR] File not found: {pdf_path}")
        sys.exit(1)

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    s = max(1, start or 1)
    e = min(end or total_pages, total_pages)
    if s > e:
        print(f"[ERROR] start page {s} > end page {e}")
        sys.exit(1)

    print(f"[INFO] Reading pages {s}..{e} of {total_pages} from {pdf_path.name}")

    # Rolling buffer; we only keep at most CHUNK_SIZE + OVERLAP chars
    buf = ""
    written = 0
    manifest_path = OUTDIR / "manifest.jsonl"

    # If you’re re-running, you can uncomment the next two lines to clear old outputs:
    # for old in OUTDIR.glob("gale_chunk_*.txt"): old.unlink(missing_ok=True)
    # manifest_path.unlink(missing_ok=True)

    with open(manifest_path, "w", encoding="utf-8") as mf:
        for pnum in range(s - 1, e):
            try:
                page_text = reader.pages[pnum].extract_text()
            except Exception:
                page_text = ""
            buf += " " + clean_text(page_text)

            # progress
            if (pnum + 1) % 25 == 0:
                print(f"[INFO] processed page {pnum+1}")

            # While buffer is long enough, emit chunks and keep only the overlap tail
            while len(buf) >= CHUNK_SIZE:
                chunk = buf[:CHUNK_SIZE].strip()
                if chunk:
                    written += 1
                    write_chunk(mf, written, chunk)
                # Keep only the end tail for overlap
                buf = buf[CHUNK_SIZE - OVERLAP:]

        # Final remainder
        if buf.strip():
            written += 1
            write_chunk(mf, written, buf.strip())

    print(f"[OK] Wrote {written} chunks to {OUTDIR} and updated manifest.jsonl")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", help="Path to PDF")
    ap.add_argument("--start", type=int, help="Start page (1-based)")
    ap.add_argument("--end", type=int, help="End page (inclusive, 1-based)")
    args = ap.parse_args()
    ingest_pdf(Path(args.pdf), args.start, args.end)
