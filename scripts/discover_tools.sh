#!/usr/bin/env bash
# Automated AI Tool Discovery Pipeline
# Runs every 4 hours, discovers new tools, adds to library

set -euo pipefail

LIBRARY_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M)
LOG_FILE="$LIBRARY_DIR/data/discovery_${TIMESTAMP}.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

# GitHub API search queries
SEARCHES=(
  "ai agent framework"
  "mcp server"
  "local llm inference"
  "text to speech ai"
  "image generation ai"
  "rag knowledge base"
  "vector database"
  "ai coding assistant"
  "llm router"
  "ai workflow automation"
  "model serving"
  "ai monitoring"
  "prompt engineering"
  "fine tuning llm"
  "ai evaluation"
  "ai security"
  "ai red team"
  "ai benchmark"
  "ai dataset"
  "ai robotics"
  "embedded ai"
  "tinyml"
  "edge ai"
  "ai voice clone"
  "ai music generation"
  "ai video generation"
  "ai chatbot framework"
  "ai memory"
  "ai planning"
  "ai tool use"
)

CATEGORY_MAP=(
  "ai agent framework:08-ai-agents"
  "mcp server:08-ai-agents"
  "local llm inference:10-local-llms"
  "text to speech ai:07-voice-tts"
  "image generation ai:04-image-generation"
  "rag knowledge base:09-rag-knowledge"
  "vector database:09-rag-knowledge"
  "ai coding assistant:03-coding-tools"
  "llm router:10-local-llms"
  "ai workflow automation:08-ai-agents"
  "model serving:14-devops-mlops"
  "ai monitoring:14-devops-mlops"
  "prompt engineering:12-learning"
  "fine tuning llm:13-frameworks"
  "ai evaluation:18-benchmarks"
  "ai security:22-vibe-code-audit"
  "ai red team:22-vibe-code-audit"
  "ai benchmark:18-benchmarks"
  "ai dataset:17-datasets"
  "ai robotics:15-robotics-edge"
  "embedded ai:24-esp-embedded-ai"
  "tinyml:24-esp-embedded-ai"
  "edge ai:24-esp-embedded-ai"
  "ai voice clone:07-voice-tts"
  "ai music generation:06-audio-music"
  "ai video generation:05-video-generation"
  "ai chatbot framework:08-ai-agents"
  "ai memory:09-rag-knowledge"
  "ai planning:08-ai-agents"
  "ai tool use:08-ai-agents"
)

log "Starting tool discovery pipeline"
NEW_TOOLS=0

for search in "${SEARCHES[@]}"; do
  log "Searching: $search"
  
  # Get category from map
  category=""
  for mapping in "${CATEGORY_MAP[@]}"; do
    key="${mapping%%:*}"
    val="${mapping##*:}"
    if [[ "$key" == "$search" ]]; then
      category="$val"
      break
    fi
  done
  
  [[ -z "$category" ]] && continue
  
  # Search GitHub
  results=$(gh search repos "$search" --sort stars --order desc --limit 20 --json name,fullName,description,stargazersCount,updatedAt,language 2>/dev/null || echo "[]")
  
  # Process results
  echo "$results" | python3 -c "
import json, sys, os

results = json.load(sys.stdin)
category = '$category'
library_dir = '$LIBRARY_DIR'
readme_path = os.path.join(library_dir, category, 'README.md')

# Load existing tools
existing = set()
if os.path.exists(readme_path):
    with open(readme_path) as f:
        for line in f:
            if '|' in line and 'github.com' in line:
                parts = line.split('|')
                for p in parts:
                    if 'github.com' in p:
                        # Extract owner/repo
                        import re
                        match = re.search(r'github\.com/([^/\)]+/[^/\)\s]+)', p)
                        if match:
                            existing.add(match.group(1).lower())

new_count = 0
new_entries = []
for r in results:
    full_name = r.get('fullName', '').lower()
    if full_name in existing:
        continue
    if r.get('stargazersCount', 0) < 50:
        continue
    name = r.get('name', '')
    desc = (r.get('description', '') or '')[:120]
    stars = r.get('stargazersCount', 0)
    lang = r.get('language', '')
    updated = r.get('updatedAt', '')[:10]
    url = f'https://github.com/{r[\"fullName\"]}'
    
    entry = f'| [{name}]({url}) | {desc} | ⭐{stars} | {lang} | {updated} |'
    new_entries.append(entry)
    new_count += 1

if new_count > 0:
    with open(readme_path, 'a') as f:
        f.write('\n')
        for entry in new_entries:
            f.write(entry + '\n')
    print(f'ADDED:{new_count}:{category}')
else:
    print('NONE')
" 2>/dev/null | while IFS=: read -r action count cat; do
    if [[ "$action" == "ADDED" ]]; then
      log "Added $count new tools to $cat"
      NEW_TOOLS=$((NEW_TOOLS + count))
    fi
  done
done

log "Discovery complete. New tools found: $NEW_TOOLS"

# Commit if changes
cd "$LIBRARY_DIR"
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "discover: auto-added $NEW_TOOLS new tools from GitHub search"
  git push origin main 2>/dev/null || true
  log "Committed and pushed changes"
else
  log "No changes to commit"
fi

# Save run metadata
cat > "$LIBRARY_DIR/data/latest_discovery.json" << METAEOF
{
  "timestamp": "$(date -Iseconds)",
  "new_tools": $NEW_TOOLS,
  "searches_run": ${#SEARCHES[@]},
  "log_file": "$LOG_FILE"
}
METAEOF

log "Pipeline finished"
