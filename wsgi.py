import sys
import os

# Spécifiez le chemin de votre projet Flask
path = '/home/mamebousso24/projet/Flask'
if path not in sys.path:
    sys.path.append(path)

# Définir la variable d'environnement pour Flask
os.environ['FLASK_ENV'] = 'production'

# Importer l'application Flask
from app import create_app  # Assurez-vous que cela correspond à votre structure

application = create_app()  # Créez l'instance de votre application Flask
