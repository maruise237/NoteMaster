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
    ["Dashboard", "Prise de Notes", "Mode Quiz", "API", "Docs"], 
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
        
        # Fonction pour charger les questions et les stocker dans session_state
        def load_questions():
            if os.path.exists(json_file_path):
                with open(json_file_path, "r") as file:
                    return json.load(file)
            return []

        # Initialisation des questions si pas encore chargées
        if "questions" not in st.session_state or st.session_state.get("current_note") != selected_note:
            st.session_state.questions = load_questions()
            st.session_state.current_note = selected_note  # Stocker la note sélectionnée

        # Générer de nouvelles questions
        if st.button("Générer des questions"):
            try:
                with st.spinner("Génération des questions en cours..."):
                    new_questions = generate_questions(selected_note, note_content)
                
                if new_questions:
                    with open(json_file_path, "w") as file:
                        json.dump(new_questions, file, indent=4, ensure_ascii=False)
                    
                    st.session_state.questions = new_questions  # Met à jour en session_state
                    st.success("Questions générées et sauvegardées avec succès !")
                else:
                    st.error("L'API n'a retourné aucune question. Veuillez vérifier le contenu des notes ou l'API.")
            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")

        # Afficher les questions
        if st.session_state.questions:
            st.write("### Questions :")
            for i, question in enumerate(st.session_state.questions, 1):
                with st.expander(f"Question {i}: {question['text']}"):
                    user_answer = st.text_input(f"Votre réponse pour la question {i}", key=f"answer_{i}")
                    if st.button(f"Vérifier la réponse {i}", key=f"check_{i}"):
                        st.write(f"**Réponse correcte :** {question['reponse']}")

            # Bouton pour supprimer les questions existantes
            if st.button("🗑️ Supprimer toutes les questions"):
                try:
                    os.remove(json_file_path)  # Supprime le fichier JSON
                    st.session_state.questions = []  # Met à jour immédiatement
                    st.success("Les questions ont été supprimées avec succès !")
                except Exception as e:
                    st.error(f"Erreur lors de la suppression : {e}")
        
        else:
            st.info("Aucune question disponible. Cliquez sur 'Générer des questions' pour commencer.")


elif menu == "API":
    st.header("Configuration de l'API")

    # Charger la clé API existante (si elle existe)
    if "api_key" not in st.session_state:
        from dotenv import load_dotenv
        load_dotenv()
        st.session_state.api_key = os.getenv("DEEPSEEK_KEY", "")

    # Formulaire pour entrer ou mettre à jour la clé API
    st.write("Entrez votre clé API de OpenRouter pour activer les fonctionnalités de génération.")
    api_key_input = st.text_input(
        "Clé API",
        value=st.session_state.api_key,
        placeholder="Entrez votre clé API",
        type="password",
        key="api_input"
    )

    # Boutons pour enregistrer ou réinitialiser
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enregistrer la clé API"):
            if len(api_key_input) == 73:
                with open(".env", "w") as file:
                    file.write(f'DEEPSEEK_KEY="{api_key_input}"')
                st.session_state.api_key = api_key_input
                st.success("Clé API enregistrée avec succès !")
            else:
                st.error("Clé API invalide. Elle doit comporter exactement 73 caractères.")

    with col2:
        if st.button("Réinitialiser la clé API"):
            if os.path.exists(".env"):
                os.remove(".env")
            st.session_state.api_key = ""
            st.warning("Clé API réinitialisée. Veuillez en entrer une nouvelle.")


elif menu == "Docs":
    st.header("📖 Docs")

    # Bouton vers le dépôt GitHub
    st.subheader("Accéder au Répo GitHub")
    st.write("Vous pouvez accéder au code source et aux détails du projet sur le répo GitHub.")
    st.link_button("👉 Aller au dépôt GitHub", url="https://github.com/mamour-dx/NoteMaster")

    # Documentation sur la gestion de l'API DeepSeek via OpenRouter
    st.subheader("Configurer l'API DeepSeek V3 via OpenRouter")
    st.markdown(
        """
        Pour utiliser l'API DeepSeek dans cette application, vous devez générer une clé API OpenRouter et la configurer. Deux options sont disponibles :

        ### 1️⃣ Obtenir une clé API OpenRouter
        - Rendez-vous sur [OpenRouter](https://openrouter.ai) et créez un compte.
        - Générez une clé API gratuite pour le model DeepSeek V3.

        ### 2️⃣ Ajouter votre clé API à l'application

        **Option 1 : via un fichier `.env` (manuel)**
        - Créez un fichier `.env` à la racine du projet.
        - Ajoutez-y la ligne suivante en remplaçant `VOTRE_CLE_API` par votre clé API :
          ```
          DEEPSEEK_KEY=VOTRE_CLE_API
          ```
        - Redémarrez l'application pour que les modifications soient prises en compte :
          ```bash
          streamlit run app.py
          ```

        **Option 2 : directement via l'application (automatique)**
        - Accédez à l'onglet **API** dans le menu latéral de l'application.
        - Entrez votre clé API dans le champ prévu et cliquez sur **Enregistrer**.
        - L'application enregistrera automatiquement la clé pour une utilisation immédiate.

        ### 💡 Résolution des problèmes
        Si vous rencontrez des problèmes avec l'API :
        - Vérifiez que votre clé API est correcte et valide.
        - Assurez-vous que vous avez bien installé les dépendances nécessaires (`pip install openai`).
        - Consultez la documentation d'OpenRouter ici : [Documentation OpenRouter](https://openrouter.ai/docs).

        ### 🚀 Besoin d'aide ou d'une nouvelle fonctionnalité ?
        Si vous avez un problème ou souhaitez suggérer une amélioration, ouvrez un **issue** sur GitHub :
        👉 [Ouvrir un issue](https://github.com/mamour-dx/NoteMaster/issues)
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