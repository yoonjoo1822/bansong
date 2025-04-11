import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.write("✅ 앱이 정상적으로 실행 중입니다.")  # 앱이 화면에 출력되는지 확인


# 제목 설정
st.title("💡윤주샘과 함께하는 데이터 분석")

st.text("")  # 공백 한 줄 추가

            
    
st.subheader("🌟 환영합니다!")
st.info("""
    이 애플리케이션은 **반송고 1학년 데이터 분석 및 모델링 수업**을 위해 윤주샘이 개발했습니다😊 
    수업을 마치고 별도의 보고서를 리로스쿨에 제출하면 교과세특에 작성됩니다.🚀
    """)
    
st.markdown("""
    - 이 앱에서는 분석하고 싶은 데이터 파일을 업로드하면 그래프로 시각화해줍니다.
    - 그래프의 <u>추세선(직선의 방정식)</u>을 활용하여 데이터를 분석해봅시다.
    - step1 부터 step5 까지 순서대로 따라해보세요.
    """, unsafe_allow_html=True)
st.text("")  # 공백 한 줄 추가
st.text("")  # 공백 한 줄 추가
          
          
            
# 1) 데이터 탐색
st.markdown(
    "<h3 style='font-size:20px; font-weight:bold; margin-bottom: 0;'>Step1) 🔍 데이터 탐색</h3>",
    unsafe_allow_html=True
)

# KOSIS 이동 버튼 추가
st.markdown("""
    <a href="https://kosis.kr/statisticsList/statisticsListIndex.do?vwcd=MT_ZTITLE&menuId=M_01_01" target="_blank">
        <button style="
            background-color: #d4edda; 
            color: #155724; 
            border: none; 
            border-radius: 8px; 
            padding: 10px 20px; 
            font-size: 16px; 
            font-weight: bold;
            cursor: pointer;">
            📥 여기를 클릭하여 국가통계포털 KOSIS에서 원하는 데이터를 다운로드 받으세요.
        </button>
    </a>
""", unsafe_allow_html=True)


st.markdown("""
    - 연도별 변화 추이를 분석하고 싶은 데이터를 선정하세요.
    - 데이터는 반드시 '숫자 데이터' 여야 합니다.
    - 10분 안에 데이터 다운로드를 마쳐야 합니다.
    - 다운로드 파일 형태는 CSV 여야 합니다. (예: 연도별 인구수.csv)
    """)
st.text("")  # 공백 한 줄 추가
st.text("")  # 공백 한 줄 추가



# 2) 데이터 전처리 안내
st.markdown(
    "<h3 style='font-size:20px; font-weight:bold;'>Step2) 🛠️ 데이터 전처리</h3>", 
    unsafe_allow_html=True
    )

with st.expander("선정한 데이터를 다음과 조건에 맞추어 정리하세요.", expanded = True):
     st.write("""
        - 모든 데이터는 숫자 데이터여야 합니다. (예: 인구 수, 참여율, 농도 등)
        - 불필요한 열 또는 행은 모두 삭제합니다.
        - x, y축에 들어갈 2개의 데이터를 2개의 열로 정리합니다.
        - 첫번째 행은 데이터의 정보(x축 이름, y축 이름)가 들어갑니다.
        - 데이터는 CSV 형식의 파일이어야 합니다. (예: 연도별 인구수.csv)
        """)    
     # 이미지 추가
     st.image(
        "전처리 예시.jpg", 
        caption="데이터 전처리 예시",
        width=300  # 원하는 이미지 너비 설정
     )
st.text("")  # 공백 한 줄 추가
st.text("")  # 공백 한 줄 추가
            
    
# 3) 데이터 업로드
st.markdown("<h3 style='font-size:20px; font-weight:bold;'>Step3) 📂데이터 업로드</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("CSV 파일 형식으로 업로드하세요:", type=["csv"])
    
if uploaded_file is not None:
    # 데이터 읽기
    try:
        # ANSI(CP1252/CP949) 인코딩 시도
        data = pd.read_csv(uploaded_file, encoding="cp949")
    except UnicodeDecodeError:
        try:
        # UTF-8로 재시도
            data = pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            st.error("⚠️ 지원되지 않는 파일 인코딩 형식입니다. ANSI, UTF-8, 또는 CP949 형식의 파일을 업로드해주세요.")
            data = None

    if data is not None: 
        # 데이터를 표로 출력 
        st.markdown("<h3 style='font-size:16px; font-weight:bold;'>📝참고: 업로드한 데이터 확인하기</h3>", unsafe_allow_html=True)
        st.dataframe(data, height=200, use_container_width=True)  # 전체 데이터를 스크롤 가능한 표로 출력
st.text("")  # 공백 한 줄 추가
st.text("")  # 공백 한 줄 추가



# 4) 데이터 시각화
st.markdown("<h3 style='font-size:20px; font-weight:bold;'>Step4) 📈데이터 시각화</h3>", unsafe_allow_html=True)

if uploaded_file is not None and data is not None:  # 데이터가 업로드된 경우에만 실행
    # X, Y 변수 선택 탭
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox(
            "📊 X축 데이터를 선택하세요.:", 
            ["선택하세요"] + list(data.columns),  # "선택하세요"를 옵션에 추가
            index=0  # 기본값으로 "선택하세요" 설정
        )
    with col2:
        y_col = st.selectbox(
            "📊 Y축 데이터를 선택하세요.:", 
            ["선택하세요"] + list(data.columns),  # "선택하세요"를 옵션에 추가
            index=0  # 기본값으로 "선택하세요" 설정
        )

    # 학생이 선택해야만 다음 단계를 진행할 수 있도록 조건 설정
    if x_col != "선택하세요" and y_col != "선택하세요":
        # X, Y 데이터를 숫자로 변환 (필요할 경우 소수점 유지)
        x = pd.to_numeric(data[x_col], errors='coerce')
        y = pd.to_numeric(data[y_col], errors='coerce')

        # NaN 값 제거
        valid_mask = ~np.isnan(x) & ~np.isnan(y)
        x = x[valid_mask]
        y = y[valid_mask]

        # 선형 회귀 계산
        slope, intercept, r_value, _, _ = stats.linregress(x, y)
        y_pred = slope * x + intercept  # 추세선 값

        # 산점도와 추세선 그리기
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x, y, c='blue', alpha=0.7, label='Data')  # 산점도
        ax.plot(x, y_pred, color='red', label='Trend Line')  # 추세선
        ax.legend()
        st.pyplot(fig)

        # 추세선 방정식 출력
        st.markdown(f"**추세선 방정식**: y = {slope:.2f}x + {intercept:.2f}")
        
    else:
        st.warning("⚠️ X축과 Y축 데이터를 모두 선택하세요.")
else:
    st.warning("⚠️ 데이터를 업로드하면 시각화 그래프가 나옵니다.")

st.text("")  # 공백 한 줄 추가
st.text("")  # 공백 한 줄 추가


                   
# 5) 데이터 분석하기
st.markdown("<h3 style='font-size:20px; font-weight:bold;'>Step5) 💬데이터 분석하기</h3>", unsafe_allow_html=True)

# 데이터 분석 안내 메시지
st.info("🔍추세선을 이용하여 데이터의 변화 추이를 분석하는 글을 작성하세요.")

# 답안 작성 텍스트 박스
analysis_text = st.text_area(
    "✏️ 분석 내용을 작성하세요:",
    placeholder="예시: 연도별 인구 추이는 계속해서 증가하고 있다. 추세선의 직선의 방정식은 y=0.24x-423 으로 기울기가 0.24정도의 경향으로 증가하고 있음을 알 수 있다. 추세선을 이용하여 2080년의 인구수를 예측해보면...",
    height=250  # 텍스트 박스의 세로 길이
)
st.text("")  # 공백 한 줄 추가



# 학번과 이름 입력
st.markdown("#### 📌 학생 정보")

# 상태 저장을 위한 세션 상태 초기화
if "saved" not in st.session_state:
    st.session_state["saved"] = False
if "student_id" not in st.session_state:
    st.session_state["student_id"] = ""
if "student_name" not in st.session_state:
    st.session_state["student_name"] = ""

if not st.session_state["saved"]:  # 입력창과 버튼이 보이는 상태
    # 한 줄에 학번, 이름 입력 필드와 저장 버튼 배치
    col1, col2, col3 = st.columns([3, 3, 1])  # 열의 비율 설정

    with col1:
        student_id = st.text_input(
            "학번 입력",
            placeholder="예시: 10201",
            max_chars=10,
            key="student_id",
        )  # 학번 입력

    with col2:
        student_name = st.text_input(
            "이름 입력",
            placeholder="예시: 조윤주",
            max_chars=20,
            key="student_name",
        )  # 이름 입력

    with col3:
        if st.button("저장"):
            # 학번과 이름이 모두 입력되었는지 확인
            if student_id.strip() and student_name.strip():
                st.session_state["saved"] = True
            else:
                st.error("⚠️ 학번과 이름을 모두 입력해주세요!")
else:
    # 입력창과 버튼 대신 메시지 출력
    st.success(
        f"🎉 **{st.session_state['student_id']} {st.session_state['student_name']}** 님이 접속하였습니다!"
    )
    st.markdown("""
                - 이제 ctrl+A, ctrl+P 를 누르고 전체 드래그하여 pdf로 인쇄하여 파일을 제출하세요.
                - 오늘 제출한 pdf 파일을 토대로 **보고서**를 작성하면 교과세특에 작성됩니다!
                """)


st.write("✅ 앱 끝까지 실행됨")
