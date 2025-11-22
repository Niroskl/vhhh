import streamlit as st

st.set_page_config(page_title="Baby Unicorn", layout="centered")

st.markdown("""
    <style>
        body { background:#ffe6ff; }
        #game {
            width: 350px;
            height: 420px;
            background: linear-gradient(#ffe6ff,#fff0ff);
            border-radius: 25px;
            margin: auto;
            padding-top: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            text-align: center;
        }
        .unic {
            width: 180px;
            border-radius: 20px;
        }
        .bar {
            width: 80%;
            height: 20px;
            background: #ffd3f7;
            border-radius: 12px;
            margin: auto;
            overflow: hidden;
        }
        .fill {
            height: 100%;
            border-radius: 12px;
            transition: 0.3s;
        }
    </style>
""", unsafe_allow_html=True)

# --- STATE ---
if "food" not in st.session_state:
    st.session_state.food = 50
    st.session_state.water = 50

# --- BUTTONS ---
st.markdown("<div id='game'>", unsafe_allow_html=True)

st.image("https://i.imgur.com/xF7Lw1n.png", width=200, caption="🦄 חד־קרן תינוק")

st.write("### 🍼 מצב רעב:")
st.markdown(f"""
<div class="bar">
    <div class="fill" style="width:{st.session_state.food}%; background:#ff92d0;"></div>
</div>""", unsafe_allow_html=True)

st.write("### 💧 מצב צמא:")
st.markdown(f"""
<div class="bar">
    <div class="fill" style="width:{st.session_state.water}%; background:#92caff;"></div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("🍎 תן אוכל"):
        st.session_state.food = min(100, st.session_state.food + 15)

with col2:
    if st.button("🥤 תן מים"):
        st.session_state.water = min(100, st.session_state.water + 15)

st.markdown("</div>", unsafe_allow_html=True)
