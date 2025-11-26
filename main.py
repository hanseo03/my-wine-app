"""
와인 추천 시스템 CLI 인터페이스
메인 실행 파일
"""

from recommender import WineRecommender


def format_recommendations(recommendations, profile_info):
    """
    추천 결과를 포맷팅하여 출력합니다.
    
    Args:
        recommendations: 추천 와인 딕셔너리 리스트
        profile_info: 프로파일 정보 딕셔너리
    """
    print("\n" + "="*80)
    print("🍷 추천 와인")
    print("="*80)
    
    # 프로파일 정보 출력
    profile = profile_info['profile']
    source = profile_info['source']
    description = profile_info.get('description', '')
    source_text = "GPT API로 생성" if source == 'gpt' else "기본 프로파일 사용"
    print(f"\n📊 음식 프로파일: 단맛={profile[0]}, 산도={profile[1]}, "
          f"바디={profile[2]}, 탄닌={profile[3]} ({source_text})")
    
    # 설명 출력
    if description:
        print(f"\n💬 프로파일 설명:")
        print(f"   {description}")
    
    print("\n추천 와인:")
    for i, wine in enumerate(recommendations, 1):
        print(f"\n{i}. {wine['name']}")
        print(f"   맛 프로파일: 단맛={wine['sweet']}, 산도={wine['acidity']}, "
              f"바디={wine['body']}, 탄닌={wine['tannin']}")
        price_text = f"{int(wine['price']):,}" if wine.get('price') is not None else "정보 없음"
        print(f"   가격: ₩{price_text}")
        abv_text = f"{wine['abv']:.1f}%" if wine.get('abv') is not None else "정보 없음"
        type_text = wine.get('type') or "정보 없음"
        nation_text = wine.get('nation') or "정보 없음"
        year_text = str(int(wine['year'])) if wine.get('year') is not None else "정보 없음"
        print(f"   알코올 도수: {abv_text}")
        print(f"   종류: {type_text} | 국가: {nation_text} | 빈티지: {year_text}")
    
    print("\n" + "="*80)


def main():
    """
    메인 실행 함수
    """
    print("="*80)
    print("와인 추천 시스템")
    print("="*80)
    print("\n음식에 맞는 와인을 추천해드립니다!")
    print("💡 GPT API를 사용하여 임의의 음식에 대한 최적의 와인 프로파일을 생성합니다.")
    
    try:
        # 추천 시스템 초기화
        recommender = WineRecommender()
        
        # 사용 가능한 기본 음식 목록 출력 (참고용)
        available_foods = recommender.get_available_foods()
        print(f"\n💡 참고: 기본 프로파일이 있는 음식: {', '.join(available_foods)}")
        print("   (다른 음식도 입력 가능하며, GPT API로 자동 분석됩니다)")
        
        # 인터랙티브 루프
        while True:
            print("\n" + "-"*80)
            food = input("\n음식을 입력하세요 (종료하려면 'quit' 또는 'exit' 입력): ").strip()
            
            # 종료 명령 처리
            if food.lower() in ['quit', 'exit', 'q']:
                print("\n프로그램을 종료합니다. 좋은 하루 되세요! 🍷")
                break
            
            # 빈 입력 처리
            if not food:
                print("음식 이름을 입력해주세요.")
                continue
            
            try:
                # GPT API로 프로파일 생성 중 표시
                print(f"\n🔍 '{food}'에 어울리는 와인 프로파일을 생성하는 중...")
                
                # 와인 추천
                recommendations, profile_info = recommender.recommend(food)
                
                # 결과 출력
                print(f"\n✅ '{food}'에 어울리는 와인:")
                format_recommendations(recommendations, profile_info)
                
            except ValueError as e:
                print(f"❌ 오류: {str(e)}")
            except Exception as e:
                print(f"❌ 예상치 못한 오류가 발생했습니다: {str(e)}")
    
    except FileNotFoundError as e:
        print(f"❌ 오류: {str(e)}")
        print("CSV 파일이 올바른 위치에 있는지 확인해주세요.")
    except Exception as e:
        print(f"❌ 오류: {str(e)}")
        print("프로그램을 시작하는 중 문제가 발생했습니다.")


if __name__ == "__main__":
    main()

