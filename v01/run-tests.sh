#!/bin/bash

# Load environment variables using direnv
#set -a
#source $(direnv export bash)
#set +a

# Create the output directory if it doesn't exist
mkdir -p output

# Run the parser
python3 parser.py ../examples
