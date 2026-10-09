#!/bin/sh
set -eu

project_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
backup_dir="$project_dir/backups"
timestamp="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$backup_dir"
cd "$project_dir"

docker compose --env-file .env.production -f docker-compose.prod.yml exec -T db \
  pg_dump -U "$(sed -n 's/^POSTGRES_USER=//p' .env.production)" \
  "$(sed -n 's/^POSTGRES_DB=//p' .env.production)" | gzip > "$backup_dir/database_$timestamp.sql.gz"

docker run --rm -v pure-line_media_data:/source:ro -v "$backup_dir:/backup" alpine \
  tar -czf "/backup/media_$timestamp.tar.gz" -C /source .

find "$backup_dir" -type f -mtime +14 -delete
echo "Backup completed: $timestamp"
