# 1. Image Python adaptée et légère
FROM python:3.10-slim

# 2. Dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le reste du code source (dont app.py et items.db)
COPY . .

# 5. Exposer le port interne de Flask
EXPOSE 5000

# 6. Commande de démarrage
CMD ["python", "app.py"]