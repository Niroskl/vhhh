import streamlit as st
import random

st.set_page_config(page_title="Baby Unicorn Plus", layout="centered")

# --- INIT STATE SAFELY ---
if "food" not in st.session_state:
    st.session_state.food = 50
if "water" not in st.session_state:
    st.session_state.water = 50
if "happy" not in st.session_state:
    st.session_state.happy = 50

# --- SAFE GET FUNCTION ---
def get_state(key, default):
    return st.session_state.get(key, default)

# --- UNICORN IMAGE LOGIC ---
def get_unicorn_image():
    food = get_state("food", 50)
    water = get_state("water", 50)
    happy = get_state("happy", 50)

    if happy > 70:
        return "https://i.imgur.com/L6KAHqr.png"   # שמח
    if food < 30 or water < 30:
        return "https://i.imgur.com/3j5s8vR.png"   # עצוב
    return "https://i.imgur.com/xF7Lw1n.png"       # רגיל

# --- STYLING ---
st.markdown("""
<style>
    body { background:#ffe6ff; }
    #game {
        width: 360px;
        background: linear-gradient(#ffe6ff,#fff0ff);
        border-radius: 25px;
        margin: auto;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
    }
    .bar {
        width: 85%;
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

def cap(v):
    return max(0, min(100, v))

st.markdown("<div id='game'>", unsafe_allow_html=True)

# --- DISPLAY UNICORN ---
st.image(get_unicorn_image(), width=200, caption="🦄 חד־קרן תינוק")

# --- BARS ---
st.write("### 🍼 רעב:")
st.markdown(
    f"<div class='bar'><div class='fill' style='width:{st.session_state.food}%; background:#ff92d0;'></div></div>",
    unsafe_allow_html=True,
)

st.write("### 💧 צמא:")
st.markdown(
    f"<div class='bar'><div class='fill' style='width:{st.session_state.water}%; background:#92caff;'></div></div>",
    unsafe_allow_html=True,
)

st.write("### 🌟 שמחה:")
st.markdown(
    f"<div class='bar'><div class='fill' style='width:{st.session_state.happy}%; background:#ffd966;'></div></div>",
    unsafe_allow_html=True,
)

st.write("---")

# --- FOOD ---
st.write("## 🍎 אוכל")
f1, f2, f3, f4 = st.columns(4)

with f1:
    if st.button("🍎 תפוח"):
        st.session_state.food = cap(st.session_state.food + 10)
        st.session_state.happy = cap(st.session_state.happy + 5)

with f2:
    if st.button("🎂 עוגה"):
        st.session_state.food = cap(st.session_state.food + 20)
        st.session_state.happy = cap(st.session_state.happy + 10)

with f3:
    if st.button("🍭 סוכריה"):
        st.session_state.food = cap(st.session_state.food + 8)
        st.session_state.happy = cap(st.session_state.happy + 12)

with f4:
    if st.button("🥕 גזר"):
        st.session_state.food = cap(st.session_state.food + 6)

st.write("---")

# --- DRINKS ---
st.write("## 🥤 שתייה")
d1, d2 = st.columns(2)

with d1:
    if st.button("🥤 מים"):
        st.session_state.water = cap(st.session_state.water + 15)

with d2:
    if st.button("🧪 שיקוי קסם"):
        st.session_state.water = cap(st.session_state.water + 10)
        st.session_state.food = cap(st.session_state.food + 10)
        st.session_state.happy = cap(st.session_state.happy + 10)

st.write("---")

# --- TOYS ---
st.write("## 🎮 צעצועים")
t1, t2, t3 = st.columns(3)

with t1:
    if st.button("⚽ כדור"):
        st.session_state.happy = cap(st.session_state.happy + 8)

with t2:
    if st.button("🧸 דובי"):
        st.session_state.happy = cap(st.session_state.happy + 12)

with t3:
    if st.button("🌈 קשת"):
        st.session_state.happy = cap(st.session_state.happy + 15)

st.markdown("</div>", unsafe_allow_html=True)
