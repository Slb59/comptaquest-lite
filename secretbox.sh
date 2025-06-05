#!/bin/bash

MAIN_DIR="/home/sylvie/Documents/01_Documents Slb/01-Journaling/SecretBox"
LOG_FILE="/home/sylvie/Documents/01_Documents Slb/01-Journaling/SecretBox/secretbox.log"

# Rediriger la sortie vers un fichier log
exec > >(tee -a "$LOG_FILE") 2>&1

# Notification pour indiquer que le terminal est sur le point d'être lancé
notify-send "Lancement du serveur Django" "Ouverture du terminal pour le serveur Django..."

# Commande pour lancer le serveur Django
konsole -e "bash -c sbrunserver.sh" | tee -a "$LOG_FILE"

# Notification pour indiquer que le terminal est sur le point d'être lancé
notify-send "Lancement du serveur Frontend" "Ouverture du terminal pour le serveur Frontend..."

# Commande pour construire avec npm
konsole -e "bash -c 'cd "$MAIN_DIR" &&source .venv/bin/activate && npm run build; exec bash'" | tee -a "$LOG_FILE"

# Attendre un peu pour s'assurer que le serveur a démarré
sleep 10

# Vérifier si le serveur répond
response=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/)

if [ "$response" -eq 200 ]; then
    notify-send "Le serveur Django est en cours d'exécution."
    # Ouvrir Firefox avec l'URL localhost
    firefox http://127.0.0.1:8000/
else
    notify-send "Le serveur Django ne répond pas correctement."
    firefox "$LOG_FILE"
fi


