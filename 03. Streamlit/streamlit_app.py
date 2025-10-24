import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="이화여대 대학원 수업 설문조사",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 이화여대 색상 테마 CSS
st.markdown("""
<style>
    .main {
        background-color: #f8fffe;
    }
    .stTitle {
        color: #00704a;
        font-weight: bold;
        text-align: center;
        padding: 20px 0;
    }
    .stHeader {
        color: #00704a;
        border-bottom: 2px solid #00704a;
        padding-bottom: 10px;
    }
    .stSubheader {
        color: #2d8659;
    }
    .survey-section {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 4px solid #00704a;
    }
    .ewha-button {
        background-color: #00704a;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #e8f5f0;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #00704a;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #00704a, #2d8659); color: white; border-radius: 10px; margin-bottom: 30px;">
    <h1>🎓 이화여자대학교 대학원</h1>
    <h2>수업 만족도 설문조사</h2>
    <p>더 나은 교육 환경을 위한 여러분의 소중한 의견을 들려주세요</p>
</div>
""", unsafe_allow_html=True)

# 사이드바 - 설문조사 결과 시각화
st.sidebar.markdown("## 📊 실시간 설문 결과")

# 더미 데이터 생성
@st.cache_data
def generate_dummy_data():
    np.random.seed(42)
    departments = ['국어국문학과', '영어영문학과', '사학과', '철학과', '수학과', '물리학과', '화학과', '생명과학과', '컴퓨터공학과', '전자공학과']
    grades = ['석사 1년차', '석사 2년차', '박사 1년차', '박사 2년차', '박사 3년차 이상']
    
    data = []
    for _ in range(150):  # 150명의 응답자
        data.append({
            'department': np.random.choice(departments),
            'grade': np.random.choice(grades),
            'course_satisfaction': np.random.randint(1, 6),
            'professor_satisfaction': np.random.randint(1, 6),
            'facility_satisfaction': np.random.randint(1, 6),
            'overall_satisfaction': np.random.randint(1, 6),
            'recommend': np.random.choice(['매우 추천', '추천', '보통', '비추천', '매우 비추천']),
            'online_preference': np.random.choice(['대면 수업', '온라인 수업', '혼합형 수업'])
        })
    return pd.DataFrame(data)

dummy_df = generate_dummy_data()

# 사이드바 통계
st.sidebar.metric("총 응답자 수", len(dummy_df))
st.sidebar.metric("평균 만족도", f"{dummy_df['overall_satisfaction'].mean():.1f}/5.0")

# 학과별 응답 분포
dept_counts = dummy_df['department'].value_counts()
fig_dept = px.bar(x=dept_counts.values, y=dept_counts.index, orientation='h',
                  title="학과별 응답자 분포", color_discrete_sequence=['#00704a'])
fig_dept.update_layout(height=400, showlegend=False)
st.sidebar.plotly_chart(fig_dept, use_container_width=True)

# 메인 설문조사 폼
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.header("📝 기본 정보")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("성명", placeholder="홍길동")
    student_id = st.text_input("학번", placeholder="2024123456")
    department = st.selectbox(
        "소속 학과",
        ['국어국문학과', '영어영문학과', '사학과', '철학과', '수학과', '물리학과', 
         '화학과', '생명과학과', '컴퓨터공학과', '전자공학과', '기타']
    )

with col2:
    grade = st.selectbox(
        "학년",
        ['석사 1년차', '석사 2년차', '박사 1년차', '박사 2년차', '박사 3년차 이상']
    )
    semester = st.selectbox("학기", ['2024-1학기', '2024-2학기'])
    course_name = st.text_input("수강 과목명", placeholder="예: 고급 데이터 분석")

st.markdown('</div>', unsafe_allow_html=True)

# 수업 만족도 평가
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.header("📚 수업 만족도 평가")

col1, col2 = st.columns(2)

with col1:
    course_satisfaction = st.select_slider(
        "수업 내용 만족도",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: f"{x}점 ({'매우 불만족' if x==1 else '불만족' if x==2 else '보통' if x==3 else '만족' if x==4 else '매우 만족'})"
    )
    
    professor_satisfaction = st.select_slider(
        "교수님 강의 만족도",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: f"{x}점 ({'매우 불만족' if x==1 else '불만족' if x==2 else '보통' if x==3 else '만족' if x==4 else '매우 만족'})"
    )

with col2:
    facility_satisfaction = st.select_slider(
        "시설 및 환경 만족도",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: f"{x}점 ({'매우 불만족' if x==1 else '불만족' if x==2 else '보통' if x==3 else '만족' if x==4 else '매우 만족'})"
    )
    
    overall_satisfaction = st.select_slider(
        "전반적 만족도",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: f"{x}점 ({'매우 불만족' if x==1 else '불만족' if x==2 else '보통' if x==3 else '만족' if x==4 else '매우 만족'})"
    )

st.markdown('</div>', unsafe_allow_html=True)

# 수업 방식 선호도
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.header("💻 수업 방식 선호도")

online_preference = st.radio(
    "선호하는 수업 방식",
    ['대면 수업', '온라인 수업', '혼합형 수업'],
    horizontal=True
)

recommend = st.selectbox(
    "이 수업을 다른 학생에게 추천하시겠습니까?",
    ['매우 추천', '추천', '보통', '비추천', '매우 비추천']
)

st.markdown('</div>', unsafe_allow_html=True)

# 개선사항 및 의견
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.header("💡 개선사항 및 의견")

improvements = st.multiselect(
    "개선이 필요한 부분 (복수 선택 가능)",
    ['강의 내용', '강의 방법', '과제 및 평가', '시설 및 환경', '온라인 플랫폼', '교재 및 자료', '기타']
)

additional_comments = st.text_area(
    "추가 의견 및 건의사항",
    placeholder="수업에 대한 자세한 의견이나 개선사항을 자유롭게 작성해주세요.",
    height=100
)

st.markdown('</div>', unsafe_allow_html=True)

# 설문 제출 버튼
if st.button("📤 설문조사 제출", type="primary"):
    if name and student_id and course_name:
        st.success("✅ 설문조사가 성공적으로 제출되었습니다. 소중한 의견 감사합니다!")
        
        # 제출된 정보 요약
        st.markdown("### 📋 제출된 정보 요약")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **기본 정보**
            - 성명: {name}
            - 학과: {department}
            - 학년: {grade}
            """)
        
        with col2:
            st.markdown(f"""
            **만족도 평가**
            - 수업 내용: {course_satisfaction}/5
            - 교수님 강의: {professor_satisfaction}/5
            - 시설 환경: {facility_satisfaction}/5
            - 전반적 만족도: {overall_satisfaction}/5
            """)
        
        with col3:
            st.markdown(f"""
            **기타 정보**
            - 수업 방식 선호: {online_preference}
            - 추천 의향: {recommend}
            - 개선 필요 부분: {', '.join(improvements) if improvements else '없음'}
            """)
    else:
        st.error("❌ 필수 항목(성명, 학번, 수강 과목명)을 모두 입력해주세요.")

# 설문 결과 시각화
st.markdown("---")
st.header("📈 설문조사 결과 분석")

tab1, tab2, tab3 = st.tabs(["만족도 분석", "학과별 분석", "수업 방식 선호도"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # 만족도 분포
        satisfaction_data = {
            '수업 내용': dummy_df['course_satisfaction'].mean(),
            '교수님 강의': dummy_df['professor_satisfaction'].mean(),
            '시설 환경': dummy_df['facility_satisfaction'].mean(),
            '전반적 만족도': dummy_df['overall_satisfaction'].mean()
        }
        
        fig_satisfaction = px.bar(
            x=list(satisfaction_data.keys()),
            y=list(satisfaction_data.values()),
            title="평균 만족도 점수",
            color_discrete_sequence=['#00704a']
        )
        fig_satisfaction.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    with col2:
        # 추천 의향 분포
        recommend_counts = dummy_df['recommend'].value_counts()
        fig_recommend = px.pie(
            values=recommend_counts.values,
            names=recommend_counts.index,
            title="추천 의향 분포",
            color_discrete_sequence=['#00704a', '#2d8659', '#5ba373', '#89c08d', '#b7dda7']
        )
        st.plotly_chart(fig_recommend, use_container_width=True)

with tab2:
    # 학과별 만족도
    dept_satisfaction = dummy_df.groupby('department')['overall_satisfaction'].mean().sort_values(ascending=False)
    fig_dept_sat = px.bar(
        x=dept_satisfaction.values,
        y=dept_satisfaction.index,
        orientation='h',
        title="학과별 평균 만족도",
        color_discrete_sequence=['#00704a']
    )
    st.plotly_chart(fig_dept_sat, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # 수업 방식 선호도
        online_counts = dummy_df['online_preference'].value_counts()
        fig_online = px.pie(
            values=online_counts.values,
            names=online_counts.index,
            title="수업 방식 선호도",
            color_discrete_sequence=['#00704a', '#2d8659', '#5ba373']
        )
        st.plotly_chart(fig_online, use_container_width=True)
    
    with col2:
        # 학년별 선호도
        grade_online = pd.crosstab(dummy_df['grade'], dummy_df['online_preference'])
        fig_grade_online = px.bar(
            grade_online,
            title="학년별 수업 방식 선호도",
            color_discrete_sequence=['#00704a', '#2d8659', '#5ba373']
        )
        st.plotly_chart(fig_grade_online, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00704a; padding: 20px;">
    <p><strong>이화여자대학교 대학원</strong></p>
    <p>더 나은 교육 환경을 위한 여러분의 참여에 감사드립니다.</p>
</div>
""", unsafe_allow_html=True)