#!/bin/bash
set -e

# If no arguments passed, drop into bash
if [ "$#" -eq 0 ]; then
  exec /bin/bash
fi

exec "$@"
