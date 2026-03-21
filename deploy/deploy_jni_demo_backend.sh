#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/tsi/dl/jni-inscriptions-demo"
BRANCH="${1:-codexdeploy}"

cd "$APP_DIR"

git fetch origin
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git checkout "$BRANCH"
else
  git checkout -b "$BRANCH" "origin/$BRANCH"
fi

git pull origin "$BRANCH"
git submodule sync --recursive
git submodule update --init --recursive

cd django_inscriptions
git fetch origin "$BRANCH"
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git checkout "$BRANCH"
else
  git checkout -b "$BRANCH" "origin/$BRANCH"
fi
git pull origin "$BRANCH"
cd ..

if [[ ! -f .env.demo ]]; then
  cp .env.demo.example .env.demo
fi

if [[ ! -f django_inscriptions/.env.docker.demo ]]; then
  cp django_inscriptions/.env.docker.demo.example django_inscriptions/.env.docker.demo
fi

if [[ ! -f django_inscriptions/.env.docker ]]; then
  cp django_inscriptions/.env.docker.demo django_inscriptions/.env.docker
fi

docker compose --env-file .env.demo -f docker-compose.yml -f docker-compose.demo.yml -p jni_demo up -d --build backend
docker compose --env-file .env.demo -f docker-compose.yml -f docker-compose.demo.yml -p jni_demo ps
docker logs jni_demo_backend --tail 80
