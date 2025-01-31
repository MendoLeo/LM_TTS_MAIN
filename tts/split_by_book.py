import os
import argparse
import pandas as pd
from tqdm import tqdm

def format_and_split(metadata_file, output_dir, test_books, dev_books):
    dataset = []

    # Lecture et formatage des données
    with open(metadata_file, 'r') as file:
        print("📥 Lecture et formatage du dataset...")
        for line in tqdm(file, desc="Formattage des données"):
            audio_filename, transcript = line.strip().split('|')

            # Extraire le nom du livre directement (3e élément avant le fichier dans le chemin)
            book_name = audio_filename.split(os.sep)[-3]

            dataset.append({"audio_path": audio_filename, "text": transcript, "book": book_name})

    # Conversion en DataFrame
    df = pd.DataFrame(dataset)

    # Filtrage par livres
    test_df = df[df["book"].isin(test_books)]
    dev_df = df[df["book"].isin(dev_books)]
    train_df = df[~df["book"].isin(test_books + dev_books)]  # Reste pour train

    # Création du dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    # Sauvegarde des fichiers
    test_df[["audio_path", "text"]].to_csv(os.path.join(output_dir, "test.csv"), sep="|", index=False, header=False)
    dev_df[["audio_path", "text"]].to_csv(os.path.join(output_dir, "dev.csv"), sep="|", index=False, header=False)
    train_df[["audio_path", "text"]].to_csv(os.path.join(output_dir, "train.csv"), sep="|", index=False, header=False)

    # Affichage des statistiques
    print("\n✅ Répartition terminée :")
    print(f"- Train : {len(train_df)} fichiers")
    print(f"- Dev   : {len(dev_df)} fichiers ({', '.join(dev_books)})")
    print(f"- Test  : {len(test_df)} fichiers ({', '.join(test_books)})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Formater et diviser un dataset TTS en train, test et dev selon les livres spécifiés")
    parser.add_argument('--metadata_file', type=str, required=True, help="Chemin vers le fichier metadata.csv")
    parser.add_argument('--output_dir', type=str, required=True, help="Répertoire de sortie des fichiers divisés")
    parser.add_argument('--test_books', nargs='+', required=True, help="Liste des livres pour le test (ex: JHN LUK)")
    parser.add_argument('--dev_books', nargs='+', required=True, help="Liste des livres pour le dev (ex: MRK ACT)")

    args = parser.parse_args()
    
    format_and_split(args.metadata_file, args.output_dir, args.test_books, args.dev_books)
