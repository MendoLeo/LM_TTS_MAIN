#!/bin/bash

# Vérifier qu'un argument a été passé
if [ -z "$1" ]; then
    echo "Utilisation : $0 <chemin_du_repertoire>"
    exit 1
fi

# Récupérer le chemin du répertoire
directory="$1"

# Vérifier que le répertoire existe
if [ ! -d "$directory" ]; then
    echo "Erreur : Le répertoire '$directory' n'existe pas."
    exit 1
fi

# Lancer le script Python pour traiter le répertoire
echo "Traitement du répertoire : $directory"
python3 csv_to_json.py "$directory"
