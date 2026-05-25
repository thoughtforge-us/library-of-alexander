#!/bin/bash
# Library of Alexander — Run once and exit (for cron)
cd /home/donn/repos/library-of-alexander
echo "=== $(date -u +%Y-%m-%dT%H:%M:%S) UTC | Node: $(hostname) ===" >> data/scrape.log
python3 scripts/pipeline.py --once >> data/scrape.log 2>&1
echo "=== Done ===" >> data/scrape.log
