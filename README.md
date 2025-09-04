# EML Analyzer App

Cette application est conçue pour analyser des fichiers `.eml` en utilisant une interface web propre, déployée dans un conteneur Docker. Elle permet de télécharger un ou plusieurs fichiers `.eml`, de les analyser automatiquement avec `eml-analyzer`, puis d'afficher les résultats d'analyse.

## Fonctionnalités

- **Upload multiple de fichiers .eml** : Téléchargez plusieurs fichiers en une seule fois.
- **Analyse automatique** : Chaque fichier `.eml` est analysé grâce au module `eml-analyzer`.
- **Affichage des résultats** : Visualisez les résultats d'analyse directement dans l'interface.

## Prérequis

- **Docker** : Assurez-vous que Docker est installé et opérationnel sur votre machine.
- **Python (facultatif)** : Si vous souhaitez exécuter le code localement sans Docker, Python 3.8 ou plus est requis.
- **requirements.txt** : ```eml-analyzer
Flask~=3.1.0
mail-parser
Werkzeug>=3.1
pyyaml~=6.0.2
MarkupSafe~=3.0.2```

## Installation et Exécution

### Étapes pour utiliser Docker

1. **Clonez le projet :**
   
   ```bash
   git clone https://github.com/hackutt-ctf/emails-analyser.git
   cd eml-analyzer-app

2.	**Construisez et exécutez l’image Docker :**

Cette commande démarre un conteneur basé sur l’image créée et mappe le port 5000 du conteneur au port 5000 de votre machine locale.
   
   ```./dockermake```
3.	**Accédez à l’application :**

Ouvrez votre navigateur et allez sur http://localhost:5000 pour utiliser l’interface d’upload et analyser vos fichiers .eml

Structure du Projet

	•	app.py: Code principal de l’application Flask pour gérer l’upload et l’analyse des fichiers .eml.
	•	Dockerfile: Fichier de configuration pour construire l’image Docker.
	•	requirements.txt: Liste des dépendances Python (Flask, eml-analyzer).
	•	templates/: Contient les fichiers HTML pour l’interface utilisateur.
	•	upload.html: Interface d’upload des fichiers .eml.
	•	result.html: Affichage les résultats d’analyse généraux.
	•	analysis.html: Affichage les résultats d’analyse détaillés d'un fichier .eml.
	•	static/style.css: Fichier CSS pour le style de l’application.

Exemples d’Utilisation

	1.	Téléchargez un ou plusieurs fichiers .eml via le bouton d’upload.
 <img width="1016" height="395" alt="projets_emailanalyzer" src="https://github.com/user-attachments/assets/eef59d0a-1720-475b-83de-6d41c8c7788a" />

	2.	Lancez l’analyse en soumettant les fichiers.
	3.	Consultez les résultats pour chaque fichier .eml directement sur la page de résultats.
<img width="1016" height="928" alt="Screenshot 2025-09-04 at 18 36 29" src="https://github.com/user-attachments/assets/8b372656-8469-4268-bab3-0f5086f3afb8" />
<img width="1312" height="853" alt="Screenshot 2025-09-04 at 18 36 41" src="https://github.com/user-attachments/assets/a4684dc4-851c-480c-9fd2-50f424e66aec" />



