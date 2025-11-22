import streamlit as st
import random

st.set_page_config(page_title="Baby Unicorn Game", layout="centered")

st.markdown("""
    <style>
        body { background: #ffeaff; }
        #game-area {
            width: 400px;
            height: 500px;
            background: linear-gradient(#ffdfff, #fff3ff);
            border-radius: 20px;
            position: relative;
            overflow: hidden;
            margin: auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .unic {
            width: 60px;
            height: 60px;
            position: absolute;
            transition: 0.05s;
        }
        .star {
            width: 40px;
            position: absolute;
        }
    </style>
""", unsafe_allow_html=True)

# --- GAME LOGIC IN SESSION STATE ---
if "x" not in st.session_state:
    st.session_state.x = 170
    st.session_state.y = 400
    st.session_state.star_x = random.randint(0, 350)
    st.session_state.star_y = random.randint(0, 200)
    st.session_state.score = 0

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️"):
        st.session_state.x = max(0, st.session_state.x - 20)
with col3:
    if st.button("➡️"):
        st.session_state.x = min(340, st.session_state.x + 20)

# Collision
if abs(st.session_state.x - st.session_state.star_x) < 40 and abs(st.session_state.y - st.session_state.star_y) < 40:
    st.session_state.score += 1
    st.session_state.star_x = random.randint(0, 350)
    st.session_state.star_y = random.randint(0, 300)

# Render game
st.markdown(f"""
    <div id="game-area">
        <img src="https://i.imgur.com/JnFqz3a.png" class="unic" style="left:{st.session_state.x}px;top:{st.session_state.y}px;">
        <img src="https://i.imgur.com/9yQ6g1B.png" class="star" style="left:{st.session_state.star_x}px;top:{st.session_state.star_y}px;">
    </div>
    <h3 style="text-align:center;">⭐ ניקוד: {st.session_state.score}</h3>
""", unsafe_allow_html=True)
