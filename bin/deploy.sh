#!/usr/bin/env sh

set -e
set -v

DOCKER_CERT_PATH=/root/.docker
DOCKER_COMPOSE_PROJECT_NAME=vsong_bot

mkdir -p $DOCKER_CERT_PATH


echo "$PROD_CA_PEM" | tr -d '\r' > $DOCKER_CERT_PATH/ca.pem
echo "$PROD_CERT_PEM" | tr -d '\r' > $DOCKER_CERT_PATH/cert.pem
echo "$PROD_KEY_PEM" | tr -d '\r' > $DOCKER_CERT_PATH/key.pem

echo "$PROD_ENV_FILE" | tr -d '\r' > ./.env

export DOCKER_TLS_VERIFY=1
export DOCKER_HOST=tcp://$PROD_STAGING_HOST:2376

docker login -u gitlab-ci-token -p ${CI_JOB_TOKEN} registry.gitlab.com

python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"

docker-compose \
    -f docker-compose.yml \
    --project-name $DOCKER_COMPOSE_PROJECT_NAME \
    pull

docker-compose \
    -f docker-compose.yml \
    --project-name $DOCKER_COMPOSE_PROJECT_NAME \
    up -d
