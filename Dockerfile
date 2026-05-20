# Image Python légère
FROM python:3.10-slim

# Dossier de travail interne au conteneur
WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code
COPY . .

# Ouverture du port Streamlit
EXPOSE 8501

# Lancement de l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]