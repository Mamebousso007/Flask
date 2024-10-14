import os
from app import create_app, db

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Utiliser le port spécifié par Render ou 5000 par défaut
    app.run(host='0.0.0.0', port=port)  # Exécutez l'application sur toutes les interfaces réseau
