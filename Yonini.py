import streamlit as st
import random
import time

st.set_page_config(page_title="Pizza Rush", page_icon="🍕")

st.title("🍕 Pizza Rush – משחק הכנת פיצות!")

# רשימת תוספות
all_toppings = [
    "גבינה", "זיתים", "פטריות", "בצל", "עגבניות",
    "פלפל חריף", "פלפל מתוק", "אננס", "נקניק",
    "תירס", "טונה", "בולגרית"
]

# יצירת הזמנה רנדומלית ללקוח
def generate_order():
    amount = random.randint(2, 5)
    return random.sample(all_toppings, amount)

# שמירה בסשן
if "score" not in st.session_state:
    st.session_state.score = 0
if "order" not in st.session_state:
    st.session_state.order = generate_order()

st.subheader("👨‍🍳 הלקוח מבקש:")
st.info(" | ".join(st.session_state.order))

# בחירת תוספות
selected = st.multiselect("מה אתה שם בפיצה?", all_toppings)

# התחלת טיימר
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

time_left = 15 - int(time.time() - st.session_state.start_time)
st.write(f"⏱️ זמן שנותר: **{max(time_left, 0)} שניות**")

# בדיקה ולחיצה
if st.button("מוכן!"):
    if time_left <= 0:
        st.error("⏰ נגמר הזמן! הלקוח כועס 😡")
    else:
        if set(selected) == set(st.session_state.order):
            st.success("🔥 בול מה שהלקוח רצה! +10 נקודות")
            st.session_state.score += 10
        else:
            st.error("😡 טעית בתוספות! -5 נקודות")
            st.session_state.score -= 5

    # הזמנה חדשה + אתחול זמן
    st.session_state.order = generate_order()
    st.session_state.start_time = time.time()

st.write(f"💰 ניקוד: **{st.session_state.score}**")

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg",
    width=250
)
