import streamlit as st

# רשימת שורות מתוך שירים עם התשובה - שם השיר
questions = [
    {"line": "Imagine all the people living life in peace", "answer": "Imagine"},
    {"line": "Cause this is thriller, thriller night", "answer": "Thriller"},
    {"line": "Is this the real life? Is this just fantasy?", "answer": "Bohemian Rhapsody"},
    {"line": "How many roads must a man walk down before you call him a man?", "answer": "Blowin' in the Wind"},
    {"line": "When you were here before, couldn't look you in the eye", "answer": "Creep"},
]

st.title("חידון שירים - נחש את השיר מהמילים")

if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "finished" not in st.session_state:
    st.session_state.finished = False

def check_answer():
    user_answer = st.session_state.user_answer.strip().lower()
    correct_answer = questions[st.session_state.current_question]["answer"].lower()
    if user_answer == correct_answer:
        st.session_state.score += 1
        st.success("נכון! 🎉")
    else:
        st.error(f"לא נכון ❌ התשובה הנכונה היא: {questions[st.session_state.current_question]['answer']}")
    st.session_state.current_question += 1

if st.session_state.finished:
    st.write(f"המשחק הסתיים! ניקוד סופי: {st.session_state.score}/{len(questions)}")
    if st.button("שחק שוב"):
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.finished = False
else:
    if st.session_state.current_question < len(questions):
        q = questions[st.session_state.current_question]
        st.write(f"מילים מתוך השיר: \n\n> {q['line']}")
        st.text_input("מה שם השיר?", key="user_answer", value="")
        if st.button("שלח תשובה"):
            if st.session_state.user_answer.strip() == "":
                st.warning("אנא הזן תשובה לפני שליחה")
            else:
                check_answer()
    else:
        st.session_state.finished = True
        st.experimental_rerun()
