
import os
from glob import glob
import torchaudio
import torch
from denoiser import pretrained  # Import du modèle pré-entraîné
from denoiser.dsp import convert_audio
from torchaudio.transforms import Resample  # Pour convertir les taux d'échantillonnage

def denoiser(src_path, output_dir):
    """Appliquer la réduction du bruit aux fichiers audio."""
    # Charger le modèle DNS
    model =  pretrained.dns64().cuda()
    
    # Obtenir les fichiers audio
    raw_src_audios = sorted(glob(src_path))

    for src_audio in raw_src_audios:
        # Extraire les informations du chemin
        book = src_audio.split('/')[-2]
        h_audio = src_audio.split('/')[-1]

        # Construire le chemin de sortie
        out_audio_path = os.path.join(output_dir, book, h_audio)
        
        # Créer le répertoire de sortie si nécessaire
        os.makedirs(os.path.dirname(out_audio_path), exist_ok=True)

        # Charger et convertir l'audio
        wav, sr = torchaudio.load(src_audio)
        wav = convert_audio(wav.cuda(), sr, model.sample_rate, model.chin)

        # Appliquer la réduction du bruit
        with torch.no_grad():
            denoised = model(wav[None])[0]

        # Sauvegarder l'audio débruité
        torchaudio.save(out_audio_path, denoised.cpu(), model.sample_rate)
        print(f"Processed and saved: {out_audio_path}")

if __name__ == "__main__":
    import argparse

    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="Denoise audio files in a directory")
    parser.add_argument('src_path', type=str, help='Chemin des fichiers audio source')
    parser.add_argument('output_dir', type=str, help='Répertoire pour enregistrer les fichiers débruités')

    # Récupération des arguments
    args = parser.parse_args()

    # Lancer le processus de réduction du bruit
    denoiser(args.src_path, args.output_dir)
