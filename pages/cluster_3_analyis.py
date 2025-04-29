# cluster_3_analysis.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import koreanize_matplotlib

st.set_page_config(page_title="클러스터 1, 2, 3 전체 분석", layout="wide")
st.title("📊 클러스터 1, 2, 3 전체 분석")

# 데이터 불러오기
if 'clustered_data' not in st.session_state:
    st.warning("먼저 분석 대시보드에서 데이터를 업로드하고 군집 분석을 수행해주세요.")
    st.stop()

df = st.session_state['clustered_data'].copy()

# 컬럼명 변경
rename_dict = {
    '이용비율': '돌봄 이용비율',
    '이용인원': '돌봄 이용인원',
    '학생수(계)': '학생수',
    '학급당 학생수(계)': '학급당 학생수',
    '2023_총수입금액(백만원)': '총수입금액(백만원)'
}
df = df.rename(columns=rename_dict)

# 클러스터 비율 파이차트
st.subheader("📌 클러스터별 분포 비율")
cluster_counts = df.groupby('cluster')['시군구'].count().reset_index()

colors = ['dodgerblue', 'royalblue', 'deepskyblue']

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return '{:.1f}%\n({:d}\uac1c)'.format(pct, count)
    return my_autopct

fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.pie(
    cluster_counts['시군구'],
    labels=cluster_counts['cluster'],
    autopct=make_autopct(cluster_counts['시군구']),
    startangle=90,
    colors=colors
)
ax1.axis('equal')
ax1.set_title('클러스터별 개수 및 비율')
st.pyplot(fig1)

# 클러스터별 기초통계량
st.subheader("📊 클러스터별 주요 변수 기초통계량")
summary = df.groupby('cluster')[
    ['학생수', '교사수', '다문화자녀수', '총수입금액(백만원)']
].agg(['mean', 'median', 'min', 'max'])
st.dataframe(summary)

# 박스플롯
st.subheader("📦 주요 변수의 클러스터별 분포 (Boxplot)")
variables = ['돌봄 이용비율', '돌봄 이용인원', '학생수', '교지면적(m)']
fig2, axes2 = plt.subplots(1, 4, figsize=(20, 5))
for ax, var in zip(axes2, variables):
    sns.boxplot(data=df, x='cluster', y=var, ax=ax, color='cornflowerblue')
    ax.set_title(f'{var}', fontsize=12)
    ax.set_xlabel('Cluster')
    ax.set_ylabel(var)
plt.tight_layout()
st.pyplot(fig2)

# 히스토그램
st.subheader("📈 주요 변수의 전체 분포 (히스토그램)")
hist_cols = ['돌봄 이용인원', '돌봄 이용비율', '학생수', '총수입금액(백만원)']
fig3, axes3 = plt.subplots(1, 4, figsize=(22, 4))
for i, col in enumerate(hist_cols):
    sns.histplot(data=df, x=col, hue='cluster', ax=axes3[i], kde=True, palette='Blues')
    axes3[i].set_title(f'{col} 분포')
    axes3[i].set_xlabel(col)
    axes3[i].set_ylabel('빈도')
plt.tight_layout()
st.pyplot(fig3)

# 시도별 히트맵용 테이블 생성
st.subheader("🗺️ 시도별 클러스터 분포 지도")
df_cluster = df.pivot_table(index='시도교육청', columns='cluster', aggfunc='size', fill_value=0).reset_index()
df_cluster['시도'] = df_cluster['시도교육청'].str.replace('교육청', '', regex=False)

# 시도 행정구역 지도 데이터
try:
    gdf = gpd.read_file(r"C:\Users\jeong\education\skorea-provinces-geo.json")
    eng_to_kor = {
        'Seoul': '서울특별시',
        'Busan': '부산광역시',
        'Daegu': '대구광역시',
        'Incheon': '인천광역시',
        'Gwangju': '광주광역시',
        'Daejeon': '대전광역시',
        'Ulsan': '울산광역시',
        'Gyeonggi-do': '경기도',
        'Gangwon-do': '강원특별자치도',
        'Chungcheongbuk-do': '충청북도',
        'Chungcheongnam-do': '충청남도',
        'Jeollabuk-do': '전북특별자치도',
        'Jeollanam-do': '전라남도',
        'Gyeongsangbuk-do': '경상북도',
        'Gyeongsangnam-do': '경상남도',
        'Jeju-do': '제주특별자치도'
    }
    gdf['시도'] = gdf['NAME_1'].map(eng_to_kor)
    merged = gdf.merge(df_cluster, on='시도')

    fig4, axes4 = plt.subplots(1, 3, figsize=(24, 8))
    for idx, cluster_num in enumerate([1, 2, 3]):
        merged.plot(
            column=cluster_num,
            cmap='Blues',
            linewidth=0.8,
            ax=axes4[idx],
            edgecolor='0.8',
            legend=True
        )
        axes4[idx].set_title(f'클러스터 {cluster_num}', fontsize=15)
        axes4[idx].axis('off')

    plt.tight_layout()
    st.pyplot(fig4)
except Exception as e:
    st.warning("지도를 불러오는 데 문제가 발생했습니다. GeoJSON 파일이 누락되었거나 경로가 잘못되었을 수 있습니다.")
    st.error(str(e))