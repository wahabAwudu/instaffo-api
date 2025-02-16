#!/bin/bash

set -e

# run other scrips here before server starts

echo "Run Server! 🚀"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
