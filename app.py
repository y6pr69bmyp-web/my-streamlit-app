import streamlit as st
import random
from datetime import datetime
import requests

# ✅ 너 Apps Script 웹앱 URL
API_URL = "https://script.google.com/macros/s/AKfycbz8EDZ6Oif1SH0kVxAwjJQR7u_I0kj0ODjY7oxTzN_Cf79urVBRODxjGdiYy1GS67-j/exec"

st.set_page_config(page_title="Princess Arcade 💖", page_icon="👑", layout="centered")

# ----------------- Style -----------------
st.markdown("""
<style>
    .title {font-size: 36px; font-weight: 900; letter-spacing: -0.6px; margin-bottom: 2px;}
    .sub {color: rgba(0,0,0,0.55); font-size: 14px; margin-bottom: 14px;}
    .card {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(255, 105, 180, 0.22);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.07);
        backdrop-filter: blur(8px);
        margin: 10px 0 14px 0;
    }
    .chip {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(255, 77, 166, 0.10);
        border: 1px solid rgba(255, 77, 166, 0.22);
        font-size: 12px;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Session init -----------------
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if "tries" not in st.session_state:
    st.session_state.tries = 0
if "rps_score" not in st.session_state:
    st.session_state.rps_score = {"win": 0, "lose": 0, "draw": 0}

# ----------------- Sidebar -----------------
with st.sidebar:
    st.header("🎀 설정")
    theme = st.radio("테마", ["핑크 공주", "밤하늘", "민트"], index=0)
    effect = st.selectbox("효과", ["없음", "풍선 🎈", "눈 ❄️"], index=0)

    st.divider()
    st.header("🕹️ 메뉴")
    page = st.radio("이동", ["홈", "방명록", "게임: 숫자 맞추기", "게임: 가위바위보", "게임: 행운 룰렛"], index=0)

# ----------------- Theme backgrounds -----------------
if theme == "핑크 공주":
    st.markdown("""<style>
        [data-testid="stAppViewContainer"]{
            background: radial-gradient(circle at 20% 20%, rgba(255,182,193,0.60), transparent 42%),
                        radial-gradient(circle at 80% 10%, rgba(255,105,180,0.35), transparent 48%),
                        linear-gradient(180deg, #fff7fb 0%, #ffffff 60%);
        }
    </style>""", unsafe_allow_html=True)
elif theme == "밤하늘":
    st.markdown("""<style>
        [data-testid="stAppViewContainer"]{
            background: radial-gradient(circle at 20% 20%, rgba(120,140,255,0.25), transparent 45%),
                        radial-gradient(circle at 80% 10%, rgba(255,105,180,0.18), transparent 45%),
                        linear-gradient(180deg, #0b1020 0%, #101a33 60%);
        }
        .title, .sub, label, p, span, div { color: rgba(255,255,255,0.92) !important; }
        .card { background: rgba(255,255,255,0.08) !important; border-color: rgba(255,255,255,0.12) !important; }
    </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
        [data-testid="stAppViewContainer"]{
            background: radial-gradient(circle at 20% 20%, rgba(152,251,200,0.50), transparent 45%),
                        radial-gradient(circle at 80% 10%, rgba(255,105,180,0.18), transparent 45%),
                        linear-gradient(180deg, #f6fffb 0%, #ffffff 60%);
        }
    </style>""", unsafe_allow_html=True)

# ----------------- Header -----------------
st.markdown('<div class="title">👑 Princess Arcade <span style="color:#ff4da6;">웹사이트</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sub">방명록 + 미니게임 3종 · 윈도우/모바일 공유 OK ✨</div>', unsafe_allow_html=True)
st.markdown('<span class="chip">Streamlit</span><span class="chip">Cute UI</span><span class="chip">Mini Games</span>', unsafe_allow_html=True)

# ----------------- Effect helper -----------------
def do_effect():
    if effect == "풍선 🎈":
        st.balloons()
    elif effect == "눈 ❄️":
        st.snow()

# ----------------- Pages -----------------
if page == "홈":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 💖 환영해!")
    st.write("- 왼쪽 메뉴에서 방명록이랑 게임을 골라서 놀 수 있어.")
    st.write("- 주현준 바봉봉ㅋㅋ")
    st.write("- 신기하제? 누나가 만들었디")
    st.write("#### 오늘의 한마디 ✨")
    msgs = [
        "대체로 행복하시길 바라요 💖",
        "오늘도 잘 살았다고 말해주기 🤍",
        "느려도 괜찮아. 계속 가면 돼 ✨",
        "너는 너라서 충분해 🌸",
        "오늘은 ‘괜찮다’를 더 자주 해보자 🫧",
    ]
    st.info(random.choice(msgs))
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "방명록":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 📝 방명록 (공용 저장 · 새로고침해도 유지)")

    name = st.text_input("닉네임", placeholder="예: 정인/동생/친구")
    msg = st.text_area("남길 말", placeholder="한 줄 남겨줘 💕", height=90)

    col1, col2 = st.columns(2)
    with col1:
        add = st.button("💌 남기기", use_container_width=True)
    with col2:
        refresh = st.button("🔄 새로 불러오기", use_container_width=True)

    # ✅ 글 남기기 (POST)
    if add:
        if name.strip() and msg.strip():
            payload = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "name": name.strip(),
                "message": msg.strip(),
            }

            try:
                res = requests.post(API_URL, json=payload, timeout=10)

                # Apps Script가 {"ok": true} 같은 JSON을 주면 파싱
                try:
                    result = res.json()
                    if result.get("ok") is True:
                        st.success("💖 방명록 저장 완료!")
                        do_effect()
                    else:
                        st.warning(f"⚠️ 응답은 왔는데 형식이 다름: {result}")
                except:
                    # JSON이 아닌 응답이어도 저장 성공할 수 있어서 일단 성공 처리
                    st.success("💖 방명록 저장 완료! (응답 파싱 생략)")
                    do_effect()

            except Exception as e:
                st.error(f"저장 실패: {e}")
        else:
            st.warning("닉네임이랑 메시지를 둘 다 써줘!")

    st.divider()
    st.write("#### 📌 최근 방명록")

    # ✅ 글 불러오기 (GET) - refresh 눌러도 되고, 페이지 들어오면 자동으로도 됨
    try:
        data = requests.get(API_URL, timeout=10).json()

        # data 형태: [["time","name","message"], ["2026-...","정인","..."], ...]
        rows = data[1:] if isinstance(data, list) and len(data) > 0 else []
        rows = rows[::-1]  # 최신이 위로

        if not rows:
            st.caption("아직 아무도 안 남겼어… 첫 손님 가자 🐣")
        else:
            for row in rows[:30]:
                t, n, m = (row + ["", "", ""])[:3]
                st.markdown(f"**{n}** · {t}")
                st.write(m)
                st.markdown("---")

    except Exception as e:
        st.error(f"불러오기 실패: {e}")

    st.caption("※ 방명록은 Google Sheet에 공용 저장돼요. 새로고침해도 유지됩니다 ✨")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "게임: 숫자 맞추기":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 🎯 숫자 맞추기 (1~100)")
    st.caption("힌트: 업/다운. 맞추면 자동으로 새 게임 시작!")

    guess = st.number_input("숫자 입력", min_value=1, max_value=100, step=1, value=50)
    col1, col2 = st.columns(2)
    with col1:
        check = st.button("🔎 확인", use_container_width=True)
    with col2:
        reset = st.button("🔁 새로 뽑기", use_container_width=True)

    if reset:
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.tries = 0
        st.info("새 숫자 뽑았어! 다시 가자 ✨")

    if check:
        st.session_state.tries += 1
        ans = st.session_state.secret_number
        if guess < ans:
            st.warning(f"업 ⬆️ (시도 {st.session_state.tries}번)")
        elif guess > ans:
            st.warning(f"다운 ⬇️ (시도 {st.session_state.tries}번)")
        else:
            st.success(f"정답!! 🎉 {st.session_state.tries}번 만에 맞췄다!")
            do_effect()
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.tries = 0
            st.info("새 게임 시작! (숫자 다시 뽑음)")

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "게임: 가위바위보":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### ✊✌️🖐️ 가위바위보")
    options = ["가위 ✌️", "바위 ✊", "보 🖐️"]
    me = st.selectbox("내 선택", options)
    play = st.button("⚡ 대결!", use_container_width=True)

    if play:
        cpu = random.choice(options)
        st.write(f"너: **{me}**  vs  컴퓨터: **{cpu}**")

        def judge(a, b):
            if a == b:
                return "draw"
            if (a.startswith("가위") and b.startswith("보")) or \
               (a.startswith("바위") and b.startswith("가위")) or \
               (a.startswith("보") and b.startswith("바위")):
                return "win"
            return "lose"

        result = judge(me, cpu)
        if result == "win":
            st.session_state.rps_score["win"] += 1
            st.success("이겼다!!! 💖")
            do_effect()
        elif result == "lose":
            st.session_state.rps_score["lose"] += 1
            st.error("졌어… 다음 판 가자 😤")
        else:
            st.session_state.rps_score["draw"] += 1
            st.info("비겼다! 한 번 더!")

    s = st.session_state.rps_score
    st.caption(f"전적: ✅ {s['win']}승  ❌ {s['lose']}패  ➖ {s['draw']}무")

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "게임: 행운 룰렛":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 🎡 행운 룰렛")
    st.caption("버튼 누르면 오늘의 랜덤 보상/미션이 나와!")

    rewards = [
        "🍓 딸기 보상: 좋아하는 간식 1개 허용",
        "🌸 힐링 보상: 10분 멍때리기",
        "✨ 미션: 물 한 컵 마시기",
        "🎀 미션: 스트레칭 2분",
        "👑 보상: 나 자신 칭찬 3개 쓰기",
        "🫧 미션: 책상 위 3개만 치우기",
        "🎶 보상: 최애 노래 1곡 크게 듣기",
        "😈 미션: 안 미룸—지금 5분만 하기",
    ]

    if st.button("SPIN 💖", use_container_width=True):
        pick = random.choice(rewards)
        st.success(pick)
        do_effect()

    st.markdown('</div>', unsafe_allow_html=True)
