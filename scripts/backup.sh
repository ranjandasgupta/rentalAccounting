#!/usr/bin/env bash
set -euo pipefail

# Usage: BACKUP_DIR=/mnt/nas/rental_accounting_backups DB_URL=postgresql://user:pass@host:5432/db ./backup.sh

: "${BACKUP_DIR:=/mnt/nas/rental_accounting_backups}"
: "${DB_URL:=postgresql://postgres:postgres@localhost:5432/rental_accounting}"

mkdir -p "$BACKUP_DIR"
ts=$(date +"%Y%m%d_%H%M%S")
pg_dump "$DB_URL" > "$BACKUP_DIR/rental_accounting_${ts}.sql"
echo "Backup written to $BACKUP_DIR/rental_accounting_${ts}.sql"
