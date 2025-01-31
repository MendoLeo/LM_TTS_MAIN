import os
import argparse

# Fonction pour formatter le dataset
def formatter(metadata_file, audio_dir):
    dataset = []

    with open(metadata_file, 'r', encoding='utf-8') as file:
        next(file)  # Passer l'en-tête
        for line in file:
            # Séparer le chemin du fichier audio et la transcription
            audio_filename, transcript = line.strip().split('|')
            
            # Créer le chemin complet du fichier audio
            audio_path = os.path.join(audio_dir, audio_filename)
            
            # Ajouter à la liste sous forme de dictionnaire
            dataset.append({"audio_path": audio_path, "text": transcript})
    
    return dataset

# Fonction principale pour gérer les arguments et exécuter le formatage
"""if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Formatter le dataset à partir du fichier metadata.csv")
    parser.add_argument('--metadata_file', type=str, required=True, help="Chemin vers le fichier metadata.csv")
    parser.add_argument('--audio_dir', type=str, required=True, help="Répertoire contenant les fichiers audio")
    
    args = parser.parse_args()
    
    # Formatter le dataset
    formatted_dataset = formatter(args.metadata_file, args.audio_dir)"""
    
   