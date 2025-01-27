import streamlit as st

def evaluate_answer(question, user_answer):
    correct = question["answer"].strip().lower() == user_answer.strip().lower()
    return correct

def provide_feedback(question, correct):
    if correct:
        return f"Bonne réponse ! {question['explanation']}"
    else:
        return f"Mauvaise réponse. {question['explanation']}"

def start_quiz(questions):
    for question in questions:
        st.write(question["text"])
        user_answer = st.text_input("Votre réponse :")
        if st.button("Valider"):
            correct = evaluate_answer(question, user_answer)
            feedback = provide_feedback(question, correct)
            st.write(feedback)
