import streamlit as st

# רשימת שאלות לדוגמה
questions = [
    {"question": "מי שר את השיר 'Imagine'?", "answer": "ג'ון לנון"},
    {"question": "מי שר את השיר 'Thriller'?", "answer": "מייקל ג'קסון"},
    {"question": "מי שר את השיר 'Bohemian Rhapsody'?", "answer": "פרדי מרקורי"},
    {"question": "מי שר את השיר 'Like a Rolling Stone'?", "answer": "בוב דילן"},
    {"question": "מי שר את השיר 'Shape of You'?", "answer": "אד שירן"},
    # אפשר להוסיף עוד שאלות פה...
]

st.title("חידון שירים")

if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "finished" not in st.session_state:
    st.session_state.finished = False

def check_answer():
    user_answer = st.session_state.user_answer.strip()
    current_q = questions[st.session_state.current_question]
    if user_answer == current_q["answer"]:
        st.session_state.score += 1
        st.success("נכון! 🎉")
    else:
        st.error(f"לא נכון ❌ התשובה הנכונה היא: {current_q['answer']}")
    st.session_state.current_question += 1
    st.session_state.user_answer = ""

if st.session_state.finished:
    st.write(f"המשחק הסתיים! ניקוד סופי: {st.session_state.score}/{len(questions)}")
    if st.button("שחק שוב"):
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.finished = False
else:
    if st.session_state.current_question < len(questions):
        q = questions[st.session_state.current_question]
        st.write(q["question"])
        st.text_input("הקלד את התשובה שלך כאן:", key="user_answer")
        if st.button("שלח תשובה"):
            if st.session_state.user_answer.strip() == "":
                st.warning("אנא הכנס תשובה לפני שליחה")
            else:
                check_answer()
    else:
        st.session_state.finished = True
        st.experimental_rerun()
