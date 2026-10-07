from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
required = ["README.md", "LICENSE", "SUBMISSION_TEXT.md", "vec_xspecies/metrics.py", "scripts/benchmark.py", "tests/test_metrics.py", "references/reading.md"]
missing = [x for x in required if not (ROOT / x).is_file()]
if missing: raise SystemExit(f"Missing files: {missing}")
text = "\n".join(p.read_text(errors="ignore") for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".md", ".py", ".yml"})
if re.search(r"[\u4e00-\u9fff]", text): raise SystemExit("Repository must remain English-only")
if list(ROOT.rglob("*.h5ad")): raise SystemExit("Expression data detected")
print("Repository audit passed.")
