import streamlit as st

st.set_page_config(page_title="Pizza Maker", page_icon="🍕")

st.title("🍕 הכנת פיצה Streamlit")

st.write("בחר את כל מה שאתה רוצה בפיצה שלך:")

size = st.selectbox(
    "גודל הפיצה:",
    ["קטן", "בינוני", "גדול"]
)

toppings = st.multiselect(
    "תוספות:",
    ["זיתים", "פטריות", "בצל", "תירס", "גבינה נוספת", "ביצת עין", "אננס", "טונה", "פפרוני"]
)

extra_cheese = st.checkbox("🧀 להוסיף עוד גבינה?")

# חישוב מחיר בסיסי
price = 20

if size == "בינוני":
    price += 10
elif size == "גדול":
    price += 20

price += len(toppings) * 3

if extra_cheese:
    price += 5

st.write("---")
st.write("### 🍽️ סיכום ההזמנה שלך:")

st.write(f"**גודל:** {size}")
st.write(f"**תוספות:** {', '.join(toppings) if toppings else 'ללא'}")
st.write(f"**תוספת גבינה:** {'כן' if extra_cheese else 'לא'}")

st.write(f"### 💰 מחיר סופי: **₪{price}**")

if st.button("הכין פיצה!"):
    st.success("🍕 הפיצה שלך מוכנה! בתיאבון 😄")
