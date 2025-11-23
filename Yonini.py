import streamlit as st

st.set_page_config(page_title="Unicorn Quest", layout="centered")

# ----- STYLE -----
st.markdown("""
<style>
    body { background:#ffe6ff; }
    .box {
        width: 380px;
        background: #fff0ff;
        margin: auto;
        padding: 20px;
        border-radius: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        text-align: center;
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

# ----- STATE -----
if "food" not in st.session_state:
    st.session_state.food = 60
    st.session_state.water = 60
    st.session_state.happy = 50
    st.session_state.xp = 0
    st.session_state.tasks = {"eat": False, "drink": False, "play": False}

# ----- UNICORN IMAGE -----
def get_unicorn():
    if st.session_state.happy > 80:
        return "https://i.imgur.com/ap1wijS.png"
    elif st.session_state.happy > 50:
        return "https://i.imgur.com/xF7Lw1n.png"
    else:
        return "https://i.imgur.com/v6W4iho.png"

def add_xp(amount):
    st.session_state.xp += amount
    st.session_state.happy = min(100, st.session_state.happy + amount / 2)

# ----- GAME BOX -----
st.markdown('<div class="box">', unsafe_allow_html=True)

st.image(get_unicorn(), width=200, caption="🦄 חד־קרן תינוק")

st.write("### 💞 מצב שמחה")
st.markdown(f"""
<div class="bar"><div class="fill" style="width:{st.session_state.happy}%; background:#ff85d0;"></div></div>
""", unsafe_allow_html=True)

# ----- BUTTONS -----
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🍎 אוכל"):
        st.session_state.food = min(100, st.session_state.food + 20)
        st.session_state.tasks["eat"] = True
        add_xp(10)

with col2:
    if st.button("🥤 מים"):
        st.session_state.water = min(100, st.session_state.water + 20)
        st.session_state.tasks["drink"] = True
        add_xp(10)

with col3:
    if st.button("🧸 שחק"):
        st.session_state.happy = min(100, st.session_state.happy + 15)
        st.session_state.tasks["play"] = True
        add_xp(15)

# ----- TASKS -----
st.write("## 🎯 משימות יומיות")
st.write("• 🍎 תאכיל את החד־קרן")
st.write("• 🥤 תן לו מים")
st.write("• 🧸 שחק איתו")

done = all(st.session_state.tasks.values())

if done:
    st.success("🎁 כל המשימות הושלמו! קיבלת תיבת פרס!")
    if st.button("📦 פתח את התיבה"):
        st.balloons()
        st.session_state.happy = min(100, st.session_state.happy + 30)
        st.session_state.xp += 50
        st.session_state.tasks = {"eat": False, "drink": False, "play": False}

# ----- XP -----
st.write(f"### ⭐ XP: **{st.session_state.xp}**")

st.markdown("</div>", unsafe_allow_html=True)
