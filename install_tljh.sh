#!/bin/bash

# Check if username parameter is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <admin_username>"
    echo "Please provide a admin_username as parameter"
    exit 1
fi

# Store the username parameter
username="$1"

# Execute the bootstrap command with the provided username
cat ./bootstrap.py | sudo -E python3 - --admin "$admin_username"
