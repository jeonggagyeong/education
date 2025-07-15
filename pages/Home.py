# Home.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.cluster.hierarchy import linkage, fcluster
import gower
import folium
from streamlit_folium import folium_static
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
import koreanize_matplotlib

st.set_page_config(page_title="분석 대시보드", layout="wide")
st.title("📊 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("업로드한 데이터 컬럼:", data.columns.tolist())

    data = data.dropna()

    st.subheader("데이터 미리보기")
    st.dataframe(data.head())

    selected_columns = [
        '위도', '경도', '이용인원', '1학년 학급당 학생수', '2학년 학급당 학생수', '3학년 학급당 학생수', '4학년 학급당 학생수', '5학년 학급당 학생수', '6학년 학급당 학생수', '특수학급 학급당 학생수', '다문화자녀수'
    ]

    sample_data = data[selected_columns].copy()
    numeric_data = sample_data.select_dtypes(include=["float64", "int64"])

    

    st.subheader("Gower 거리 기반 계층적 클러스터링")

    @st.cache_data
    def compute_gower_matrix(df):
        matrix = gower.gower_matrix(df)
        return np.nan_to_num(matrix, nan=1.0, posinf=1.0, neginf=1.0)

    distance_matrix = compute_gower_matrix(sample_data)
    linked = linkage(distance_matrix, method='average')

   
    cluster_labels = fcluster(linked, 3,criterion='maxclust')
    data['cluster'] = cluster_labels

    st.write("### 클러스터별 데이터 수")
    st.dataframe(data['cluster'].value_counts())

    # 세션 저장
    st.session_state['clustered_data'] = data
    st.session_state['file_ready'] = True

    # ========== 추가된 기본 EDA 시각화 ==========
    st.subheader("📊 기본 EDA 시각화")

    rename_dict = {
        '이용비율': '돌봄 이용비율',
        '이용인원': '돌봄 이용인원',
        '학생수(계)': '학생수',
        '학급당 학생수(계)': '학급당 학생수',
        '2023_총수입금액(백만원)': '총수입금액(백만원)'
    }
    data = data.rename(columns=rename_dict)

    fig1, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig1.suptitle('돌봄 이용인원 & 이용비율 분포', fontsize=18)
    sns.histplot(data['돌봄 이용인원'], bins=30, kde=True, ax=axes[0, 0])
    axes[0, 0].set_title('이용인원 히스토그램')
    sns.histplot(data['돌봄 이용비율'], bins=30, kde=True, color='powderblue', ax=axes[0, 1])
    axes[0, 1].set_title('이용비율 히스토그램')
    sns.boxplot(x=data['돌봄 이용인원'], ax=axes[1, 0])
    axes[1, 0].set_title('이용인원 박스플랏')
    sns.boxplot(x=data['돌봄 이용비율'], color='powderblue', ax=axes[1, 1])
    axes[1, 1].set_title('이용비율 박스플랏')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    st.pyplot(fig1)

    fig2 = plt.figure(figsize=(8, 5))
    sns.histplot(data['학생수'], bins=30, kde=True, color='royalblue')
    plt.title('학생수 히스토그램')
    plt.xlabel('학생수')
    plt.ylabel('학교 수')
    st.pyplot(fig2)

   
    st.success("✅ 군집분석과 기본 EDA가 완료되었습니다.")

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
