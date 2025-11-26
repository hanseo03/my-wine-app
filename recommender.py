"""
와인 추천 엔진 모듈
음식 프로파일을 기반으로 와인을 추천합니다.
"""

from model import WineKNNModel
from data_loader import load_wine_data, prepare_features
from food_profile_generator import get_food_profile_from_gpt
import pandas as pd


# 음식별 프로파일 정의 [sweet, acidity, body, tannin]
FOOD_PROFILES = {
    'steak': [2, 3, 5, 5],
    'salmon': [3, 4, 3, 2],
    'dessert': [5, 2, 2, 1],
    'cheese': [2, 3, 4, 4]
}


class WineRecommender:
    """
    와인 추천 클래스
    """
    
    def __init__(self, data_file="cleansingWine.csv", n_neighbors=5):
        """
        추천 시스템 초기화
        
        Args:
            data_file: 와인 데이터 CSV 파일 경로
            n_neighbors: 추천할 와인 개수 (기본값: 5)
        """
        # 데이터 로드 및 전처리
        print("데이터를 로드하는 중...")
        df_raw = load_wine_data(data_file)
        self.df = prepare_features(df_raw)
        
        # feature 추출
        self.features = ['sweet', 'acidity', 'body', 'tannin']
        X = self.df[self.features]
        
        # 모델 생성 및 학습
        print("모델을 학습하는 중...")
        self.model = WineKNNModel(n_neighbors=n_neighbors)
        self.model.fit(X)
        
        print(f"완료! 총 {len(self.df)}개의 와인이 로드되었습니다.")
    
    def get_food_profile(self, food_name, use_gpt=True):
        """
        음식 이름으로 프로파일을 가져옵니다.
        GPT API를 사용하여 프로파일을 생성하고, 실패 시 기존 프로파일을 사용합니다.
        
        Args:
            food_name: 음식 이름
            use_gpt: GPT API 사용 여부 (기본값: True)
        
        Returns:
            tuple: (프로파일 리스트, 프로파일 소스, 설명)
                - 프로파일: [sweet, acidity, body, tannin]
                - 프로파일 소스: 'gpt' 또는 'fallback'
                - 설명: 프로파일 설명 (GPT의 경우 상세 설명, fallback의 경우 기본 메시지)
        """
        food_name_clean = food_name.strip().lower()
        
        # GPT API로 프로파일 생성 시도
        if use_gpt:
            try:
                profile, description = get_food_profile_from_gpt(food_name)
                return profile, 'gpt', description
            except Exception as e:
                print(f"⚠️  GPT API 호출 실패: {str(e)}")
                print("기존 프로파일을 사용합니다...")
        
        # Fallback: 기존 프로파일 사용
        if food_name_clean in FOOD_PROFILES:
            description = f"{food_name}에 어울리는 기본 와인 프로파일입니다."
            return FOOD_PROFILES[food_name_clean], 'fallback', description
        
        # 알 수 없는 음식인 경우
        raise ValueError(
            f"알 수 없는 음식: '{food_name}'. "
            f"GPT API 호출도 실패했고, 기본 프로파일에도 없습니다. "
            f"기본 프로파일 목록: {', '.join(FOOD_PROFILES.keys())}"
        )
    
    def recommend(self, food_name, use_gpt=True):
        """
        음식에 맞는 와인을 추천합니다.
        
        Args:
            food_name: 음식 이름
            use_gpt: GPT API 사용 여부 (기본값: True)
        
        Returns:
            tuple: (추천 와인 리스트, 프로파일 정보)
                - 추천 와인 리스트: 각 딕셔너리는 {'name', 'sweet', 'acidity', 'body', 'tannin', 'distance'} 포함
                - 프로파일 정보: {'profile': [sweet, acidity, body, tannin], 'source': 'gpt' 또는 'fallback', 'description': 설명 문자열}
        """
        # 음식 프로파일 가져오기
        food_profile, profile_source, description = self.get_food_profile(food_name, use_gpt=use_gpt)
        
        # 가장 가까운 와인 찾기
        distances, indices = self.model.predict(food_profile)
        
        # 결과 구성
        recommendations = []
        for i, idx in enumerate(indices[0]):
            wine = self.df.iloc[idx]
            recommendations.append({
                'name': wine['name'],
                'sweet': int(wine['sweet']),
                'acidity': int(wine['acidity']),
                'body': int(wine['body']),
                'tannin': int(wine['tannin']),
                'price': float(wine['price']),
                'abv': float(wine['abv']) if pd.notna(wine['abv']) else None,
                'type': wine['type'] if 'type' in wine and pd.notna(wine['type']) else None,
                'nation': wine['nation'] if 'nation' in wine and pd.notna(wine['nation']) else None,
                'year': int(wine['year']) if pd.notna(wine['year']) else None,
                'distance': float(distances[0][i])
            })
        
        profile_info = {
            'profile': food_profile,
            'source': profile_source,
            'description': description
        }
        
        return recommendations, profile_info
    
    def get_available_foods(self):
        """
        사용 가능한 음식 목록을 반환합니다.
        
        Returns:
            list: 음식 이름 리스트
        """
        return list(FOOD_PROFILES.keys())

