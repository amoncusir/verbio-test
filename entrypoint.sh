#!/bin/sh

# Enable verbose execution
set -x

run_api() {
  echo "Starting GAPI with arguments: $*"
  exec gunicorn -k uvicorn_worker.UvicornWorker --preload -t 0 "$@" 'src.app.instances.api:api'
}

# Check if at least one argument is provided
if [ -z "$1" ]; then
  echo "You must provide the <mode> argument"
  exit 1
fi

# Capture the first argument as the mode to run
mode=$1
shift # Remove the first argument to pass the remaining arguments

# Execute the corresponding function based on the first argument
case "$mode" in
  api)
    run_api "$@"
    ;;
  *)
    echo "Invalid option."
    exit 1
    ;;
esac
