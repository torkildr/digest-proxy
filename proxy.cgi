#!/usr/bin/env bash

set -e

if [ -z "$DIGEST_USER" ] || [ -z "$DIGEST_PASSWORD" ] || [ -z "$PROXY_HOST" ];
then
  echo -e "Status: 400 Bad Request"
  echo -e "\r"
  echo "Missing \$DIGEST_USER, \$DIGEST_PASSWORD or \$PROXY_HOST"
  exit 1
fi

if [ -z "$REQUEST_URI" ] || [ -z "$REQUEST_METHOD" ];
then
  echo -e "Status: 400 Bad Request"
  echo -e "\r"
  echo "Missing \$REQUEST_URI or \$REQUEST_METHOD"
  exit 1
fi

request_body_arg=""
if [ ! -z "$REQUEST_BODY_FILE" ]; 
then
  request_body_arg="--data-binary @${REQUEST_BODY_FILE}"
fi

curl -sL \
  -D - \
  --digest \
  --user "${DIGEST_USER}:${DIGEST_PASSWORD}" \
  -X "${REQUEST_METHOD}" \
  $request_body_arg \
  "${PROXY_HOST}${REQUEST_URI}" \
  | sed '/^HTTP.* 401 Unauthorized\r$/,/^\r$/d' \
  | sed 's/^HTTP.*\([0-9]\{3\}.*\)/Status: \1/' \

