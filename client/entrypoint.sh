#!/bin/sh

if ! isTrue "$DEBUG"; then
  exec npm run serve
else
  exec "$@"
fi