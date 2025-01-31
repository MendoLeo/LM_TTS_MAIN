import os
import csv
import argparse
from tqdm import tqdm

def generate_metadata(input_dir, output_dir):
    # Vérifier si le répertoire de sortie existe, sinon créer
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "metadata.csv")
    
    # Initialisation du fichier CSV avec l'en-tête
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(["audio_filename", "transcription"])
        
        # Récupérer tous les fichiers .txt dans le répertoire d'entrée
        txt_files = [os.path.join(root, file) 
                     for root, _, files in os.walk(input_dir) 
                     for file in files if file.endswith(".txt")]
        
        # Calcul du nombre total de fichiers pour la progression
        total_txt_files = len(txt_files)
        
        # Progression avec tqdm
        for i, txt_file in tqdm(enumerate(txt_files), total=total_txt_files, desc="Processing files"):
            # Trouver le fichier audio correspondant
            wav_file = txt_file.replace('.txt', '.wav')
            
            if os.path.isfile(wav_file):
                # Lire la transcription depuis le fichier .txt
                with open(txt_file, 'r', encoding='utf-8') as text_file:
                    transcription = text_file.read().strip()
                    
                # Écrire dans le fichier CSV
                writer.writerow([wav_file, transcription])

    print(f"Metadata file created at {output_file}")

# Gestion des arguments en ligne de commande
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate metadata.csv for TTS dataset.")
    parser.add_argument('--input_dir', type=str, required=True, help="Path to the input directory containing .txt files.")
    parser.add_argument('--output_dir', type=str, required=True, help="Path to the output directory where metadata.csv will be saved.")
    
    args = parser.parse_args()
    
    generate_metadata(args.input_dir, args.output_dir)
