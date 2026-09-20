#!/usr/bin/env bash
# Nightly backup of the SQLite DB and generated reports to an S3-compatible bucket (R2 / B2 / S3). Needs rclone configured as "bucket".
set -euo pipefail
cd "$(dirname "$0")/.."
STAMP=$(date -u +%Y%m%d)
mkdir -p /tmp/uniaiverse-backup && sqlite3 outputs/uniaiverse.db ".backup /tmp/uniaiverse-backup/uniaiverse-$STAMP.db" 2>/dev/null || cp outputs/uniaiverse.db /tmp/uniaiverse-backup/uniaiverse-$STAMP.db
tar -czf /tmp/uniaiverse-backup/outputs-$STAMP.tgz outputs --exclude=uniaiverse.db
rclone copy /tmp/uniaiverse-backup bucket:uniaiverse-backups/ && rclone delete --min-age 30d bucket:uniaiverse-backups/
rm -rf /tmp/uniaiverse-backup && echo "backup $STAMP done"
