#!/bin/bash
# PostToolUse hook — sync index + selective cache rebuild on source changes
# Triggered after Write/Edit. PostToolUse stdout does NOT enter Claude context
# (only in verbose mode), so echo here is for log cleanliness only.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
PROJ_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# --- Project file changed → index sync + frontmatter rebuild ---
if [[ "$FILE_PATH" == *"profile/projects/"* && "$FILE_PATH" == *".md" ]]; then
  PROJECT_ID=$(basename "$FILE_PATH" .md)
  mkdir -p "$PROJ_ROOT/.cache"
  echo "$(date +%Y-%m-%dT%H:%M) INDEX_SYNC: $PROJECT_ID" >> "$PROJ_ROOT/.cache/hook_log.txt"
  "$PROJ_ROOT/.claude/hooks/build-bundle.sh" --only=frontmatter 2>/dev/null
fi

# --- Common context source changed → rebuild common bundle ---
if [[ "$FILE_PATH" == *"identity.md" || "$FILE_PATH" == *"preferences.md" || \
      "$FILE_PATH" == *"templates/"* || "$FILE_PATH" == *"glossary.yaml" ]]; then
  "$PROJ_ROOT/.claude/hooks/build-bundle.sh" --only=common 2>/dev/null
fi

# --- Log output file changes ---
if [[ "$FILE_PATH" == *"outputs/"* ]]; then
  mkdir -p "$PROJ_ROOT/.cache"
  echo "$(date +%Y-%m-%dT%H:%M) OUTPUT: $FILE_PATH" >> "$PROJ_ROOT/.cache/hook_log.txt"
fi

exit 0
