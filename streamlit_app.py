"""
와인 추천 시스템 Streamlit 웹 UI
"""

import streamlit as st
from recommender import WineRecommender
import time


# 페이지 설정
st.set_page_config(
    page_title="Le Mariage",
    page_icon="🔔",
    layout="wide"
)

# 세션 상태 초기화
if 'recommender' not in st.session_state:
    st.session_state.recommender = None
if 'initialized' not in st.session_state:
    st.session_state.initialized = False


def initialize_recommender():
    """추천 시스템 초기화"""
    if not st.session_state.initialized:
        with st.spinner("데이터를 로드하고 모델을 학습하는 중..."):
            st.session_state.recommender = WineRecommender()
            st.session_state.initialized = True


def format_profile_bar(value, max_value, label):
    """맛 프로파일을 바 형태로 표시"""
    percentage = (value / max_value) * 100
    # 진행 바 색상 설정을 위해 컬럼 사용
    col_bar, col_text = st.columns([4, 1])
    with col_bar:
        st.progress(percentage / 100)
    with col_text:
        st.markdown(f"**{value}/{max_value}**")


def display_wine_profile(wine, index):
    """와인 프로파일을 바 형태로 표시"""
    with st.container():
        st.markdown(f"### {index}. {wine['name']}")
        
        # 맛 프로파일 바 차트
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**단맛 (Sweet)**")
            format_profile_bar(wine['sweet'], 5, "Sweet")
            
            st.markdown("**산도 (Acidity)**")
            format_profile_bar(wine['acidity'], 4, "Acidity")
        
        with col2:
            st.markdown("**바디감 (Body)**")
            format_profile_bar(wine['body'], 5, "Body")
            
            st.markdown("**탄닌감 (Tannin)**")
            format_profile_bar(wine['tannin'], 5, "Tannin")
        
        st.markdown(f"**유사도 거리**: {wine['distance']:.4f}")
        st.divider()


def main():
    """메인 UI"""
    # 커스텀 CSS 스타일 적용
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');
        
        /* 전체 배경색 - 아주 약한 노란끼가 도는 흰색 */
        .stApp {
            background-color: #FFFEF7;
        }
        
        /* 메인 컨테이너 배경 */
        .main .block-container {
            background-color: #FFFEF7;
        }
        
        /* 텍스트 색상 - 검은색 */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, div, span {
            color: #1a1a1a !important;
        }
        
        /* 제목 색상 - 금색 */
        h1 {
            color: #D4AF37 !important;
        }
        
        /* 헤더 색상 - 금색 */
        h2, h3 {
            color: #D4AF37 !important;
        }
        
        /* 강조 텍스트 - 금색 */
        strong, b {
            color: #D4AF37 !important;
        }
        
        /* 버튼 스타일 - 금색 배경 */
        .stButton > button {
            background-color: #D4AF37;
            color: #1a1a1a;
            border: none;
            font-weight: bold;
        }
        
        .stButton > button:hover {
            background-color: #B8941F;
            color: #1a1a1a;
        }
        
        /* 입력 필드 스타일 - 금색 테두리, 미색 배경 */
        .stTextInput > div > div > input {
            border-color: #D4AF37;
            background-color: #FFFEF7;
            color: #1a1a1a;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #D4AF37;
            background-color: #FFFEF7;
            box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
        }
        
        /* 플레이스홀더 색상 */
        .stTextInput > div > div > input::placeholder {
            color: #999;
        }
        
        /* 진행 바 - 금색 */
        .stProgress > div > div > div > div {
            background-color: #D4AF37;
        }
        
        /* 정보 박스 - 금색 테두리 */
        .stInfo {
            border-left: 4px solid #D4AF37;
        }
        
        /* 성공 메시지 - 금색 테두리 */
        .stSuccess {
            border-left: 4px solid #D4AF37;
        }
        
        /* 경고 메시지 - 금색 테두리 */
        .stWarning {
            border-left: 4px solid #D4AF37;
        }
        
        /* 에러 메시지 - 금색 테두리 */
        .stError {
            border-left: 4px solid #D4AF37;
        }
        
        /* 사이드바 배경 */
        .css-1d391kg {
            background-color: #FFFEF7;
        }
        
        /* 구분선 - 금색 */
        hr {
            border-color: #D4AF37;
        }
        
        /* 캡션 텍스트 - 금색 */
        .stCaption {
            color: #D4AF37 !important;
        }
        
        /* 하단 정보 텍스트 - 금색 */
        .footer-text {
            color: #D4AF37 !important;
        }
        
        /* 사이드바 숨기기 */
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        /* 메인 컨텐츠 영역 확장 */
        .main .block-container {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        
        /* 설명 박스 스타일 - 금색 배경, 미색 텍스트, 전체 너비 */
        .info-box {
            background-color: #D4AF37;
            padding: 3rem 2rem;
            border-radius: 0;
            margin-top: 2rem;
            margin-left: -2rem;
            margin-right: -2rem;
            width: calc(100% + 4rem);
            color: #FFFEF7;
            box-sizing: border-box;
        }
        
        /* 전체 너비를 위한 컨테이너 조정 */
        .info-container {
            width: 100vw;
            position: relative;
            left: 50%;
            right: 50%;
            margin-left: -50vw;
            margin-right: -50vw;
        }
        
        .info-box h3 {
            color: #FFFEF7 !important;
            margin-bottom: 1rem;
        }
        
        .info-box p {
            color: #FFFEF7 !important;
            line-height: 1.8;
        }
        
        /* 입력 영역 중앙 정렬 */
        .input-section {
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* 섹션 스타일 */
        .section {
            padding: 4rem 2rem;
            margin: 2rem 0;
        }
        
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
            color: #D4AF37 !important;
            font-family: "Playfair Display", serif;
        }
        
        /* Feature 카드 */
        .feature-card {
            background-color: #FFFEF7;
            border: 2px solid #D4AF37;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            height: 100%;
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(212, 175, 55, 0.2);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-size: 1.5rem;
            color: #D4AF37 !important;
            margin-bottom: 1rem;
            font-weight: bold;
        }
        
        .feature-text {
            color: #1a1a1a;
            line-height: 1.6;
        }
        
        /* How it Works 스텝 */
        .step-card {
            background-color: #FFFEF7;
            border-left: 4px solid #D4AF37;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 5px;
        }
        
        .step-number {
            display: inline-block;
            width: 50px;
            height: 50px;
            background-color: #D4AF37;
            color: #FFFEF7;
            border-radius: 50%;
            text-align: center;
            line-height: 50px;
            font-size: 1.5rem;
            font-weight: bold;
            margin-right: 1rem;
        }
        
        .step-title {
            font-size: 1.5rem;
            color: #D4AF37 !important;
            margin-bottom: 0.5rem;
        }
        
        /* 통계 섹션 */
        .stats-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            padding: 2rem 0;
        }
        
        .stat-item {
            text-align: center;
            padding: 1rem;
        }
        
        .stat-number {
            font-size: 3rem;
            color: #D4AF37 !important;
            font-weight: bold;
            font-family: "Playfair Display", serif;
        }
        
        .stat-label {
            font-size: 1.2rem;
            color: #1a1a1a;
            margin-top: 0.5rem;
        }
        
        /* 예시 버튼 */
        .example-button {
            display: inline-block;
            padding: 0.5rem 1.5rem;
            margin: 0.5rem;
            background-color: transparent;
            border: 2px solid #D4AF37;
            color: #D4AF37;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        
        .example-button:hover {
            background-color: #D4AF37;
            color: #FFFEF7;
        }
        
        /* Hero 섹션 */
        .hero-section {
            padding: 4rem 2rem;
            text-align: center;
        }
        
        /* CTA 섹션 */
        .cta-section {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(212, 175, 55, 0.05) 100%);
            padding: 3rem 2rem;
            border-radius: 10px;
            margin: 3rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 추천 시스템 초기화
    if not st.session_state.initialized:
        initialize_recommender()
    
    # ========== Hero 섹션 ==========
    st.markdown(
        """
        <div class="hero-section">
            <h1 style='color: #D4AF37; margin-bottom: 0.5rem; font-style: italic; font-family: "Playfair Display", "Cormorant Garamond", serif; font-weight: 400; font-size: 4rem; letter-spacing: 2px;'>Le Mariage</h1>
            <p style='color: #1a1a1a; margin-top: 1rem; font-size: 1.5rem; font-weight: 300;'>완벽한 음식과 와인의 만남</p>
            <p style='color: #666; margin-top: 0.5rem; font-size: 1.1rem;'>AI 기반 와인 추천 시스템으로 당신의 식사를 더욱 특별하게</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # ========== CTA 섹션 (음식 입력) ==========
    st.markdown('<div class="cta-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    
    
    food_input = st.text_input(
        "음식 이름을 입력하세요",
        placeholder="예: 파스타, 치킨, 초콜릿 케이크, 스테이크 등",
        key="food_input"
    )
    
    
    
    # 추천 버튼 또는 예시 버튼 클릭 시
    should_recommend = False
    food_name = None
    
    
    if st.button("와인 추천하기", type="primary", use_container_width=True, key="recommend_btn"):
        if not food_input or not food_input.strip():
            st.warning("⚠️ 음식 이름을 입력해주세요.")
        else:
            food_name = food_input.strip()
            should_recommend = True
    
    if should_recommend and food_name:
        # 로딩 UI 표시
        with st.spinner(f"🔍 '{food_name}'에 어울리는 와인 프로파일을 생성하는 중..."):
            try:
                # 와인 추천
                recommendations, profile_info = st.session_state.recommender.recommend(food_name)
                
                # 결과 표시
                st.success(f"✅ '{food_name}'에 어울리는 와인을 찾았습니다!")
                
                # 프로파일 정보 표시
                st.header("📊 음식 프로파일")
                profile = profile_info['profile']
                source = profile_info['source']
                description = profile_info.get('description', '')
                
                source_text = "GPT API로 생성" if source == 'gpt' else "기본 프로파일 사용"
                st.info(f"**프로파일 소스**: {source_text}")
                
                # 프로파일 바 차트
                st.markdown("**목표 와인 프로파일:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**단맛 (Sweet)**")
                    st.progress(profile[0] / 5)
                    st.caption(f"Sweet: {profile[0]}/5")
                    
                    st.markdown("**산도 (Acidity)**")
                    st.progress(profile[1] / 4)
                    st.caption(f"Acidity: {profile[1]}/4")
                
                with col2:
                    st.markdown("**바디감 (Body)**")
                    st.progress(profile[2] / 5)
                    st.caption(f"Body: {profile[2]}/5")
                    
                    st.markdown("**탄닌감 (Tannin)**")
                    st.progress(profile[3] / 5)
                    st.caption(f"Tannin: {profile[3]}/5")
                
                # 설명 표시
                if description:
                    st.markdown("**💬 프로파일 설명:**")
                    st.info(description)
                
                # 추천 와인 표시
                st.header("🍷 추천 와인")
                st.markdown(f"총 {len(recommendations)}개의 와인이 추천되었습니다.")
                
                # 각 와인 표시
                for i, wine in enumerate(recommendations, 1):
                    display_wine_profile(wine, i)
                
            except ValueError as e:
                st.error(f"❌ 오류: {str(e)}")
            except Exception as e:
                st.error(f"❌ 예상치 못한 오류가 발생했습니다: {str(e)}")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ========== 설명 섹션 (금색 배경) ==========
    st.markdown(
        """
        <div class="info-container">
            <div class="info-box">
                <h3 style='text-align: center; font-size: 2rem; margin-bottom: 1.5rem;'>Le Mariage에 대해</h3>
                <p style='text-align: center; font-size: 1.1rem; line-height: 1.8;'>
                    Le Mariage는 GPT API와 KNN 알고리즘을 활용하여 음식에 최적의 와인을 추천해드립니다.<br><br>
                    어떤 음식을 드시든, 그에 어울리는 완벽한 와인을 찾아드립니다.<br>
                    단순히 음식 이름만 입력하시면, AI가 분석하여 최적의 와인 프로파일을 생성하고<br>
                    데이터베이스에서 가장 잘 어울리는 와인들을 추천해드립니다.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # ========== Features 섹션 ==========
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">왜 Le Mariage인가요?</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    features = [
        {
            "icon": "🤖",
            "title": "AI 기반 분석",
            "text": "GPT API를 활용한 지능형 와인 프로파일 생성으로 정확한 추천을 제공합니다."
        },
        {
            "icon": "🍷",
            "title": "다양한 와인",
            "text": "1,000개 이상의 와인 데이터베이스에서 최적의 매칭을 찾아드립니다."
        },
        {
            "icon": "⚡",
            "title": "간편한 사용",
            "text": "음식 이름만 입력하면 몇 초 만에 완벽한 와인 추천을 받을 수 있습니다."
        }
    ]
    
    for i, feature in enumerate(features):
        with [col1, col2, col3][i]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature['icon']}</div>
                    <div class="feature-title">{feature['title']}</div>
                    <div class="feature-text">{feature['text']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== How it Works 섹션 ==========
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">작동 방식</h2>', unsafe_allow_html=True)
    
    steps = [
        {
            "number": "1",
            "title": "음식 입력",
            "text": "드시고 싶은 음식의 이름을 입력하세요. 어떤 음식이든 가능합니다."
        },
        {
            "number": "2",
            "title": "AI 분석",
            "text": "음식의 특성을 분석하여 최적의 와인 프로파일을 생성합니다."
        },
        {
            "number": "3",
            "title": "와인 추천",
            "text": "KNN 알고리즘으로 데이터베이스에서 가장 잘 어울리는 와인들을 추천합니다."
        }
    ]
    
    for step in steps:
        st.markdown(
            f"""
            <div class="step-card">
                <span class="step-number">{step['number']}</span>
                <span class="step-title">{step['title']}</span>
                <p style='color: #1a1a1a; margin-top: 0.5rem;'>{step['text']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== 통계 섹션 ==========
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">1,000+</div>
                <div class="stat-label">와인 데이터베이스</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">AI</div>
                <div class="stat-label">지능형 분석</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">5</div>
                <div class="stat-label">최적 추천 개수</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 하단 정보
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer-text" style='text-align: center; color: #D4AF37;'>
            <p>와인 추천 시스템 | Le Mariage</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

