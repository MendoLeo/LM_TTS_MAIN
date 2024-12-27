#!/bin/bash

# Vérifier si le nombre d'arguments est correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_path> <target_audio>"
    exit 1
fi

# Passer les arguments au script Python
python3 process_audio.py "$1" "$2"
