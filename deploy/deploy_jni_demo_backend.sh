#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/tsi/dl/jni-inscriptions-demo"
BRANCH="${1:-codexdeploy}"

cd "$APP_DIR/django_inscriptions"
pwd
git fetch origin --prune

if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  git checkout -B "$BRANCH" "origin/$BRANCH"
  git pull origin "$BRANCH"
else
  DEFAULT_BRANCH="$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's|^origin/||')"
  echo "Branch '$BRANCH' not found in django_inscriptions remote. Falling back to '$DEFAULT_BRANCH'."
  git checkout -B "$DEFAULT_BRANCH" "origin/$DEFAULT_BRANCH"
  git pull origin "$DEFAULT_BRANCH"
fi

cd "$APP_DIR"
docker compose --env-file .env.demo -f docker-compose.demo.yml -p jni_demo up -d --build backend
docker compose --env-file .env.demo -f docker-compose.demo.yml -p jni_demo exec -T backend python manage.py migrate --noinput
docker compose --env-file .env.demo -f docker-compose.demo.yml -p jni_demo exec -T backend python manage.py collectstatic --noinput
docker compose --env-file .env.demo -f docker-compose.demo.yml -p jni_demo ps
docker logs jni_demo_backend --tail 80
