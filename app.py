import streamlit as st

st.set_page_config(
    page_title="인사 웹앱",
    page_icon="💖",
    layout="centered",
)

st.title("내 첫 웹앱 💖")
st.caption("이 링크는 윈도우/모바일에서도 열려요!")

with st.sidebar:
    st.header("설정")
    emoji = st.selectbox("이모지 선택", ["👋", "💖", "✨", "🐣", "🦊"])

name = st.text_input("이름을 입력하세요", placeholder="예: 정인")

if st.button("인사하기"):
    if name.strip():
        st.success(f"{name} 안녕! {emoji}")
    else:
        st.warning("이름을 먼저 입력해줘!")
