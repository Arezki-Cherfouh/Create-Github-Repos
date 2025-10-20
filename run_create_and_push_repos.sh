#!/bin/bash
cd "$(dirname "$0")"
echo "Running run_create_and_push_repos..."
wine "run_create_and_push_repos" || ./"run_create_and_push_repos" "$@"
