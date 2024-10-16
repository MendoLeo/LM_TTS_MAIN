import pandas as pd
import os
from glob import glob
from tqdm import tqdm


# Liste des langues
lang = ['Bulu', 'Bafia', 'MKPAMAN_AMVOE_Ewondo']
# Dossier contenant tous les fichiers CSV des livres de la Bible
path_all_chapters = '/home/mendo/Downloads/LM/LM_news/TTS_data/bible_text_CSV'  # Remplacez par le chemin correct

# Utiliser glob pour sélectionner tous les fichiers CSV dans le répertoire
book_files = glob(os.path.join(path_all_chapters, '*.csv'))

# Ajouter une barre de progression pour les fichiers de livres
for book_path in tqdm(book_files, desc="Traitement des livres"):
    # Obtenir le nom du fichier sans le chemin et l'extension
    book_name = os.path.splitext(os.path.basename(book_path))[0]
    
    # Lire le fichier CSV du livre
    df_book = pd.read_csv(book_path)
    
    # Ajouter une barre de progression pour chaque langue
    for ln in tqdm(lang, desc=f"Extraction des langues pour {book_name}", leave=False):
        if ln in df_book.columns:  # Vérifier si la colonne existe
            # Définir le répertoire de sortie pour la langue, à l'intérieur du dossier de base
            output_lang_path = os.path.join(path_all_chapters, ln)
            # Créer le répertoire s'il n'existe pas encore
            os.makedirs(output_lang_path, exist_ok=True)
            
            # Extraire la colonne de langue avec les index
            subset = df_book[['livre.chapitre.verset',ln]].copy()
            # Définir le nom de fichier de sortie en utilisant le nom du livre et la langue
            output_file_name = f"{book_name}.csv"
            output_path = os.path.join(output_lang_path, output_file_name)
            # Sauvegarder le sous-ensemble dans un fichier CSV
            subset.to_csv(output_path, index=False)
