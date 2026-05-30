import os
import json
from groq import Groq
from dotenv import load_dotenv
from data_loader import load_movies, filtrer_par_genres

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_recommendations(genres: list, films_vus: str, humeur: str, likes: list = []) -> list:
    """
    1. Charge les vrais films MovieLens filtrés par genre
    2. Envoie ces films au LLM pour qu'il choisisse les 5 meilleurs
    3. Retourne la liste avec explications personnalisées
    """

    # --- Étape 1 : charger les vraies données ---
    movies = load_movies()
    candidats = filtrer_par_genres(movies, genres, n=30)

    if candidats.empty:
        candidats = movies.sort_values("note_moyenne", ascending=False).head(30)

    # Construire la liste des films candidats pour le prompt
    films_liste = ""
    for _, row in candidats.iterrows():
        films_liste += (
            f"- {row['titre_propre']} ({int(row['annee']) if row['annee'] else 'N/A'}) "
            f"| Genres: {row['genres']} "
            f"| Note moyenne: {row['note_moyenne']}/5 ({int(row['nb_votes'])} votes)\n"
        )

    likes_section = ""
    if likes:
        likes_section = f"\nFilms que l'utilisateur a aimés : {', '.join(likes)}."

    # --- Étape 2 : prompt avec les vraies données ---
    prompt = f"""Tu es un expert en cinéma et système de recommandation.

Profil utilisateur :
- Genres préférés : {', '.join(genres)}
- Films déjà vus (ne pas recommander) : {films_vus if films_vus else 'aucun'}
- Humeur actuelle : {humeur}{likes_section}

Voici une liste de VRAIS films issus du dataset MovieLens avec leurs notes réelles :
{films_liste}

À partir de cette liste uniquement, choisis les 5 films les plus adaptés au profil.
Ne recommande pas les films déjà vus.
Pour chaque film, explique pourquoi il correspond à ce profil précis.

Réponds UNIQUEMENT en JSON valide, sans texte avant ni après :
[
  {{
    "titre": "titre exact du film",
    "annee": 2000,
    "genre": "genre principal",
    "note": 4.2,
    "synopsis": "résumé en 1 phrase",
    "raison": "pourquoi ce film correspond au profil (2 phrases)"
  }}
]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()

    # Nettoyage balises markdown si présentes
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)
