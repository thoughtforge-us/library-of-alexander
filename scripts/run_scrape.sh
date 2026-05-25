#!/bin/bash
# Library of Alexander — Nexus Scraper (full power)
# Runs every 4 hours, full scraping + RE

set -e
cd /home/donn/repos/library-of-alexander

echo "=== Library of Alexander — Nexus ==="
echo "Time: $(date -u +%Y-%m-%dT%H:%M:%S) UTC"
echo "Scratch: $(du -sh /tmp/luna-ssd/scratch/ 2>/dev/null | cut -f1)"

# 1. Scrape GitHub
echo "--- Scraping ---"
python3 scripts/scrape_github.py 2>&1 | tail -15

# 2. Reverse engineer
echo "--- Reverse Engineering ---"
python3 scripts/reverse_engineer.py 2>&1 | tail -15

# 3. Commit and push
echo "--- Committing ---"
git add -A
CHANGES=$(git diff --cached --stat 2>/dev/null | tail -1)
if [ -n "$CHANGES" ]; then
    git commit -m "🔄 Nexus auto-scrape: $(date -u +%Y-%m-%d-%H:%M) UTC"
    git push origin main 2>&1 | tail -3
    echo "✅ Pushed: $CHANGES"
else
    echo "No changes"
fi

# 4. Final cleanup
echo "--- Cleanup ---"
rm -rf /tmp/luna-ssd/scratch/clones/* /tmp/luna-ssd/scratch/analysis/*
echo "Scratch after cleanup: $(du -sh /tmp/luna-ssd/scratch/ 2>/dev/null | cut -f1)"

echo "=== Done ==="
