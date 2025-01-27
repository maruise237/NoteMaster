# 📝 Active Learning avec Python et Mistral

Ce projet combine la prise de notes et l'apprentissage actif grâce à l'intégration de Python et de l'API Mistral. L'application permet aux étudiants de prendre des notes, de générer des questions basées sur leurs notes et de répondre à ces questions avec des corrections automatiques accompagnées d'explications détaillées. 🚀

---

## 🛠️ Fonctionnalités

- **Prise de notes simplifiée** : Ajoutez, consultez et supprimez des notes facilement.
- **Génération de questions** : Utilisez l'API de Mistral pour transformer vos notes en questions relativment ouverte.
- **Correction instantanée** : Répondez aux questions et recevez des explications détaillées sur vos réponses.
- **Interface intuitive** : Une interface graphique épurée et facile à utiliser grâce à Streamlit.
- **Configuration de l'API** : Gérer votre clé API Mistral directement depuis l'interface sur la partie API.

---

## 📋 Prérequis

1. **Python 3.9 ou plus**
2. **Bibliothèques Python nécessaires** :
    - `streamlit`
    - `dotenv`
    - `mistralai` 
3. **Clé API Mistral** :
    - Créer un compte et obtenez votre clé auprès de [Mistral](https://mistral.ai) et configurez-la dans le projet.
---

## 🚀 Installation

1. Clonez ce dépôt :
    ```bash
    git clone https://github.com/mamour-dx/NoteMaster.git
    cd NoteMaster
    ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

3. Lancez l'application Streamlit :
    ```bash
    streamlit run main.py
    ```

---

## 📚 Utilisation

### Configuration de l'API 🛠️

1. Lancez l'application et rendez-vous dans la section **API**.
2. Entrez votre clé API de Mistral.
3. Sauvegardez pour l'utiliser avec l'application.

### Prise de notes ✍️

1. Ajoutez une nouvelle note en remplissant le titre et le contenu.
2. Consultez la liste de vos notes existantes.
3. Supprimez des notes si nécessaire.

### Génération de questions 🎯

1. Rendez-vous dans la section **Questions**.
2. Sélectionnez une note pour générer des questions basées sur son contenu.
3. Visualisez les questions générées et répondez-y directement dans l'interface.

---

## 📦 Structure du projet

```
active-learning-mistral/
├── main.py               # Fichier principal Streamlit
├── config.py             # Gestion des configurations (dossiers de notes et de questions)
├── utils/
│   ├── notes_manager.py  # Gestion des notes (ajout, suppression, chargement)
│   ├── question_manager.py  # Génération et gestion des questions
├── notes/                # Dossier de sauvegarde des notes (en format txt)
├── questions/            # Dossier de sauvegarde des questions (en format json)
├── .env                  # Fichier pour la clé API
└── requirements.txt      # Dépendances Python 
```

---

## 🤝 Contribuer

Les contributions sont les bienvenues !

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité :
    ```bash
    git checkout -b feature/ma-nouvelle-fonctionnalite
    ```
3. Commitez vos modifications :
    ```bash
    git commit -m "Ajout d'une nouvelle fonctionnalité"
    ```
4. Poussez la branche :
    ```bash
    git push origin feature/ma-nouvelle-fonctionnalite
    ```
5. Ouvrez une Pull Request.

---

## 🛡️ Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.

---

## ❤️ Remerciements

Merci à tous ceux qui soutiennent ce projet et à la communauté Python pour ses ressources incroyables. 🙌
