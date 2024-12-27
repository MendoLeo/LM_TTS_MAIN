import os
import sys
import argparse
from glob import glob
from TTS import TTS

def process_audio(src_path, target_audio):
    # Obtenir la liste des fichiers source audio
    raw_src_audios = sorted(glob(src_path))  

    for src_audio in raw_src_audios:
        # Extraire le livre et le fichier audio
        book = src_audio.split('/')[-2]
        h_audio = src_audio.split('/')[-1]

        # Construire le chemin de sortie
        out_audios = f"/wavs_16/{book}/{h_audio}"
        
        # Créer les répertoires de sortie si nécessaire
        os.makedirs(os.path.dirname(out_audios), exist_ok=True)

        # Initialiser le modèle TTS
        tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=False).to("cuda")
        
        # Convertir le fichier audio
        tts.voice_conversion_to_file(source_wav=src_audio, target_wav=target_audio, file_path=out_audios)

if __name__ == "__main__":
    # Initialisation du parser d'arguments
    parser = argparse.ArgumentParser(description="Audio processing script")
    parser.add_argument('src_path', type=str, help='Le chemin des fichiers audio source')
    parser.add_argument('target_audio', type=str, help='Le chemin de l\'audio cible')

    # Récupération des arguments
    args = parser.parse_args()

    # Lancer le processus avec les chemins fournis
    process_audio(args.src_path, args.target_audio)
