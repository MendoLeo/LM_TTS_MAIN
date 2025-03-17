import argparse
from pathlib import Path
from tqdm import tqdm
from tc_utils import (load_transcripts)
from text_normalization import text_normalize

def process_files(clean_path:Path, json_path:Path, lang_code:str):
    txt_paths = sorted(clean_path.rglob("*.txt"))

    for txt_path in tqdm(txt_paths, desc="Processing"):
        verset_c = txt_path.stem

        # Chargement du transcript depuis le JSON
        try:
            _, transcript_o = load_transcripts(json_path, verset_c)
        except Exception as e:
            print(f"Error loading transcript for {verset_c}: {e}")
            continue

        # Normalisation et écriture du fichier
        try:
            transcript_norm = text_normalize(transcript_o[0], lang_code,remove_numbers=False)

            # Écriture dans le fichier (remplacement de l'ancien contenu)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(transcript_norm)

        except Exception as e:
            print(f"Problème de remplacement et/ou de normalisation pour {verset_c}: {e}")
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and normalize transcripts.")
    parser.add_argument('--texts_dir', type=str, required=True, help='Path to the directory containing text files.')
    parser.add_argument('--json_file', type=str, required=True, help='Path to the JSON file containing original transcripts.')
    parser.add_argument('--lang', type=str, default='fr', help='Language code for normalization (default: eo).')

    args = parser.parse_args()

    # Convertir les chemins en objets Path
    clean_path = Path(args.texts_dir)
    json_path = Path(args.json_file)

    # Exécuter la fonction principale
    process_files(clean_path, json_path, args.lang)
