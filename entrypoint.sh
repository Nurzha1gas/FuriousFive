#!/bin/bash
echo "Starting Daphne on port $PORT"
daphne broma_config.asgi:application -b 0.0.0.0 -p $PORT
