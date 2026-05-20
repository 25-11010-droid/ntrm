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
    # (반도체공학과용 비선형 가속도 수식 반영: 현재 저항의 10%씩 감소)
    if st.button("🔴 전기 자극 주기 (Apply Pulse)", use_container_width=True):
        decrease_value = st.session_state.resistance * 0.1
        st.session_state.resistance -= decrease_value
        if st.session_state.resistance < 10.0:
            st.session_state.resistance = 10.0  # 최소 저항 한계선 설정
            
    st.markdown("---")
    st.header("🔬 가상 시냅스 소자 상태")
    
    # [핵심 로직 2] 가중치(전도도) 계산 및 시각화
    # 전도도(Conductance)는 저항의 역수 (G = 1 / R)
    conductance = 1 / st.session_state.resistance
    
    # 저항 수치에 따라 동그라미(시냅스)의 색상 진하기(Alpha값)를 결정 (0.1 ~ 1.0)
    alpha = min(max((100.0 - st.session_state.resistance) / 90.0, 0.1), 1.0)
    
    # HTML/CSS를 활용해 화면에 가상 반도체 소자를 시각화 (오류 수정 완료)
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
        unsafe_allow_html=True  # ⭕ 정상 작동하도록 수정한 옵션 이름
    )

with col2:
    st.header
