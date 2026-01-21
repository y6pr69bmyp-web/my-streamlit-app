import streamlit as st

st.title("내 첫 웹앱 💖")

name = st.text_input("이름을 입력하세요")

if st.button("인사하기"):
    if name.strip():
        st.write(f"{name} 안녕! 👋")
    else:
        st.warning("이름을 먼저 입력해줘!")
