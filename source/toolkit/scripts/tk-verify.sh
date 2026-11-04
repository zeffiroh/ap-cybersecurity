sha256sum -c "${1:-/tmp/evidence.sha256}" 2>&1 | grep -v ": OK$"
if sha256sum -c "${1:-/tmp/evidence.sha256}" >/dev/null 2>&1; then echo "Every file matches."; else echo "Some files changed or are missing."; exit 1; fi
