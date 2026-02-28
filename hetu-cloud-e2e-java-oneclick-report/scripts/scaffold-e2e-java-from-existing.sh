#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scaffold-e2e-java-from-existing.sh --source <dir> --dest <dir> --from-name <old> --to-name <new>

Notes:
  - Copies an existing Java E2E project directory and does a best-effort rename in text files.
  - This is a helper; you still need to adjust controllers/clients/payloads/tests manually.
  - Designed for projects similar to company-feed-curve-e2e-java / company-feed-scheme-e2e-java.

Example:
  ./scripts/scaffold-e2e-java-from-existing.sh \
    --source /path/company-feed-curve-e2e-java \
    --dest   /path/company-feed-scheme-e2e-java \
    --from-name company-feed-curve-e2e-java \
    --to-name   company-feed-scheme-e2e-java
EOF
}

SOURCE=""
DEST=""
FROM_NAME=""
TO_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) SOURCE="${2:-}"; shift 2 ;;
    --dest) DEST="${2:-}"; shift 2 ;;
    --from-name) FROM_NAME="${2:-}"; shift 2 ;;
    --to-name) TO_NAME="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 2 ;;
  esac
done

if [[ -z "${SOURCE}" || -z "${DEST}" || -z "${FROM_NAME}" || -z "${TO_NAME}" ]]; then
  usage
  exit 2
fi

if [[ ! -d "${SOURCE}" ]]; then
  echo "[ERR] source dir not found: ${SOURCE}"
  exit 1
fi

if [[ -e "${DEST}" ]]; then
  echo "[ERR] dest already exists: ${DEST}"
  exit 1
fi

echo "[OK] Copying..."
cp -R "${SOURCE}" "${DEST}"

echo "[OK] Renaming in text files..."
python3 - <<'PY'
import os
from pathlib import Path

src = Path(os.environ["DEST"])
from_name = os.environ["FROM_NAME"]
to_name = os.environ["TO_NAME"]

text_ext = {".md",".xml",".java",".properties",".yml",".yaml",".env",".gitignore",".txt",".sh"}

for p in src.rglob("*"):
    if not p.is_file():
        continue
    if p.name.startswith(".") and p.suffix == "":
        # allow .env.example etc
        pass
    if p.suffix and p.suffix.lower() not in text_ext:
        continue
    try:
        data = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if from_name in data:
        p.write_text(data.replace(from_name, to_name), encoding="utf-8")

print("[OK] Done")
PY

echo "[OK] Scaffold complete: ${DEST}"

