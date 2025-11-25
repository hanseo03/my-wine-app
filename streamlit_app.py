"""
와인 추천 시스템 Streamlit 웹 UI
"""

import streamlit as st
from recommender import WineRecommender
import time


# 페이지 설정
st.set_page_config(
    page_title="와인 추천 시스템",
    page_icon="🍷",
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
    st.title("🍷 와인 추천 시스템")
    st.markdown("음식에 어울리는 와인을 추천해드립니다!")
    st.markdown("💡 GPT API와 KNN-알고리즘을 사용하여 임의의 음식에 대한 최적의 와인을 찾습니다.")
    
    # 추천 시스템 초기화
    if not st.session_state.initialized:
        initialize_recommender()
    
    # 사이드바
    with st.sidebar:
        st.header("ℹ️ 정보")
        st.markdown("""
        **기본 프로파일이 있는 음식:**
        - steak
        - salmon
        - dessert
        - cheese
        
        **다른 음식도 입력 가능하며, GPT API로 자동 분석됩니다.**
        """)
        
        if st.session_state.initialized:
            st.success("✅ 시스템 준비 완료")
    
    # 음식 입력 폼
    st.header("음식 입력")
    food_input = st.text_input(
        "음식 이름을 입력하세요",
        placeholder="예: 파스타, 치킨, 초콜릿 케이크 등",
        key="food_input"
    )
    
    # 추천 버튼
    if st.button("🍷 와인 추천", type="primary", use_container_width=True):
        if not food_input or not food_input.strip():
            st.warning("⚠️ 음식 이름을 입력해주세요.")
        else:
            food_name = food_input.strip()
            
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
    
    # 하단 정보
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>와인 추천 시스템 | KNN 알고리즘 기반</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

