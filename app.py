import streamlit as st
import pandas as pd

st.title("Plan détaillé de mémoire")

# Initialisation
if 'plan' not in st.session_state:
    st.session_state.plan = []

# Fonction pour déplacer une partie
def move_part(index, direction):
    plan = st.session_state.plan
    if direction == "up" and index > 0:
        plan[index], plan[index-1] = plan[index-1], plan[index]
    elif direction == "down" and index < len(plan)-1:
        plan[index], plan[index+1] = plan[index+1], plan[index]

# Formulaire pour ajouter une partie
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
            "Sous_parties": [s.strip() for s in sous_parties.split(",") if s.strip()],
            "Commentaires": commentaires
        })
        st.success(f"Partie '{titre}' ajoutée !")

# Affichage du plan actuel
st.subheader("Plan actuel")
total_pages = 0
for idx, partie in enumerate(st.session_state.plan):
    st.markdown(f"### Partie {idx+1}: {partie['Titre']} ({partie['Nb_pages']} pages)")
    total_pages += partie['Nb_pages']
    
    col1, col2, col3, col4 = st.columns([1,1,1,6])
    with col1:
        if st.button("↑", key=f"up_{idx}"):
            move_part(idx, "up")
    with col2:
        if st.button("↓", key=f"down_{idx}"):
            move_part(idx, "down")
    with col3:
        if st.button("❌", key=f"del_{idx}"):
            st.session_state.plan.pop(idx)
            st.experimental_rerun()
    
    with col4:
        if partie['Sous_parties']:
            st.write("**Sous-parties:**")
            for sp_idx, sp in enumerate(partie['Sous_parties']):
                col_a, col_b = st.columns([8,1])
                with col_a:
                    st.write(f"- {sp}")
                with col_b:
                    if st.button("❌", key=f"del_sp_{idx}_{sp_idx}"):
                        partie['Sous_parties'].pop(sp_idx)
                        st.experimental_rerun()
        if partie['Commentaires']:
            st.write(f"**Commentaires:** {partie['Commentaires']}")

st.markdown(f"**Nombre total de pages prévu : {total_pages}**")

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
