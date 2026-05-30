import streamlit as st
from recommender import get_recommendations
from data_loader import load_movies

st.set_page_config(
    page_title="CineQuest — Find the Perfect Movie Every Time",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: #F5F0EB;
    color: #141414;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background-color: #1A1212;
    border-right: 1px solid #2E1F1F;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}
section[data-testid="stSidebar"] * {
    color: #EDE8DF !important;
}
section[data-testid="stSidebar"] h3 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.15rem !important;
    color: #C9973A !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #A08070 !important;
    font-size: 13px !important;
}
section[data-testid="stSidebar"] .stMultiSelect > div,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stSelectSlider {
    background-color: #2E1A1A !important;
    border-color: #5A3030 !important;
    color: #EDE8DF !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] textarea {
    color: #EDE8DF !important;
}
section[data-testid="stSidebar"] textarea::placeholder {
    color: #8A6A5A !important;
}
section[data-testid="stSidebar"] input {
    background-color: #2E1A1A !important;
    color: #EDE8DF !important;
}
section[data-testid="stSidebar"] input::placeholder {
    color: #8A6A5A !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="textarea"] > div {
    background-color: #2E1A1A !important;
    border-color: #5A3030 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] span,
section[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #EDE8DF !important;
}
section[data-testid="stSidebar"] [role="listbox"] {
    background-color: #2E1A1A !important;
}
section[data-testid="stSidebar"] [role="option"] {
    background-color: #2E1A1A !important;
    color: #EDE8DF !important;
}
section[data-testid="stSidebar"] [role="option"]:hover {
    background-color: #4A2020 !important;
}

/* ---- Page headings ---- */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    color: #0E0E0E !important;
    letter-spacing: -1px;
    line-height: 1.1 !important;
}
h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    color: #0E0E0E !important;
    font-size: 1.25rem !important;
}

/* ---- Film card ---- */
.film-card {
    background: #FFFFFF;
    border: 1px solid #DDD5C8;
    border-radius: 12px;
    padding: 1.25rem 1.5rem 1.25rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
}
.film-card::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #8B1A1A 0%, #C9973A 100%);
    border-radius: 0 0 12px 12px;
    opacity: 0;
    transition: opacity 0.2s;
}
.film-card:hover {
    border-color: #8B1A1A;
    box-shadow: 0 8px 30px rgba(139, 26, 26, 0.18);
    transform: translateY(-2px);
}
.film-card:hover::after {
    opacity: 1;
}

.film-number {
    position: absolute;
    top: 14px; right: 16px;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 36px;
    color: #E0D8CE;
    line-height: 1;
    user-select: none;
}

.film-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    margin: 0 0 5px 0;
    color: #0E0E0E;
    line-height: 1.3;
    padding-right: 40px;
}

.film-meta {
    font-size: 11px;
    color: #9A7A60;
    margin: 0 0 12px 0;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.film-synopsis {
    font-size: 13.5px;
    color: #3D3028;
    margin-bottom: 12px;
    line-height: 1.7;
    font-weight: 300;
}

.film-raison {
    font-size: 13px;
    background: #FFF8F0;
    color: #7A3A10;
    border-left: 3px solid #8B1A1A;
    border-radius: 0 8px 8px 0;
    padding: 8px 14px;
    line-height: 1.55;
    font-weight: 400;
}

.note-badge {
    display: inline-block;
    background: #8B1A1A;
    color: #EDE8DF;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 600;
    margin-left: 10px;
    vertical-align: middle;
    letter-spacing: 0.3px;
}

/* ---- Stat box ---- */
.stat-box {
    background: #231616;
    border: 1px solid #2E1F1F;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #A08070;
    margin-bottom: 14px;
    line-height: 1.7;
}
.stat-box b { color: #C9973A; }

/* ---- Section label ---- */
.section-label {
    font-family: 'Outfit', sans-serif;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #8B1A1A;
    margin: 0 0 6px 0;
}

/* ---- Like tags ---- */
.like-tag {
    display: inline-block;
    background: #231616;
    color: #C9973A;
    border: 1px solid #3E2222;
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 12px;
    font-weight: 500;
    margin: 2px 3px 0 0;
}

/* ---- Divider ---- */
hr {
    border: none;
    border-top: 1px solid #DDD5C8;
    margin: 1.75rem 0;
}

/* ---- Buttons ---- */
div[data-testid="stButton"] > button {
    border-radius: 8px;
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 14px;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #8B1A1A;
    border: none;
    color: #EDE8DF;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #6E1010;
}

/* ---- Multiselect tags ---- */
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #8B1A1A !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {
    color: #FFFFFF !important;
}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] [role="presentation"] {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #8B1A1A !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] span[data-baseweb="tag"] span,
section[data-testid="stSidebar"] span[data-baseweb="tag"] * {
    color: #FFFFFF !important;
}

/* ---- Caption ---- */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #9A7A60 !important;
    font-size: 12.5px !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- Session state ----------
if "likes" not in st.session_state:
    st.session_state.likes = []
if "resultats" not in st.session_state:
    st.session_state.resultats = []

# ---------- Dataset stats ----------
@st.cache_data
def get_stats():
    movies = load_movies()
    return len(movies), movies["genres"].str.split("|").explode().nunique()

nb_films, nb_genres = get_stats()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<p class="section-label">CineQuest</p>', unsafe_allow_html=True)
    st.markdown("### Mes préférences")

    st.markdown(f"""
    <div class="stat-box">
        🎞 Dataset <strong>MovieLens</strong><br>
        <b>{nb_films:,} films</b> disponibles<br>
        <span style="font-size:12px;">Notes réelles de vrais utilisateurs</span>
    </div>
    """, unsafe_allow_html=True)

    genres = st.multiselect(
        "Genres préférés",
        ["Action", "Comedy", "Drama", "Thriller", "Sci-Fi",
         "Horror", "Romance", "Animation", "Documentary", "Fantasy",
         "Adventure", "Crime", "Mystery"],
        default=["Thriller", "Sci-Fi"]
    )

    films_vus = st.text_area(
        "Films déjà vus (séparés par des virgules)",
        placeholder="Ex : Inception, Interstellar, The Matrix",
        height=90
    )

    humeur = st.select_slider(
        "Mon humeur du moment",
        options=["Détendu", "Curieux", "Aventurier", "Intense", "Mélancolique"],
        value="Curieux"
    )

    if st.session_state.likes:
        st.markdown("---")
        st.markdown('<p class="section-label">Films aimés</p>', unsafe_allow_html=True)
        likes_html = "".join(
            f'<span class="like-tag">{f}</span>' for f in st.session_state.likes
        )
        st.markdown(likes_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Réinitialiser les likes"):
            st.session_state.likes = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    recommander = st.button(
        "🎬  Recommander des films",
        type="primary",
        use_container_width=True
    )

# ---------- Page principale ----------
st.markdown('<p class="section-label">Recommandation intelligente · MovieLens × LLM</p>', unsafe_allow_html=True)
st.title("CineQuest")
st.markdown(
    "Système de recommandation basé sur le dataset **MovieLens** "
    "et un LLM *(Llama 3.3)* pour la personnalisation selon votre humeur."
)

if recommander:
    if not genres:
        st.warning("Sélectionne au moins un genre dans la sidebar.")
    else:
        with st.spinner("Analyse du dataset MovieLens + génération LLM..."):
            try:
                resultats = get_recommendations(
                    genres, films_vus, humeur, st.session_state.likes
                )
                st.session_state.resultats = resultats
            except Exception as e:
                st.error(f"Erreur : {e}")

if st.session_state.resultats:
    st.markdown("---")
    st.markdown(
        f"### Sélection du soir"
        f'<span style="font-family:\'Outfit\',sans-serif; font-size:14px; '
        f'color:#9A7A60; font-weight:300; margin-left:12px;">humeur : {humeur}</span>',
        unsafe_allow_html=True
    )
    st.caption("5 films sélectionnés parmi le dataset MovieLens · classés par note réelle")
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, film in enumerate(st.session_state.resultats):
        with cols[i % 2]:
            note = film.get("note", "")
            note_html = f'<span class="note-badge">★ {note}</span>' if note else ""
            num = ["I", "II", "III", "IV", "V"][i]

            st.markdown(f"""
<div class="film-card">
  <span class="film-number">{num}</span>
  <div class="film-title">{film['titre']} ({film.get('annee', '')}) {note_html}</div>
  <div class="film-meta">{film['genre']}</div>
  <div class="film-synopsis">{film['synopsis']}</div>
  <div class="film-raison">🎯 {film['raison']}</div>
</div>
""", unsafe_allow_html=True)

            if st.button(f"♡  J'aime — {film['titre']}", key=f"like_{i}"):
                if film["titre"] not in st.session_state.likes:
                    st.session_state.likes.append(film["titre"])
                    st.success(f"✓  Ajouté aux likes !")
                    st.rerun()
else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "Configure tes préférences dans la sidebar et clique sur "
        "**🎬 Recommander des films** pour commencer."
    )