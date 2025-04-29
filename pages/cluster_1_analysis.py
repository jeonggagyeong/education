import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

st.set_page_config(page_title="클러스터 1 분석", layout="wide")
st.title("클러스터 1 상세 분석")

# 데이터 불러오기
data = st.session_state.get('clustered_data')
if data is None:
    st.error("먼저 분석대시보드에서 클러스터링을 수행해주세요.")
    st.stop()

# 컬럼명 정리
rename_dict = {
    '이용비율': '돌봄 이용비율',
    '이용인원': '돌봄 이용인원',
    '학생수(계)': '학생수',
    '학급당 학생수(계)': '학급당 학생수',
    '2023_총수입금액(백만원)': '총수입금액(백만원)'
}
df = data.rename(columns=rename_dict)

# 클러스터 1 필터링
df_cluster1 = df[df['cluster'] == 1]

# 주요 컬럼 설정
important_columns = [
    '학생수', '돌봄 이용비율', '돌봄 이용인원', '교사수',
    '수업교원 1인당 학생수', '다문화자녀수', '총수입금액(백만원)'
]

# 히스토그램 시각화
st.subheader("클러스터 1 변수별 분포")
fig, axes = plt.subplots(2, 4, figsize=(22, 12))
fig.suptitle('클러스터 1의 변수별 분포', fontsize=24)
axes = axes.flatten()

for idx, col in enumerate(important_columns):
    axes[idx].hist(df_cluster1[col].dropna(), bins=30, edgecolor='black', color='royalblue', alpha=0.8)
    axes[idx].set_title(f'{col} 분포', fontsize=14)
    axes[idx].set_xlabel(col)
    axes[idx].set_ylabel('Count')
    axes[idx].grid(True, linestyle='--', alpha=0.5)
if len(important_columns) < len(axes):
    fig.delaxes(axes[-1])
plt.tight_layout(rect=[0, 0, 1, 0.95])
st.pyplot(fig)

# 돌봄 이용비율 100% 필터
st.subheader("이용비율 100%인 학교들의 특성")
df_cluster1_full = df_cluster1[df_cluster1['돌봄 이용비율'] == 1.0].drop(['돌봄 이용비율'], axis=1)
important_columns_100 = ['학생수', '돌봄 이용인원', '교사수', '수업교원 1인당 학생수', '다문화자녀수', '총수입금액(백만원)']
fig2, axes2 = plt.subplots(2, 3, figsize=(22, 12))
fig2.suptitle('클러스터 1 & 이용비율 100% 지역 변수 분포', fontsize=24)
axes2 = axes2.flatten()

for idx, col in enumerate(important_columns_100):
    axes2[idx].hist(df_cluster1_full[col].dropna(), bins=30, edgecolor='black', color='steelblue', alpha=0.8)
    axes2[idx].set_title(f'{col} 분포', fontsize=14)
    axes2[idx].set_xlabel(col)
    axes2[idx].set_ylabel('Count')
    axes2[idx].grid(True, linestyle='--', alpha=0.5)
if len(important_columns_100) < len(axes2):
    for j in range(len(important_columns_100), len(axes2)):
        fig2.delaxes(axes2[j])
plt.tight_layout(rect=[0, 0, 1, 0.95])
st.pyplot(fig2)

# 평균 비교 막대그래프
st.subheader("이용비율 100% vs <100% 평균 비교")
df_partial = df_cluster1[df_cluster1['돌봄 이용비율'] != 1.0]
full_means = df_cluster1_full[important_columns_100].mean()
partial_means = df_partial[important_columns_100].mean()
fig3, axes3 = plt.subplots(2, 3, figsize=(20, 12))
fig3.suptitle('클러스터 1 - 이용비율 100%와 이하 비교', fontsize=24)
axes3 = axes3.flatten()

for idx, col in enumerate(important_columns_100):
    axes3[idx].bar(['100%', '<100%'], [full_means[col], partial_means[col]], color=['cornflowerblue', 'midnightblue'])
    axes3[idx].set_title(f'{col} 평균 비교', fontsize=14)
    axes3[idx].set_ylabel(col)
    axes3[idx].grid(axis='y')
if len(important_columns_100) < len(axes3):
    for j in range(len(important_columns_100), len(axes3)):
        fig3.delaxes(axes3[j])
plt.tight_layout()
st.pyplot(fig3)

# 시도교육청별 학교 수 시각화
st.subheader("이용비율 100%인 학교 - 시도교육청별 분포")
sido_count = df_cluster1_full['시도교육청'].value_counts().sort_values(ascending=False)
fig4, ax4 = plt.subplots(figsize=(12, 6))
sido_count.plot(kind='bar', ax=ax4, edgecolor='black', color='skyblue')
ax4.set_title('시도교육청별 학교 수')
ax4.set_xlabel('시도교육청')
ax4.set_ylabel('학교 수')
ax4.grid(axis='y')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig4)

# 상위 5개 시도교육청 박스플롯
st.subheader("상위 5개 시도교육청 특성 비교")
top5_sido = df_cluster1_full['시도교육청'].value_counts().nlargest(5).index.tolist()
df_top5 = df_cluster1_full[df_cluster1_full['시도교육청'].isin(top5_sido)]
fig5, axes5 = plt.subplots(2, 3, figsize=(22, 12))
axes5 = axes5.flatten()
for idx, col in enumerate(important_columns_100[:6]):
    sns.boxplot(data=df_top5, x='시도교육청', y=col, ax=axes5[idx])
    axes5[idx].set_title(f'{col} (Top5 시도교육청)', fontsize=14)
    axes5[idx].set_xlabel('시도교육청')
    axes5[idx].set_ylabel(col)
    axes5[idx].grid(True)
plt.tight_layout()
st.pyplot(fig5)
