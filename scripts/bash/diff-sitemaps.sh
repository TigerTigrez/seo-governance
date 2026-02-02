#!/usr/bin/env bash
# Compare two sitemap URL lists and show additions/removals.
# Usage: ./diff-sitemaps.sh old.txt new.txt

set -euo pipefail
old="${1:-old.txt}"
new="${2:-new.txt}"

echo "Added:"
comm -13 <(sort "$old") <(sort "$new")
echo
echo "Removed:"
comm -23 <(sort "$old") <(sort "$new")
