import re 
import os
import tempfile
from pathlib import Path
import json
from typing import List, Tuple
import uroman as ur
from tqdm import tqdm


# iso codes with specialized rules in uroman
special_isos_uroman = "ara, bel, bul, deu, ell, eng, fas, grc, ell, eng, heb, kaz, kir, lav, lit, mkd, mkd2, oss, pnt, pus, rus, srp, srp2, tur, uig, ukr, yid".split(",")
special_isos_uroman = [i.strip() for i in special_isos_uroman]

def normalize_uroman(text)-> list[str]:
    """
    normalize_uroman _summary_

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """

    text = text.lower()
    text = re.sub("([^a-z' ])", " ", text)
    text = re.sub(' +', ' ', text)
    return text.strip()

def get_uroman_tokens(norm_transcripts, iso=None):
    # load uroman data (once at the beginning)
    uroman = ur.Uroman()
    uromans = []
    
    # Création des fichiers temporaires
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as input_file, \
         tempfile.NamedTemporaryFile(mode='w+', delete=False) as output_file:

        try:
            # Écriture des textes normalisés dans le fichier temporaire d'entrée
            for text in norm_transcripts:
                input_file.write(text + "\n")
            input_file.flush()

            # Lecture du fichier et traitement avec la barre de progression
            with open(input_file.name, 'r') as infile:
                for line in tqdm(infile, desc="Romanisation des textes", unit="texte"):
                    text = line.strip()
                    try:
                        # Vérification de la présence du code ISO et romanisation
                        if iso in special_isos_uroman:
                            romanized_text = uroman.romanize_string(text,lcode=iso)
                        else:
                            romanized_text = uroman.romanize_string(text)
                        
                        # Nettoyage des textes romanisés
                        romanized_text = " ".join(romanized_text.strip())
                        romanized_text = re.sub(r"\s+", " ", romanized_text).strip()

                        # Application d'une normalisation supplémentaire
                        normalized_text = normalize_uroman(romanized_text)
                        uromans.append(normalized_text)
                    
                    except Exception as e:
                        print(f"Erreur lors de la romanisation du texte : {text}\nDétail de l'erreur : {e}")

            # Écriture des résultats dans le fichier temporaire de sortie
            with open(output_file.name, 'w') as outfile:
                for uroman_text in uromans:
                    outfile.write(uroman_text + "\n")
        
        except Exception as e:
            print(f"Erreur lors du traitement des fichiers : {e}")
        
        finally:
            # Nettoyage des fichiers temporaires
            os.remove(input_file.name)
            os.remove(output_file.name)

    return uromans
def load_transcripts(json_path: Path, clean_verset: str) -> Tuple[List[str], List[str]]:

    with open(json_path, "r") as f:
        data = json.load(f)
        #print(data)

    # convert MAT.19.1 -> MAT_019_001
    def get_chapter(x):
        return x.split('.')[0] + '_' + x.split('.')[1].zfill(3) + '_'+ x.split('.')[-1].zfill(3)

    transcripts = [d["verset"] for d in data if get_chapter(d["numVerset"]) == clean_verset]
    verse_ids = [d["numVerset"] for d in data if get_chapter(d["numVerset"]) == clean_verset]
    return verse_ids, transcripts
