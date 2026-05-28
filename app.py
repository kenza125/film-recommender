import streamlit as st
from recommender import get_recommendations

st.set_page_config(
    page_title="CineAI — Recommandation de films",
    page_icon="🎬",
    layout="wide"
)

# ---------- CSS custom ----------
st.markdown("""
<style>
.film-card {
    background: #FFFFFF;
    border: 1px solid #D3D1C7;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.film-title { font-size: 17px; font-weight: 600; margin: 0 0 2px; }
.film-meta  { font-size: 12px; color: #5F5E5A; margin: 0 0 8px; }
.film-synopsis { font-size: 13px; color: #444441; margin-bottom: 8px; }
.film-raison {
    font-size: 13px;
    background: #EEEDFE;
    color: #3C3489;
    border-radius: 8px;
    padding: 8px 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "likes" not in st.session_state:
    st.session_state.likes = []
if "resultats" not in st.session_state:
    st.session_state.resultats = []

# ---------- Sidebar ----------
with st.sidebar:
    st.title("Mes préférences")

    genres = st.multiselect(
        "Genres préférés",
        ["Action", "Comédie", "Drame", "Thriller", "Science-fiction",
         "Horreur", "Romance", "Animation", "Documentaire", "Fantastique"],
        default=["Thriller", "Science-fiction"]
    )

    films_vus = st.text_area(
        "Films déjà vus (séparés par des virgules)",
        placeholder="Ex : Inception, Interstellar, The Dark Knight",
        height=100
    )

    humeur = st.select_slider(
        "Mon humeur du moment",
        options=["Détendu", "Curieux", "Aventurier", "Intense", "Mélancolique"],
        value="Curieux"
    )

    if st.session_state.likes:
        st.markdown("---")
        st.markdown("**Films aimés :**")
        for f in st.session_state.likes:
            st.markdown(f"- {f}")
        if st.button("Réinitialiser les likes"):
            st.session_state.likes = []
            st.rerun()

    recommander = st.button("Recommander des films", type="primary", use_container_width=True)

# ---------- Page principale ----------
st.title("CineAI — Recommandation de films")
st.markdown("Système de recommandation intelligent basé sur un LLM.")

if recommander:
    if not genres:
        st.warning("Sélectionne au moins un genre dans la sidebar.")
    else:
        with st.spinner("Le LLM analyse ton profil et sélectionne les meilleurs films..."):
            try:
                resultats = get_recommendations(genres, films_vus, humeur, st.session_state.likes)
                st.session_state.resultats = resultats
            except Exception as e:
                st.error(f"Erreur lors de la recommandation : {e}")

if st.session_state.resultats:
    st.markdown(f"### 5 films recommandés pour toi — humeur *{humeur}*")
    st.markdown("---")

    cols = st.columns(2)
    for i, film in enumerate(st.session_state.resultats):
        with cols[i % 2]:
            st.markdown(f"""
<div class="film-card">
  <div class="film-title">{film['titre']} ({film['annee']})</div>
  <div class="film-meta">{film['genre']}</div>
  <div class="film-synopsis">{film['synopsis']}</div>
  <div class="film-raison">Pourquoi ce film ? {film['raison']}</div>
</div>
""", unsafe_allow_html=True)

            if st.button(f"J'aime — {film['titre']}", key=f"like_{i}"):
                if film['titre'] not in st.session_state.likes:
                    st.session_state.likes.append(film['titre'])
                    st.success(f"'{film['titre']}' ajouté à tes likes !")
                    st.rerun()
else:
    st.info("Configure tes préférences dans la sidebar et clique sur **Recommander des films**.")
