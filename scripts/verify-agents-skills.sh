#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATUS=0
COUNT=0

while IFS= read -r -d '' FILE; do
  COUNT=$((COUNT + 1))

  if [[ "$(sed -n '1p' "$FILE")" != "---" ]]; then
    echo "ERROR: $FILE: missing opening YAML frontmatter delimiter"
    STATUS=1
    continue
  fi

  CLOSING_LINE="$(awk 'NR > 1 && $0 == "---" { print NR; exit }' "$FILE")"
  if [[ -z "$CLOSING_LINE" ]]; then
    echo "ERROR: $FILE: missing closing YAML frontmatter delimiter"
    STATUS=1
    continue
  fi

  FRONTMATTER="$(sed -n "2,$((CLOSING_LINE - 1))p" "$FILE")"

  if ! grep -q '^name:[[:space:]]*' <<<"$FRONTMATTER"; then
    echo "ERROR: $FILE: missing frontmatter key 'name'"
    STATUS=1
  fi

  if ! grep -q '^description:[[:space:]]*' <<<"$FRONTMATTER"; then
    echo "ERROR: $FILE: missing frontmatter key 'description'"
    STATUS=1
  fi
done < <(find "$ROOT/.agents/skills" -mindepth 2 -maxdepth 2 -name SKILL.md -print0 | sort -z)

if (( COUNT == 0 )); then
  echo "ERROR: no .agents skill files found under $ROOT/.agents/skills"
  exit 1
fi

if (( STATUS != 0 )); then
  exit 1
fi

echo "Verified $COUNT .agents skill file(s)"
