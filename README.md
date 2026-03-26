##  ❌공모전 마감 이후 부족한 점 수정
 1. 다중공선성이 높은 변수들을 제거하여 효율을 높이지 못한 점 -> VIF가 20이 넘는 변수 삭제 후 상관관계가 높은 변수들은 그 중 하나만 남기기
 2. 변수 선택 과정을 변수 갯수 1부터 시작하여 하나씩 늘려나가며 적절한 cluster 비율과 실루엣 계산 고려를 통해 변수 조합 선택



## 🎓 제6회 교육부 공모전
### 📊 학교별 분석을 통한 돌봄교실 맞춤형 정책 제안

획일적인 돌봄교실 운영, 데이터로 해법을 찾다!
Gower 거리 기반 클러스터링을 활용한 지역 맞춤형 정책 자동화 솔루션

## 🧩 프로젝트 개요

### 주제: 지역 및 학교별 특성을 고려한 돌봄교실 수요 예측 및 맞춤형 정책 제안

### 목표: 돌봄교실 수요가 정량적으로 분석되기 어려운 상황에서, 공공데이터 기반 클러스터링 분석을 통해 유사 특성을 가진 학교군 분류 및 정책 설계 자동화 구현

### 🛠 기술 스택
분야	도구
데이터 수집	공공데이터 포털, Open API, Pandas
분석 기법	Gower Distance, Hierarchical Clustering
시각화	Streamlit, Matplotlib, Seaborn
자동화/배포	Gmail API (자동 메일 발송), Streamlit, render

### 🔍 주요 기능
🎯 혼합형 변수에 대응하는 Gower 거리 기반 클러스터링

🏫 지역별 특성을 반영한 학교군 자동 분류 및 수요 예측

📈 클러스터별 중요 변수 도출 및 맞춤형 정책 제안

📬 데이터 변경 시 모델 재학습 → 시각화 → 담당자 자동 이메일 전송까지 자동화

![Image](https://github.com/user-attachments/assets/0f1db76f-b540-48ee-bb20-06d77e287a4f)

![Image](https://github.com/user-attachments/assets/5d730d35-52ec-4433-aefb-6ee8abde19d6)



![Image](https://github.com/user-attachments/assets/5184d9ac-b2ce-4728-87be-ac18b23c828e)

