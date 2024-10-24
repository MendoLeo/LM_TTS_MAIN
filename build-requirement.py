import os
import datetime
import subprocess
from pathlib import Path

# Chemin vers le dossier site-packages (remplacez 'X.X' par votre version de Python)
site_packages_path = Path("env/lib/pythonX.X/site-packages/")  # Adapter selon votre environnement

# Fonction pour lister les packages installés et leur date de modification
def get_installed_packages_with_dates(site_packages_path):
    packages_with_dates = []
    for package in site_packages_path.iterdir():
        if package.is_dir():
            # Récupérer la date de modification du dossier (représentant l'installation ou mise à jour)
            modification_time = datetime.datetime.fromtimestamp(package.stat().st_mtime)
            packages_with_dates.append((package.name, modification_time))
    return packages_with_dates

# Fonction pour trier les packages par date de modification (les plus récents en premier)
def sort_packages_by_date(packages_with_dates):
    return sorted(packages_with_dates, key=lambda x: x[1], reverse=True)

# Fonction pour créer le fichier requirements.txt en fonction des packages installés
def create_requirements_file(sorted_packages):
    # Récupérer les informations des packages installés via 'pip freeze'
    freeze_output = subprocess.check_output(['pip', 'freeze']).decode('utf-8')
    
    # Dictionnaire pour associer chaque package à sa version
    package_versions = {}
    for line in freeze_output.splitlines():
        package, version = line.split('==')
        package_versions[package.lower()] = line  # Sauvegarder la ligne complète avec la version
    
    # Créer et écrire dans le fichier requirements.txt
    with open("requirements.txt", "w") as f:
        for package, mod_time in sorted_packages:
            # Rechercher le package dans les versions obtenues avec 'pip freeze'
            package_lower = package.lower().replace('-', '_')
            if package_lower in package_versions:
                f.write(f"{package_versions[package_lower]}\n")
    
    print("Fichier requirements.txt créé avec succès, packages triés par date d'installation.")

# Exécution du script
if __name__ == "__main__":
    # Récupérer les packages et leurs dates
    packages_with_dates = get_installed_packages_with_dates(site_packages_path)
    
    # Trier les packages par date
    sorted_packages = sort_packages_by_date(packages_with_dates)
    
    # Créer le fichier requirements.txt avec les packages triés
    create_requirements_file(sorted_packages)
