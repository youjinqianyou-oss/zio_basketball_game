import streamlit as st
from PIL import Image, ImageDraw
import time
import math
from random import uniform

st.set_page_config(page_title="迷你 3D NBA 高級版", layout="centered")
st.title("🏀 迷你 3D NBA 高級版：能力值系統")

# 上傳玩家和 AI 臉
player_face = st.file_uploader("上傳玩家臉", type=["png","jpg"])
ai_face = st.file_uploader("上傳 AI 臉", type=["png","jpg"])

# 初始化
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = [100, 300]
if 'teammate_pos' not in st.session_state:
    st.session_state.teammate_pos = [200, 300]
if 'ai_pos' not in st.session_state:
    st.session_state.ai_pos = [150, 80]
if 'ball_pos' not in st.session_state:
    st.session_state.ball_pos = st.session_state.player_pos.copy()
if 'ball_owner' not in st.session_state:
    st.session_state.ball_owner = 'player'
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'ai_score' not in st.session_state:
    st.session_state.ai_score = 0

# 初始化球員能力值
if 'player_stats' not in st.session_state:
    st.session_state.player_stats = {"shoot": 80, "pass": 70, "speed": 15}
if 'teammate_stats' not in st.session_state:
    st.session_state.teammate_stats = {"shoot": 75, "pass": 80, "speed": 12}
if 'ai_stats' not in st.session_state:
    st.session_state.ai_stats = {"shoot": 75, "pass": 70, "speed": 14}

width, height = 300, 400

# 畫球場
def draw_court():
    img = Image.new("RGB", (width, height), "green")
    draw = ImageDraw.Draw(img)
    draw.rectangle([140, 30, 160, 50], fill="orange")
    
    # 玩家
    draw.ellipse([st.session_state.player_pos[0]-15, st.session_state.player_pos[1]-15,
                  st.session_state.player_pos[0]+15, st.session_state.player_pos[1]+15], fill="blue")
    if player_face:
        face_img = Image.open(player_face).resize((20,20))
        img.paste(face_img, (st.session_state.player_pos[0]-10, st.session_state.player_pos[1]-30), mask=face_img.convert("RGBA"))
    
    # 隊友
    draw.ellipse([st.session_state.teammate_pos[0]-15, st.session_state.teammate_pos[1]-15,
                  st.session_state.teammate_pos[0]+15, st.session_state.teammate_pos[1]+15], fill="cyan")
    
    # AI
    draw.ellipse([st.session_state.ai_pos[0]-15, st.session_state.ai_pos[1]-15,
                  st.session_state.ai_pos[0]+15, st.session_state.ai_pos[1]+15], fill="red")
    if ai_face:
        ai_img = Image.open(ai_face).resize((20,20))
        img.paste(ai_img, (st.session_state.ai_pos[0]-10, st.session_state.ai_pos[1]-30), mask=ai_img.convert("RGBA"))
    
    # 球
    draw.ellipse([st.session_state.ball_pos[0]-7, st.session_state.ball_pos[1]-7,
                  st.session_state.ball_pos[0]+7, st.session_state.ball_pos[1]+7], fill="orange")
    return img

# 投籃函數（能力值影響成功率）
def shoot_ball(from_pos, stats):
    end_x, end_y = 150, 40
    steps = 20
    for t in range(steps+1):
        x = from_pos[0] + (end_x - from_pos[0]) * t/steps
        y = from_pos[1] + (end_y - from_pos[1]) * t/steps - 50 * math.sin(math.pi * t/steps)**2
        st.session_state.ball_pos = [x, y]
        st.image(draw_court(), width=300)
        time.sleep(0.03)
    # 成功率 = 投籃能力/100
    return uniform(0, 1) < stats["shoot"]/100

# 傳球函數（能力值影響成功率）
def pass_ball(from_pos, to_pos, stats):
    steps = 15
    for t in range(steps+1):
        x = from_pos[0] + (to_pos[0] - from_pos[0]) * t/steps
        y = from_pos[1] + (to_pos[1] - from_pos[1]) * t/steps
        st.session_state.ball_pos = [x, y]
        st.image(draw_court(), width=300)
        time.sleep(0.02)
    return uniform(0,1) < stats["pass"]/100

# 球員左右移動
col1, col2, col3 = st.columns(3)
if col1.button("←"):
    st.session_state.player_pos[0] -= st.session_state.player_stats["speed"]
if col3.button("→"):
    st.session_state.player_pos[0] += st.session_state.player_stats["speed"]
st.session_state.player_pos[0] = max(20, min(width-20, st.session_state.player_pos[0]))

# 玩家操作
st.subheader("操作選擇")
col_a, col_b, col_c = st.columns(3)
if col_a.button("投籃") and st.session_state.ball_owner=='player':
    if shoot_ball(st.session_state.player_pos, st.session_state.player_stats):
        st.session_state.player_score += 2
        st.success("你進球！+2分")
    else:
        st.error("投籃失敗！")
    st.session_state.ball_owner = 'ai'
if col_b.button("傳給隊友") and st.session_state.ball_owner=='player':
    if pass_ball(st.session_state.player_pos, st.session_state.teammate_pos, st.session_state.player_stats):
        st.success("傳球成功")
        st.session_state.ball_owner='teammate'
    else:
        st.error("傳球失敗！球權給 AI")
        st.session_state.ball_owner='ai'
if col_c.button("隊友投籃") and st.session_state.ball_owner=='teammate':
    if shoot_ball(st.session_state.teammate_pos, st.session_state.teammate_stats):
        st.session_state.player_score += 2
        st.success("隊友進球！+2分")
    else:
        st.error("隊友投籃失敗！")
    st.session_state.ball_owner='ai'

# AI 回合
if st.session_state.ball_owner=='ai':
    time.sleep(0.3)
    if shoot_ball(st.session_state.ai_pos, st.session_state.ai_stats):
        st.session_state.ai_score += 2
        st.info("AI 進球！+2分")
    else:
        st.warning("AI 投籃失敗！")
    st.session_state.ball_owner='player'
    st.session_state.ball_pos = st.session_state.player_pos.copy()

# 顯示比分和能力值
st.write(f"你的分數：{st.session_state.player_score} | AI 分數：{st.session_state.ai_score}")
st.write(f"你的能力值：投籃 {st.session_state.player_stats['shoot']} | 傳球 {st.session_state.player_stats['pass']} | 速度 {st.session_state.player_stats['speed']}")

# 畫球場
st.image(draw_court(), width=300)
