import pandas as pd
import requests
import zipfile
import os

MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
DATA_DIR = "data"
MOVIES_PATH = os.path.join(DATA_DIR, "movies.csv")
RATINGS_PATH = os.path.join(DATA_DIR, "ratings.csv")

def download_movielens():
    """Télécharge et extrait le dataset MovieLens si pas encore présent."""
    if os.path.exists(MOVIES_PATH) and os.path.exists(RATINGS_PATH):
        return  # déjà téléchargé

    os.makedirs(DATA_DIR, exist_ok=True)
    print("Téléchargement du dataset MovieLens...")

    response = requests.get(MOVIELENS_URL, stream=True)
    zip_path = os.path.join(DATA_DIR, "movielens.zip")

    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if name.endswith("movies.csv"):
                with z.open(name) as src, open(MOVIES_PATH, "wb") as dst:
                    dst.write(src.read())
            elif name.endswith("ratings.csv"):
                with z.open(name) as src, open(RATINGS_PATH, "wb") as dst:
                    dst.write(src.read())

    os.remove(zip_path)
    print("Dataset MovieLens prêt !")


def load_movies() -> pd.DataFrame:
    """Charge et nettoie le dataframe des films avec leur note moyenne."""
    download_movielens()

    movies = pd.read_csv(MOVIES_PATH)
    ratings = pd.read_csv(RATINGS_PATH)

    # Note moyenne et nombre de votes par film
    stats = ratings.groupby("movieId").agg(
        note_moyenne=("rating", "mean"),
        nb_votes=("rating", "count")
    ).reset_index()

    movies = movies.merge(stats, on="movieId", how="left")

    # Extraire l'année du titre  ex: "Toy Story (1995)" → 1995
    movies["annee"] = movies["title"].str.extract(r'\((\d{4})\)').astype("Int64")
    movies["titre_propre"] = movies["title"].str.replace(r'\s*\(\d{4}\)', '', regex=True).str.strip()

    # Garder seulement les films avec assez de votes
    movies = movies[movies["nb_votes"] >= 10].copy()
    movies["note_moyenne"] = movies["note_moyenne"].round(2)

    return movies


def filtrer_par_genres(movies: pd.DataFrame, genres: list, n: int = 20) -> pd.DataFrame:
    """Retourne les n meilleurs films correspondant aux genres demandés."""
    masque = movies["genres"].apply(
        lambda g: any(genre.lower() in g.lower() for genre in genres)
    )
    filtres = movies[masque].copy()
    filtres = filtres.sort_values("note_moyenne", ascending=False)
    return filtres.head(n)
