import streamlit as st
import os, json
from utils.note_manager import load_notes, save_note, delete_note
from utils.question_generator import generate_questions
from config import QUESTIONS_DIR

# Application principale

# Sidebar 
st.sidebar.title("📝 **NoteMaster**")
st.sidebar.markdown("<h3>Navigation rapide</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "📂 <span style='color: #0066CC;'>Choisissez une option :</span>", 
    ["Dashboard", "Prise de Notes", "Mode Quiz", "Docs"], 
    format_func=lambda x: f"🔹 {x}", 
    index=0,
    label_visibility="hidden", 
    key="menu_radio"
)

# Main content
if menu == "Dashboard":
    # Header with custom styles
    st.markdown("<h1>Bienvenue sur NoteMaster ⚡️</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Apprendre ses cours grâce au _Active Learning_!")

    # Feature list with emojis and custom formatting
    st.markdown(
        """
        <div style='padding: 10px;'>
            <p><strong>NoteMaster</strong> vous permet de :</p>
            <ul>
                <li>🗒️ <strong>Prendre des notes</strong> et les organiser.</li>
                <li>❓ <strong>Générer des questions</strong> pour vos cours.</li>
                <li>✅ <strong>Pratiquer l'apprentissage actif</strong> et suivre vos progrès.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )


elif menu == "Prise de Notes":
    st.header("Prise de Notes")
    
    if "notes" not in st.session_state:
        st.session_state.notes = load_notes()

    if "refresh" not in st.session_state:
        st.session_state.refresh = False

    st.write("### Vos notes :")
    if st.session_state.notes:
        for note in st.session_state.notes:
            st.write(f"- {note['title']}")
    else:
        st.write("Aucune note disponible pour le moment.")

    # Add a new note
    st.subheader("Créer une nouvelle note")
    note_title = st.text_input("Titre de la note")
    note_content = st.text_area("Contenu de la note", height=330)
    if st.button("Sauvegarder"):
        if note_title and note_content:
            save_note(note_title, note_content)
            st.session_state.notes = load_notes()
            st.success(f"Note '{note_title}' sauvegardée avec succès !")
        else:
            st.warning("Veuillez fournir un titre et un contenu pour votre note.")

    # Delete a note
    st.subheader("Supprimer une note")
    if st.session_state.notes:
        note_titles = [note["title"] for note in st.session_state.notes]
        note_to_delete = st.selectbox("Sélectionnez une note à supprimer", note_titles, key="delete_note_select")
        if st.button("Supprimer"):
            delete_note(note_to_delete)
            st.session_state.notes = load_notes()
            st.session_state.refresh = not st.session_state.refresh  
            st.success(f"Note '{note_to_delete}' supprimée avec succès !")
    else:
        st.warning("Aucune note disponible à supprimer.")



elif menu == "Mode Quiz":
    st.header("Mode Quiz")
    
    # Charger les notes disponibles
    notes = load_notes()
    note_titles = [note["title"] for note in notes]
    selected_note = st.selectbox("Choisissez une note", note_titles)
    
    if selected_note:
        note_content = next(note["content"] for note in notes if note["title"] == selected_note)
        
        json_file_path = os.path.join(QUESTIONS_DIR, f"{selected_note}.json")
        
        # Charger les questions depuis le fichier JSON si elles existent
        questions = []
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as file:
                questions = json.load(file)
        
        # Générer de nouvelles questions si l'utilisateur clique sur le bouton
        if st.button("Générer des questions"):
            try:
                with st.spinner("Génération des questions en cours..."):
                    new_questions = generate_questions(selected_note, note_content)
                
                if new_questions:
                    # Sauvegarder les nouvelles questions dans le fichier JSON
                    with open(json_file_path, "w") as file:
                        json.dump(new_questions, file, indent=4, ensure_ascii=False)
                    
                    st.success("Questions générées et sauvegardées avec succès !")
                    # Mettre à jour les questions chargées
                    questions = new_questions
                else:
                    st.error("L'API n'a retourné aucune question. Veuillez vérifier le contenu des notes ou l'API.")
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
        
        # Afficher les questions en mode Quiz
        if questions:
            st.write("### Questions :")
            for i, question in enumerate(questions, 1):
                with st.expander(f"Question {i}: {question['text']}"):
                    user_answer = st.text_input(f"Votre réponse pour la question {i}", key=f"answer_{i}")
                    if st.button(f"Vérifier la réponse {i}", key=f"check_{i}"):
                        st.write(f"**Réponse correcte :** {question['reponse']}")
        else:
            st.info("Aucune question disponible. Cliquez sur 'Générer des questions' pour commencer.")



elif menu == "Docs":
    st.header("📖 Docs")

    # Bouton vers le dépôt GitHub
    st.subheader("Accéder au Répo GitHub")
    st.write("Vous pouvez accéder au code source et aux détails du projet sur le répo GitHub.")
    st.link_button("👉 Aller au dépôt GitHub", url="https://github.com/mamour-dx/NoteMaster")

    # Documentation sur la gestion de l'API Mistral
    st.subheader("Configurer l'API Mistral")
    st.markdown(
        """
        Pour utiliser l'API Mistral dans cette application, suivez les étapes ci-dessous :

        1. **Obtenez une clé API** :
           - Rendez-vous sur le site officiel de [Mistral](https://mistral.ai) pour générer une clé API.
           - Connectez-vous ou créez un compte si nécessaire.

        2. **Configurer votre clé API dans un fichier `.env`** :
           - Créez un fichier `.env` à la racine du projet.
           - Ajoutez-y la ligne suivante en remplaçant `VOTRE_CLE_API` par votre clé API :
             ```
             MISTRAL_KEY=VOTRE_CLE_API
             ```

        3. **Redémarrez l'application** :
           - Une fois configuré, redémarrez votre application Streamlit pour prendre en compte les modifications.
            ```bash
              streamlit run app.py
              ````

        Si vous rencontrez des problèmes avec l'API, assurez-vous que :
        - Votre clé API est valide et non expirée.
        - Vous avez correctement installé toutes les dépendances nécessaires (par exemple, via `pip install mistralai`).

        Consultez la documentation de Mistral pour plus de détails : [Documentation Mistral](https://mistral.ai/docs).
        """
    )
    
    # Ajout d'un espace pour d'autres paramètres futurs
    st.subheader("Autres paramètres")
    st.write("Des options supplémentaires seront ajoutées ici à l'avenir.")



# Divider
st.markdown("---")


st.markdown("### 🌟 Ressources utiles :")
# Align the buttons horizontally
col1, col2 = st.columns(2)
with col1:
    st.link_button("📄 Répo Github", url="https://github.com/mamour-dx/NoteMaster")
with col2:
    st.link_button("📚 Vidéo YouTube", url="https://youtube.com/@mxr_codes")