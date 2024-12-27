#!/bin/bash

# Vérification du nombre d'arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_path> <output_directory>"
    exit 1
fi

# Exécuter le script Python avec les arguments fournis
python3 denoiser.py "$1" "$2"
