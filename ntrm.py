import streamlit as st
import time
import numpy as np
import pandas as pd

# 1. 앱 페이지 기본 설정
st.set_page_config(page_title="뉴로모픽 멤리스터 시뮬레이터", layout="wide")

st.title("🧠 차세대 인공지능 반도체: 뉴로모픽 멤리스터(Memristor) 시뮬레이터")
st.write("실제 하드웨어 없이 수식을 기반으로 차세대 반도체 소자의 전도도 변형(학습 및 망각)을 실시간 스트리밍으로 관찰합니다.")

st.markdown("---")

# 2. 세션 상태(Session State) 초기화 - 데이터 유지를 위함
if "resistance" not in st.session_state:
    st.session_state.resistance = 100.0  # 초기 저항값 (Ohm)
if "history" not in st.session_state:
    st.session_state.history = []  # 실시간 저항 변화 기록을 저장할 리스트

# 3. 레이아웃 쪼개기 (왼쪽: 제어 및 소자 상태 / 오른쪽: 실시간 스트리밍 그래프)
col1, col2 = st.columns([1, 2])

with col1:
    st.header("⚡ 가상 전기 자극 제어")
    st.write("버튼을 누르면 반도체 소자에 전기 펄스(Pulse) 자극이 가해집니다.")
    
    # [핵심 로직 1] 전기 자극(학습) 버튼
    # 버튼을 누르면 저항이 감소(전도도 증가)하여 정보를 저장하는 상태가 됨
    if st.button("🔴 전기 자극 주기 (Apply Pulse)", use_container_width=True):
        st.session_state.resistance -= 8.0  # 자극 시 저항 감소
        if st.session_state.resistance < 10.0:
            st.session_state.resistance = 10.0  # 최소 저항 한계선 설정
            
    st.markdown("---")
    st.header("🔬 가상 시냅스 소자 상태")
    
    # [핵심 로직 2] 가중치(전도도) 계산 및 시각화
    # 전도도(Conductance)는 저항의 역수 (G = 1 / R)
    conductance = 1 / st.session_state.resistance
    
    # 저항 수치에 따라 동그라미(시냅스)의 색상 진하기(Alpha값)를 결정 (0.1 ~ 1.0)
    alpha = min(max((100.0 - st.session_state.resistance) / 90.0, 0.1), 1.0)
    
    # HTML/CSS를 활용해 화면에 가상 반도체 소자를 시각화
    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; 
                    background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
            <p style="margin: 0; font-weight: bold; color: #333;">가상 뉴로모픽 시냅스 소자</p>
            <div style="width: 100px; height: 100px; border-radius: 50%; 
                        background-color: rgba(255, 75, 75, {alpha}); 
                        margin: 20px 0; border: 2px solid #ff4b4b;
                        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);"></div>
            <p style="margin: 0; font-size: 18px; font-weight: bold; color: #111;">현재 저항: {st.session_state.resistance:.1f} Ω</p>
            <p style="margin: 0; font-size: 14px; color: #666;">전도도(학습 강도): {conductance*1000:.2f} mS</p>
        </div>
        """,
        unsafe_style_allowed=True
    )

with col2:
    st.header("📈 실시간 데이터 스트리밍 (Data Streaming)")
    
    # 실시간으로 변하는 저항 데이터를 저장
    st.session_state.history.append(st.session_state.resistance)
    
    # 데이터가 너무 길어지면 최근 50개만 보여주도록 유지
    if len(st.session_state.history) > 50:
        st.session_state.history.pop(0)
        
    # 라인 차트(그래프)로 실시간 스트리밍 시각화
    chart_data = pd.DataFrame(st.session_state.history, columns=["Resistance (Ω)"])
    st.line_chart(chart_data, y="Resistance (Ω)", use_container_width=True)

# 4. [핵심 로직 3] 가상 망각(Forget) 시스템 기능 및 화면 강제 새로고침(Streaming)
# 버튼을 누르지 않고 시간이 흐르면 뇌의 망각처럼 저항이 다시 초기 상태(100)로 서서히 복귀함
time.sleep(0.3)  # 0.3초마다 데이터 스트리밍 흐름 생성

if st.session_state.resistance < 100.0:
    st.session_state.resistance += 1.2  # 0.3초마다 저항이 1.2씩 증가 (자연 망각 수식)
    if st.session_state.resistance > 100.0:
        st.session_state.resistance = 100.0

# 화면을 강제로 새로고침하여 무한 스트리밍 루프를 만듦
st.rerun()
