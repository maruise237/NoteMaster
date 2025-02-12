import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from config import QUESTIONS_DIR, QUESTIONS_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Configuration API
api_key = os.getenv("DEEPSEEK_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def generate_questions(note_title, note_content):
    """
    Génère des questions à partir du contenu des notes en utilisant l'API DeepSeek.
    :param note_title: Titre de la note
    :param note_content: Contenu de la note
    :return: Une liste de questions générées
    """
    try:
        prompt = (
            f"À partir de ce texte, crée des questions relativement ouvertes qui permettent l'apprentissage actif. "
            f"Tu choisiras un nombre de questions adéquat en fonction de la longueur du texte.\n"
            f"Pour chaque question, retourne un JSON avec deux clés : "
            f"'text' pour la question et 'reponse' pour la réponse correcte.\n"
            f"Texte : {note_content}\n"
            f"Retourne uniquement du JSON, rien d'autre."
        )

        # Envoyer la requête à l'API
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mxr.codes",
                "X-Title": "Python-Accelerator",
            },
            extra_body={},
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # Vérification de la réponse
        logging.info("Réponse brute de l'API : %s", response)
        generated_text = response.choices[0].message.content.strip()
        if generated_text.startswith("```json") and generated_text.endswith("```"):
            generated_text = generated_text.strip("```json").strip("```")
        if not generated_text:
            raise ValueError("Réponse vide retournée par l'API.")

        # Chargement du JSON
        try:
            questions = json.loads(generated_text)
        except json.JSONDecodeError as json_err:
            logging.error("Erreur lors de l'analyse du JSON : %s", json_err)
            raise ValueError("La réponse de l'API n'est pas un JSON valide.")

        # Sauvegarder les questions dans un fichier JSON
        json_file_path = os.path.join(QUESTIONS_DIR, f"{note_title}.json")
        with open(json_file_path, "w") as file:
            json.dump(questions, file, indent=4, ensure_ascii=False)
        logging.info("Questions sauvegardées dans : %s", json_file_path)
        return questions

    except Exception as e:
        logging.error("Erreur lors de la génération des questions : %s", e)
        return []

def save_questions(questions):
    """
    Sauvegarde les questions générées dans un fichier JSON.
    :param questions: Liste des questions
    """
    try:
        if not os.path.exists(os.path.dirname(QUESTIONS_FILE)):
            os.makedirs(os.path.dirname(QUESTIONS_FILE))
        with open(QUESTIONS_FILE, "w") as file:
            json.dump(questions, file, indent=4)
        logging.info("Questions sauvegardées dans le fichier principal : %s", QUESTIONS_FILE)
    except Exception as e:
        logging.error("Erreur lors de la sauvegarde des questions : %s", e)

def load_questions():
    """
    Charge les questions sauvegardées à partir du fichier JSON.
    :return: Liste des questions
    """
    try:
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, "r") as file:
                return json.load(file)
    except Exception as e:
        logging.error("Erreur lors du chargement des questions : %s", e)
    return []
