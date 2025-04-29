import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler
from scipy.stats import ttest_ind
import koreanize_matplotlib

st.set_page_config(page_title="클러스터 2 vs 3 비교 분석", layout="wide")
st.title("클러스터 2 vs 3 상세 비교 분석")

# 세션에서 데이터 불러오기
data = st.session_state.get('clustered_data')
if data is None:
    st.error("먼저 분석 대시보드에서 클러스터링을 수행해주세요.")
    st.stop()

# 컬럼명 변경
rename_dict = {
    '이용비율': '돌봄 이용비율',
    '이용인원': '돌봄 이용인원',
    '학생수(계)': '학생수',
    '학급당 학생수(계)': '학급당 학생수',
    '2023_총수입금액(백만원)': '총수입금액(백만원)'
}
df = data.rename(columns=rename_dict)

# 클러스터별 필터링
df_cluster2 = df[df['cluster'] == 2]
df_cluster3 = df[df['cluster'] == 3]

# 주요 변수 목록
important_columns = [
    '학생수', '돌봄 이용인원', '돌봄 이용비율',
    '교사수', '수업교원 1인당 학생수', '다문화자녀수', '총수입금액(백만원)'
]

# ----------------------------
# T-test 분석
st.subheader("클러스터 2 vs 3: 주요 변수에 대한 t-test")
ttest_results = {}
for col in important_columns:
    group2 = df_cluster2[col].dropna()
    group3 = df_cluster3[col].dropna()
    t_stat, p_value = ttest_ind(group2, group3, equal_var=False)
    ttest_results[col] = {'t-statistic': t_stat, 'p-value': p_value}

# 결과 테이블 출력
ttest_df = pd.DataFrame(ttest_results).T.round(4)
st.dataframe(ttest_df)

st.markdown("""
**해석 요약**  
- 대부분의 변수에서 p-value < 0.05로 통계적으로 유의한 차이가 있음  
- Cluster 3은 학생수, 교사수, 총수입, 다문화자녀수가 높고,  
- Cluster 2는 돌봄 이용비율이 확연히 높음  
- 교원 1인당 학생수도 Cluster 3이 더 높아 과밀 양상
""")

# ----------------------------
# 로그 + Robust Scaling 바 차트
st.subheader("클러스터 2 vs 3: 변수 비교 (Log + Robust Scaling)")
important_columns_no_income = [
    '학생수', '돌봄 이용인원', '돌봄 이용비율',
    '교사수', '수업교원 1인당 학생수', '다문화자녀수'
]

# 로그 변환 및 스케일링
df_cluster2_log = np.log1p(df_cluster2[important_columns_no_income])
df_cluster3_log = np.log1p(df_cluster3[important_columns_no_income])
scaler = RobustScaler()
df_cluster2_scaled = scaler.fit_transform(df_cluster2_log)
df_cluster3_scaled = scaler.transform(df_cluster3_log)

# 평균값 계산
cluster2_scaled_means = df_cluster2_scaled.mean(axis=0)
cluster3_scaled_means = df_cluster3_scaled.mean(axis=0)

# 시각화
x = np.arange(len(important_columns_no_income))
width = 0.35
fig, ax = plt.subplots(figsize=(14, 7))
rects1 = ax.bar(x - width/2, cluster2_scaled_means, width, label='Cluster 2', color='skyblue', capsize=5)
rects2 = ax.bar(x + width/2, cluster3_scaled_means, width, label='Cluster 3', color='royalblue', capsize=5)
ax.set_ylabel('로그 변환 + Robust Scaled 값', fontsize=14)
ax.set_title('Cluster 2 vs Cluster 3 주요 변수 비교 (Log+Robust Scaling)', fontsize=18)
ax.set_xticks(x)
ax.set_xticklabels(important_columns_no_income, rotation=30, ha='right')
ax.legend()
ax.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
st.pyplot(fig)
