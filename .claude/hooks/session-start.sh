#!/bin/bash
# Build cache bundles silently. No echo — CLAUDE.md has all needed instructions.
PROJ_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
"$PROJ_ROOT/.claude/hooks/build-bundle.sh" 2>/dev/null
exit 0
