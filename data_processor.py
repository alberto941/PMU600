import re

def parse_pmu_data(raw_text):
    """
    Convertit les données brutes copiées en un tableau structuré.
    Corrige les erreurs de format pour éviter les décalages dans le tableau.
    """
    if not raw_text.strip():
        return []

    # Nettoyer les lignes vides et enlever les espaces inutiles
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    data = []
    i = 0

    while i < len(lines):
        try:
            # Vérification : Assurons-nous d'avoir exactement 7 lignes pour un cheval
            if i + 6 >= len(lines):
                print(f"⚠ Données incomplètes détectées, arrêt au cheval {i // 7 + 1}.")
                break

            # Vérifier si la ligne actuelle est bien un numéro
            if not lines[i].isdigit():
                print(f"⚠ Ligne ignorée (pas un numéro de cheval) : {lines[i]}")
                i += 1
                continue

            # Extraction des informations
            numero = lines[i].strip()
            nom_cheval = lines[i + 1].strip()
            jockey_entraineur = lines[i + 2].strip()
            sexe_age_distance = lines[i + 3].strip()
            chrono = lines[i + 4].strip()
            gains = lines[i + 5].strip()
            performances = lines[i + 6].strip()

            # Vérifier et extraire Sexe / Âge / Distance correctement
            sexe, age, distance = ("", "", "")
            if " - " in sexe_age_distance:
                parts = sexe_age_distance.split(" - ")
                if len(parts) == 2:
                    sexe = parts[0].strip()
                    age_distance = parts[1].strip()
                    age_parts = age_distance.split(" ")
                    if len(age_parts) >= 2:
                        age = age_parts[0].strip()
                        distance = age_parts[1].strip()
                    else:
                        distance = age_distance.strip()

            # Vérification finale et correction si nécessaire
            if not distance.endswith("m"):
                distance = "Inconnu"  # Sécurise la distance si le format est mal écrit

            # Ajoute la ligne complète au tableau
            data.append([
                numero, nom_cheval, jockey_entraineur, sexe, age, distance,
                chrono, gains, performances
            ])

            i += 7  # Passer au cheval suivant

        except Exception as e:
            print(f"⚠ Erreur de format à la ligne {i}, certaines informations sont manquantes : {e}")
            break

    return data

def extract_selection_data(text):
    data = {"Bases": [], "Outsiders": [], "Belles chances": [], "Délaissés": []}

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("Bases :"):
            data["Bases"] = [num.strip() for num in line.replace("Bases :", "").split("-") if num.strip().isdigit()]
        elif line.startswith("Outsiders :"):
            data["Outsiders"] = [num.strip() for num in line.replace("Outsiders :", "").split("-") if num.strip().isdigit()]
        elif line.startswith("Belles chances :"):
            data["Belles chances"] = [num.strip() for num in line.replace("Belles chances :", "").split("-") if num.strip().isdigit()]
        elif line.startswith("Délaissés :"):  # Correction ici
            data["Délaissés"] = [num.strip() for num in line.replace("Délaissés :", "").split("-") if num.strip().isdigit()]

    print("📌 Délaissés extraits après correction :", data["Délaissés"])  # Debugging
    return data


def extract_zeturf_data(raw_text):
    """
    Extrait une liste de numéros depuis une entrée au format : 16 - 11 - 7 - 12 - 9 - 10 - 8 - 5
    """
    return [num.strip() for num in raw_text.split("-") if num.strip().isdigit()]