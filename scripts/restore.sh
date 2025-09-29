#!/usr/bin/env bash
set -euo pipefail
# Usage: DB_URL=postgresql://user:pass@host:5432/db ./restore.sh /path/to/backup.sql
: "${DB_URL:=postgresql://postgres:postgres@localhost:5432/rental_accounting}"

if [ $# -lt 1 ]; then
  echo "Provide a backup sql file"
  exit 1
fi

psql "$DB_URL" < "$1"
echo "Restore complete"
