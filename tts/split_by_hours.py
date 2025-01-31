import os
import argparse
import librosa
import pandas as pd
from tqdm import tqdm

def get_audio_duration(audio_path):
    """Retourne la durée d'un fichier audio en secondes uniquement si c'est un fichier .wav"""
    if not audio_path.lower().endswith(".wav"):
        return 0  # Ignorer les fichiers non-WAV

    try:
        duration = librosa.get_duration(path=audio_path)
        return duration
    except Exception as e:
        print(f"❌ Erreur avec {audio_path}: {e}")
        return 0

def split_dataset_by_duration(metadata_file, audio_dir, output_dir, test_hours=2, dev_hours=2):
    # Charger le dataset
    df = pd.read_csv(metadata_file, sep="|", header=None, names=["audio_filename", "text"])

    # Filtrer uniquement les fichiers audio .wav
    df = df[df["audio_filename"].str.endswith(".wav", na=False)]

    # Ajouter les chemins complets des fichiers audio
    df["audio_path"] = df["audio_filename"].apply(lambda x: os.path.join(audio_dir, x))

    # Calculer la durée des fichiers audio
    tqdm.pandas(desc="⏳ Calcul des durées audio")
    df["duration"] = df["audio_path"].progress_apply(get_audio_duration)

    # Filtrer les fichiers avec une durée valide (> 0s)
    df = df[df["duration"] > 0]

    # Trier les fichiers par durée décroissante
    df = df.sort_values(by="duration", ascending=False).reset_index(drop=True)

    # Initialisation des sets
    test_set, dev_set, train_set = [], [], []
    test_total, dev_total, train_total = 0, 0, 0

    # Répartition des données en fonction des heures souhaitées
    for _, row in df.iterrows():
        if test_total < test_hours * 3600:
            test_set.append(row)
            test_total += row["duration"]
        elif dev_total < dev_hours * 3600:
            dev_set.append(row)
            dev_total += row["duration"]
        else:
            train_set.append(row)
            train_total += row["duration"]

    # Convertir en DataFrame
    test_df = pd.DataFrame(test_set)
    dev_df = pd.DataFrame(dev_set)
    train_df = pd.DataFrame(train_set)

    # Création du dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    # Sauvegarde des fichiers
    train_df[["audio_filename", "text"]].to_csv(os.path.join(output_dir, "train.csv"), sep="|", index=False, header=False)
    dev_df[["audio_filename", "text"]].to_csv(os.path.join(output_dir, "dev.csv"), sep="|", index=False, header=False)
    test_df[["audio_filename", "text"]].to_csv(os.path.join(output_dir, "test.csv"), sep="|", index=False, header=False)

    # Afficher le résumé
    print(f"\n✅ Répartition terminée :")
    print(f"- Train : {len(train_df)} fichiers ({train_total/3600:.2f}h)")
    print(f"- Dev   : {len(dev_df)} fichiers ({dev_total/3600:.2f}h)")
    print(f"- Test  : {len(test_df)} fichiers ({test_total/3600:.2f}h)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diviser un dataset TTS en train, test et dev selon la durée totale des fichiers audio (WAV uniquement)")
    parser.add_argument('--metadata_file', type=str, required=True, help="Chemin vers le fichier metadata.csv")
    parser.add_argument('--audio_dir', type=str, required=True, help="Répertoire contenant les fichiers audio")
    parser.add_argument('--output_dir', type=str, required=True, help="Répertoire de sortie des fichiers divisés")
    parser.add_argument('--test_hours', type=float, default=2, help="Nombre d'heures pour le test (default: 2h)")
    parser.add_argument('--dev_hours', type=float, default=2, help="Nombre d'heures pour le dev (default: 2h)")

    args = parser.parse_args()
    
    split_dataset_by_duration(args.metadata_file, args.audio_dir, args.output_dir, args.test_hours, args.dev_hours)
