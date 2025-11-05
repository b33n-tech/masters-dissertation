import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Plan détaillé de mémoire")

# Initialisation du stockage si pas déjà fait
if 'plan' not in st.session_state:
    st.session_state.plan = []

# Formulaire pour ajouter une nouvelle partie
with st.form("ajouter_partie"):
    st.subheader("Ajouter une nouvelle partie")
    titre = st.text_input("Titre de la partie")
    nb_pages = st.number_input("Nombre de pages prévu", min_value=1, step=1)
    sous_parties = st.text_area("Sous-parties (séparer par des virgules)")
    commentaires = st.text_area("Commentaires divers")
    submitted = st.form_submit_button("Ajouter la partie")
    
    if submitted:
        st.session_state.plan.append({
            "Titre": titre,
            "Nb_pages": nb_pages,
            "Sous_parties": [s.strip() for s in sous_parties.split(",") if s.strip() != ""],
            "Commentaires": commentaires
        })
        st.success(f"Partie '{titre}' ajoutée !")

# Affichage du plan actuel
st.subheader("Plan actuel")
if st.session_state.plan:
    for idx, partie in enumerate(st.session_state.plan):
        st.markdown(f"### Partie {idx+1}: {partie['Titre']} ({partie['Nb_pages']} pages)")
        if partie['Sous_parties']:
            st.write("**Sous-parties:**")
            for sp in partie['Sous_parties']:
                st.write(f"- {sp}")
        if partie['Commentaires']:
            st.write(f"**Commentaires:** {partie['Commentaires']}")
else:
    st.info("Aucune partie ajoutée pour l'instant.")

# Option pour télécharger le plan en CSV
if st.session_state.plan:
    df = pd.DataFrame([
        {
            "Titre": p["Titre"],
            "Nb_pages": p["Nb_pages"],
            "Sous_parties": ", ".join(p["Sous_parties"]),
            "Commentaires": p["Commentaires"]
        } 
        for p in st.session_state.plan
    ])
    st.download_button("Télécharger le plan en CSV", df.to_csv(index=False), "plan_memoire.csv", "text/csv")
