import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import time
from datetime import datetime

st.title("this is my :blue[page] :sunglasses:")
st.write("Hello World!")
st.write("Goodbye Moon!")
# We need a streaming object for this to work
# st.write_stream("Where are you Mars?!")

st.markdown("""
## Hello
- This
- Is
- Magic Formating!
""")
st.header("Column", divider=True)


df = pd.DataFrame({'col1': [1,2,3,4,5,6,7,8,9,10]})
st.write(df)

st.subheader("Graphic ", divider="blue")



arr = np.random.normal(2, 2, size=200)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.write(fig)

st.subheader("Functions ", divider="blue")
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language="python")

code = '''def calcul():
    A=5
    B=7
    result= A+B
    print(result)'''
st.code(code, language="python")

st.subheader(" PC Temperature ", divider="blue")
col1, col2, col3 = st.columns(3)
col1.metric(label=" CPU Temperature", value="39°", delta="1.2 °F")
col2.metric(label=" GPU Temperature", value="45°", delta="0 °F")
col3.metric(label=" PC Temperature", value="50°", delta="-1.5 °F")

st.subheader("Best food", divider="blue")
df = pd.DataFrame(
    [
        {"command": "burger", "rating": 4, "is_widget": True},
        {"command": "pizza", "rating": 5, "is_widget": False},
        {"command": "pasta", "rating": 3, "is_widget": True},
    ]
)
edited_df = st.data_editor(
    df,
    column_config={
        "command": "best food",
        "rating": st.column_config.NumberColumn(
            "Your rating",
            help="How much do you like this food (1-5)?",
            min_value=1,
            max_value=5,
            step=1,
            format="%d ⭐",
        ),
        "is_widget": "Widget ?",
    },
    disabled=["command", "is_widget"],
    hide_index=True,
)

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite food is **{favorite_command}** 🎈")

st.subheader("best restaurant in Brussels", divider="blue")


df = pd.DataFrame(
    np.random.randn(200, 2) / [50, 50] + [50.85 , 4.35],
    columns=["lat", "lon"],
)
st.map(df)

st.subheader("Audio recorder", divider="blue")

audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)

st.subheader("Camera capture", divider="blue")
enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture)


st.subheader("Slider", divider="blue")
age = st.slider("How old are you?", 0, 100, 15)
st.write("I'm ", age, "years old")

values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
st.write("Values:", values)



appointment = st.slider(
    "Schedule your appointment:", value=(time(11, 30), time(12, 45))
)
st.write("You're scheduled for:", appointment)


start_time = st.slider(
    "When do you start?",
    value=datetime(2025, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm",
)
st.write("Start time:", start_time)

st.subheader("Chat", divider="blue")
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")