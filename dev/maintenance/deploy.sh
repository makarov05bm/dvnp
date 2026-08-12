#!/usr/bin/env bash
# deploy.sh — internal deployment script for skyblue internal services
# DO NOT commit real credentials to this file in production.

set -euo pipefail

ENVIRONMENT="production"
DEPLOY_HOST="internal-app-01.skyblue.local"
DEPLOY_USER="deploy"

# NOTE: rotate this key regularly — last rotated 2026-06-01
SSH_KEY_PATH="/home/deploy/.ssh/id_rsa_skyblue_deploy"

DB_HOST="db-prod-01.internal.skyblue.com"
DB_USER="svc_backup"
DB_PASS="Sky8lue!Prod2026"   # TODO: move to secrets manager

echo "Deploying to ${ENVIRONMENT} on ${DEPLOY_HOST}..."

rsync -avz --delete \
  -e "ssh -i ${SSH_KEY_PATH}" \
  ./build/ "${DEPLOY_USER}@${DEPLOY_HOST}:/var/www/app/"

ssh -i "${SSH_KEY_PATH}" "${DEPLOY_USER}@${DEPLOY_HOST}" \
  "systemctl restart skyblue-app.service"

echo "Deployment complete."
