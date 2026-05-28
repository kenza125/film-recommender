# CineAI — Système de recommandation de films basé sur LLM

Projet individuel — IA Générative  
Étudiante : [Ton Prénom Nom]  
École : ENSTAB  
Date limite : 31 mai 2026

## Description

CineAI est un système de recommandation de films intelligent qui utilise un LLM (Llama 3 via Groq API) pour générer des recommandations personnalisées basées sur les préférences, l'humeur et l'historique de l'utilisateur.

## Fonctionnalités

- Sélection des genres préférés (multiselect)
- Prise en compte des films déjà vus
- Adaptation à l'humeur du moment
- Système de likes pour affiner les recommandations en session
- Interface web interactive avec Streamlit
- Recommandations expliquées par le LLM

## Modèle génératif utilisé

**Llama 3 (llama3-8b-8192)** via l'API Groq — modèle de langage génératif utilisé pour le prompt engineering et la génération de recommandations personnalisées.

## Installation

```bash
git clone https://github.com/TON_USERNAME/film-recommender
cd film-recommender
pip install -r requirements.txt
```

Crée un fichier `.env` à la racine :
```
GROQ_API_KEY=ta_cle_api_groq
```

## Lancement

```bash
streamlit run app.py
```

## Stack technique

- Python 3.10+
- Streamlit (interface web)
- Groq API + Llama 3 (LLM)
- python-dotenv

## Captures d'écran

*(ajoute tes screenshots ici après avoir lancé l'app)*

## Démo vidéo

*(ajoute le lien vers ta vidéo de démonstration ici)*
