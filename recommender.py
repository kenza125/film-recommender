import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_recommendations(genres: list, films_vus: str, humeur: str, likes: list = []) -> list:
    """
    Génère 5 recommandations de films personnalisées via le LLM.
    Retourne une liste de dicts : titre, annee, genre, synopsis, raison.
    """

    likes_section = ""
    if likes:
        likes_section = f"\nFilms que l'utilisateur a aimés lors de cette session : {', '.join(likes)}."

    prompt = f"""Tu es un expert en cinéma et système de recommandation de films.

Profil de l'utilisateur :
- Genres préférés : {', '.join(genres)}
- Films déjà vus (à ne pas recommander) : {films_vus if films_vus else 'aucun mentionné'}
- Humeur actuelle : {humeur}{likes_section}

Recommande exactement 5 films parfaitement adaptés à ce profil.
Pour chaque film, fournis une explication personnalisée qui montre pourquoi ce film correspond précisément à cet utilisateur.

Réponds UNIQUEMENT avec un tableau JSON valide, sans texte avant ni après, au format suivant :
[
  {{
    "titre": "Nom du film",
    "annee": 2019,
    "genre": "Thriller / Science-fiction",
    "synopsis": "Résumé en 1 phrase.",
    "raison": "Explication personnalisée de pourquoi ce film correspond au profil (2 phrases)."
  }}
]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()

    # Nettoyage si le modèle ajoute des balises markdown
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    films = json.loads(raw)
    return films
