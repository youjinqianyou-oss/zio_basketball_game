import streamlit as st
import random
import time

st.set_page_config(page_title="高級反應力競技", layout="centered")

GRID = 9
GAME_TIME = 30

# ===== 初始化 =====
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.start_time = time.time()
    st.session_state.target = random.randint(0, GRID - 1)
    st.session_state.trap = random.randint(0, GRID - 1)
    st.session_state.last_move = time.time()

# ===== 時間 =====
elapsed = int(time.time() - st.session_state.start_time)
time_left = GAME_TIME - elapsed

# ===== 動態難度（速度）=====
speed = max(0.6, 1.6 - elapsed * 0.04)

# ===== 自動換位 =====
if time.time() - st.session_state.last_move > speed:
    st.session_state.target = random.randint(0, GRID - 1)
    st.session_state.trap = random.randint(0, GRID - 1)
    st.session_state.last_move = time.time()

st.title("⚡ 高級反應力競技場")

if time_left <= 0:
    st.subheader("🏁 遊戲結束")
    st.write(f"🎯 分數：**{st.session_state.score}**")
    st.write(f"🔥 最高 Combo：**{st.session_state.combo}**")

    if st.button("🔁 再挑戰一次"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()

    st.stop()

# ===== 狀態顯示 =====
st.progress(time_left / GAME_TIME)
st.write(f"⏱️ {time_left}s | ⭐ 分數：{st.session_state.score} | 🔥 Combo：{st.session_state.combo}")

# ===== 地圖 =====
cols = st.columns(3)

for i in range(GRID):
    with cols[i % 3]:
        if i == st.session_state.target:
            if st.button("🐹", key=f"m{i}"):
                st.session_state.score += 1
                st.session_state.combo += 1
                st.session_state.target = random.randint(0, GRID - 1)
        elif i == st.session_state.trap:
            if st.button("💣", key=f"t{i}"):
                st.session_state.score -= 2
                st.session_state.combo = 0
                st.session_state.trap = random.randint(0, GRID - 1)
        else:
            st.button("⬜", key=f"e{i}")

st.caption("⚠️ 假地鼠會扣分，小心！")
