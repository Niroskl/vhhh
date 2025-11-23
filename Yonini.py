import streamlit as st

st.set_page_config(page_title="Unicorn Simple", layout="centered")

# ----- STATE -----
if "food" not in st.session_state:
    st.session_state.food = 50
    st.session_state.water = 50
    st.session_state.happy = 50

# ----- IMAGE -----
st.image("https://i.imgur.com/xF7Lw1n.png", width=200)

st.write("## חד־קרן תינוק 🦄")

# BARS
st.write(f"🍎 אוכל: {st.session_state.food}%")
st.progress(st.session_state.food / 100)

st.write(f"💧 מים: {st.session_state.water}%")
st.progress(st.session_state.water / 100)

st.write(f"💞 שמחה: {st.session_state.happy}%")
st.progress(st.session_state.happy / 100)

# BUTTONS
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🍎 אוכל"):
        st.session_state.food = min(100, st.session_state.food + 10)
        st.session_state.happy = min(100, st.session_state.happy + 5)

with col2:
    if st.button("🥤 מים"):
        st.session_state.water = min(100, st.session_state.water + 10)
        st.session_state.happy = min(100, st.session_state.happy + 5)

with col3:
    if st.button("🧸 משחק"):
        st.session_state.happy = min(100, st.session_state.happy + 15)
