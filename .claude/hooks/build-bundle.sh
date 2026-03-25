#!/bin/bash
# build-bundle.sh — generates .cache/ bundles for context bundling
# Called by session-start.sh and sync-and-rebuild.sh
# MUST be silent (no stdout) — SessionStart stdout enters Claude context

set -euo pipefail
PROJ_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CACHE_DIR="$PROJ_ROOT/.cache"
mkdir -p "$CACHE_DIR"

MODE="${1:---all}"  # --all | --only=common | --only=frontmatter

# --- Helper: check if cache is newer than all sources ---
cache_fresh() {
  local cache_file="$1"
  shift
  [[ ! -f "$cache_file" ]] && return 1
  for src in "$@"; do
    [[ -f "$src" && "$src" -nt "$cache_file" ]] && return 1
  done
  return 0
}

# === COMMON CONTEXT BUNDLE (English) ===
build_common() {
  local IDENTITY="$PROJ_ROOT/profile/identity.md"
  local PREFS="$PROJ_ROOT/preferences.md"
  local TEMPLATE_EN="$PROJ_ROOT/templates/resume_en.md"
  local GLOSSARY="$PROJ_ROOT/profile/locale/glossary.yaml"
  local OUT_EN="$CACHE_DIR/common_context_en.md"
  local OUT_I18N="$CACHE_DIR/common_context_i18n.md"

  # English bundle (no glossary)
  if ! cache_fresh "$OUT_EN" "$IDENTITY" "$PREFS" "$TEMPLATE_EN"; then
    {
      echo "# === IDENTITY ==="
      echo ""
      cat "$IDENTITY"
      echo ""
      echo "# === PREFERENCES ==="
      echo ""
      cat "$PREFS"
      echo ""
      echo "# === TEMPLATE ==="
      echo ""
      cat "$TEMPLATE_EN"
    } > "$OUT_EN"
  fi

  # i18n bundle (with glossary) — only if glossary exists
  if [[ -f "$GLOSSARY" ]]; then
    if ! cache_fresh "$OUT_I18N" "$IDENTITY" "$PREFS" "$TEMPLATE_EN" "$GLOSSARY"; then
      {
        echo "# === IDENTITY ==="
        echo ""
        cat "$IDENTITY"
        echo ""
        echo "# === PREFERENCES ==="
        echo ""
        cat "$PREFS"
        echo ""
        echo "# === TEMPLATE ==="
        echo ""
        cat "$TEMPLATE_EN"
        echo ""
        echo "# === GLOSSARY ==="
        echo ""
        cat "$GLOSSARY"
      } > "$OUT_I18N"
    fi
  fi
}

# === PROJECT FRONTMATTER BUNDLE ===
build_frontmatter() {
  local PROJECTS_DIR="$PROJ_ROOT/profile/projects"
  local OUT="$CACHE_DIR/project_frontmatter.yaml"

  # Check if any project file is newer than cache
  local needs_rebuild=false
  if [[ ! -f "$OUT" ]]; then
    needs_rebuild=true
  else
    while IFS= read -r -d '' f; do
      [[ "$f" -nt "$OUT" ]] && needs_rebuild=true && break
    done < <(find "$PROJECTS_DIR" -maxdepth 1 -name "*.md" -print0)
  fi

  if $needs_rebuild; then
    {
      echo "# Canonical source: profile/projects/*.md frontmatter"
      echo "# Derived cache — do not edit directly"
      echo ""
      # Process files in sorted order (by filename) for determinism
      # Use find + sort + while read to handle paths with spaces
      find "$PROJECTS_DIR" -maxdepth 1 -name "*.md" -print0 | sort -z | while IFS= read -r -d '' f; do
        # Extract YAML frontmatter (between --- markers)
        # Format as YAML list: first line gets "- " prefix, rest get "  " indent
        awk '
          BEGIN { in_fm=0; started=0; first_line=1 }
          /^---$/ {
            if (!started) { started=1; in_fm=1; next }
            else { in_fm=0; exit }
          }
          in_fm {
            if (first_line) { print "- " $0; first_line=0 }
            else { print "  " $0 }
          }
        ' "$f"
        echo ""
      done
    } > "$OUT"
  fi
}

# === Main ===
case "$MODE" in
  --all)
    build_common
    build_frontmatter
    ;;
  --only=common)
    build_common
    ;;
  --only=frontmatter)
    build_frontmatter
    ;;
esac

exit 0
