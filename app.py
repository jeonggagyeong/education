import streamlit as st
import pandas as pd

st.set_page_config(page_title="클러스터 선택", layout="wide")
st.title("클러스터 탐색")

# 사전 조건 확인
if 'file_ready' not in st.session_state or not st.session_state['file_ready']:
    st.warning("먼저 'Home'에서 CSV 업로드 및 군집분석을 완료해주세요.")
    st.stop()

# 데이터 불러오기
data = st.session_state['clustered_data']
cluster_list = ["1","2와3 비교","1,2,3 한 눈에 보기"]

# 클러스터 선택
selected_cluster = st.selectbox("클러스터 번호를 선택하세요", cluster_list)

# 보기 방식 선택
view_option = st.radio("어떤 정보를 보시겠어요?", ["클러스터별 분석 보기"], horizontal=True)

# 실행 버튼
if st.button("🔍 선택한 클러스터 보기"):
    st.session_state['selected_cluster'] = selected_cluster


    if view_option == "클러스터별 분석 보기":
        if selected_cluster == "1":
            st.switch_page("pages/cluster_1_analysis.py")
        elif selected_cluster == "2와3 비교":
            st.switch_page("pages/cluster_2_analysis.py")
        elif selected_cluster == "1,2,3 한 눈에 보기":
            st.switch_page("pages/cluster_3_analysis.py")
        else:
            st.error("선택한 클러스터에 대한 분석 페이지가 존재하지 않습니다.")
