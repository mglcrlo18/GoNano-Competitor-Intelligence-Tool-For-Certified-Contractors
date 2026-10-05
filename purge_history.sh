#!/usr/bin/env bash
# Git DAG history purge script using git-filter-repo
# Requires git-filter-repo: pip install git-filter-repo OR brew install git-filter-repo

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== GoNano Competitor Intelligence // Git DAG History Purge ==="

if ! command -v git-filter-repo &> /dev/null; then
    echo "[!] git-filter-repo is not in PATH."
    echo "    Install via: pip install git-filter-repo OR brew install git-filter-repo"
    exit 1
fi

echo "[1/3] Verifying expressions.txt..."
if [ ! -f "expressions.txt" ]; then
    echo "[!] expressions.txt not found!"
    exit 1
fi

echo "[2/3] Executing git-filter-repo --replace-text expressions.txt --force..."
git-filter-repo --replace-text expressions.txt --force

echo "[3/3] Git history successfully rewritten and sanitized!"
echo "To push changes to remote (ensure CI/CD is paused):"
echo "  git push --force-with-lease origin main"
