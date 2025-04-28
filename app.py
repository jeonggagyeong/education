import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import gower

# -----------------------------------------------------
# Streamlit 대시보드 시작
st.title("군집분석 대시보드 (VIF + Gower + PCA)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.subheader("데이터 미리보기")
    st.dataframe(data.head())

    # 사용할 변수 리스트 선택
    selected_columns = st.multiselect("분석에 사용할 컬럼을 선택하세요", data.columns.tolist())

    if selected_columns:
        sample_data = data[selected_columns].copy()

        # 결측치 제거
        sample_data = sample_data.dropna()

        # 수치형 데이터만 추출
        numeric_data = sample_data.select_dtypes(include=["float64", "int64"])

        st.subheader("VIF(다중공선성) 분석")
        if not numeric_data.empty:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_data)

            vif_df = pd.DataFrame()
            vif_df["변수명"] = numeric_data.columns
            vif_df["VIF"] = [variance_inflation_factor(scaled_data, i) for i in range(scaled_data.shape[1])]

            st.dataframe(vif_df.sort_values(by="VIF", ascending=False))

        # Gower 거리 계산
        st.subheader("Gower 거리 기반 계층적 클러스터링")
        distance_matrix = gower.gower_matrix(sample_data)
        distance_matrix = np.nan_to_num(distance_matrix, nan=1.0, posinf=1.0, neginf=1.0)
        linked = linkage(distance_matrix, method='average')

        # 덴드로그램 시각화
        st.write("덴드로그램")
        fig, ax = plt.subplots(figsize=(10, 6))
        dendrogram(linked, ax=ax)
        st.pyplot(fig)

        # 클러스터 수 선택
        k = st.slider("클러스터 수 (k)", 2, 10, 3)
        cluster_labels = fcluster(linked, k, criterion='maxclust')
        data['cluster'] = cluster_labels

        # 클러스터별 개수 출력
        st.write("### 클러스터별 데이터 수")
        st.dataframe(data['cluster'].value_counts())

        # Elbow Plot (실루엣 스코어 기반)
        st.write("### Elbow Plot (군집 수 최적화)")
        ks = range(2, 11)
        silhouette_scores = []

        for num in ks:
            labels = fcluster(linked, num, criterion='maxclust')
            score = silhouette_score(distance_matrix, labels, metric='precomputed')
            silhouette_scores.append(score)

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.plot(ks, silhouette_scores, marker='o')
        ax2.set_title("Elbow Plot (실루엣 점수)")
        ax2.set_xlabel("군집 수 (k)")
        ax2.set_ylabel("실루엣 점수")
        ax2.grid(True)
        st.pyplot(fig2)

        # PCA 2D 시각화
        st.subheader("PCA를 통한 2D 시각화")

        # 범주형 인코딩
        sample_encoded = pd.get_dummies(sample_data, drop_first=True)

        # 결측치 보간
        imputer = SimpleImputer(strategy="mean")
        imputed_data = imputer.fit_transform(sample_encoded)

        # 스케일링
        scaler2 = StandardScaler()
        scaled_pca_data = scaler2.fit_transform(imputed_data)

        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled_pca_data)

        pca_df = pd.DataFrame(pca_result, columns=["PC1", "PC2"])
        pca_df["cluster"] = cluster_labels

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="cluster", palette="Set2", s=60, ax=ax3)
        ax3.set_title("PCA 2D 군집 시각화")
        ax3.grid(True)
        st.pyplot(fig3)

    else:
        st.warning("변수를 하나 이상 선택하세요.")

else:
    st.info("먼저 CSV 파일을 업로드해주세요.")
