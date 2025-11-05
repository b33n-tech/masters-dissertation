import streamlit as st
import json

st.title("Workspace d'enrichissement de plan de mémoire")

# Initialisation
if 'plan' not in st.session_state:
    # Charger ton plan existant directement depuis un JSON ou définir les titres
    st.session_state.plan = [
        {"titre": "Abstract", "contenu": "", "notes": []},
        {"titre": "Introduction", "contenu": "", "notes": []},
        {"titre": "Literature Review", "contenu": "", "notes": []},
        {"titre": "Methodology", "contenu": "", "notes": []},
        {"titre": "Results", "contenu": "", "notes": []},
        {"titre": "Discussion", "contenu": "", "notes": []},
        {"titre": "Conclusion", "contenu": "", "notes": []},
        {"titre": "Annexes", "contenu": "", "notes": []},
    ]

# Choisir la partie à éditer
chapitre = st.selectbox("Sélectionner une partie à enrichir", [p["titre"] for p in st.session_state.plan])
index = [p["titre"] for p in st.session_state.plan].index(chapitre)
current_chap = st.session_state.plan[index]

# Affichage du contenu existant
st.subheader("Contenu existant")
st.text_area("Texte principal", value=current_chap["contenu"], key=f"contenu_{index}")

# Ajouter des notes/annotations
st.subheader("Notes / idées / citations")
new_note = st.text_input("Ajouter une note")
note_tag = st.text_input("Tag (ex: citation, idée, exemple)")
if st.button("Ajouter la note", key=f"note_btn_{index}"):
    if new_note.strip() != "":
        current_chap["notes"].append({"texte": new_note, "tag": note_tag})
        st.success("Note ajoutée !")

# Affichage des notes existantes
if current_chap["notes"]:
    st.write("Notes existantes :")
    for n_idx, note in enumerate(current_chap["notes"]):
        st.write(f"- [{note['tag']}] {note['texte']}")

# Sauvegarde globale en JSON
if st.button("Exporter tout le plan en JSON"):
    st.download_button(
        "Télécharger le plan",
        data=json.dumps(st.session_state.plan, ensure_ascii=False, indent=2),
        file_name="plan_enrichi.json",
        mime="application/json"
    )
