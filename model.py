"""
KNN 모델 모듈
StandardScaler와 NearestNeighbors를 사용한 와인 추천 모델
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


class WineKNNModel:
    """
    와인 추천을 위한 KNN 모델 클래스
    """
    
    def __init__(self, n_neighbors=5, metric='euclidean'):
        """
        모델 초기화
        
        Args:
            n_neighbors: 추천할 이웃 개수 (기본값: 5)
            metric: 거리 계산 방법 (기본값: 'euclidean')
        """
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.scaler = StandardScaler()
        self.model = NearestNeighbors(n_neighbors=n_neighbors, metric=metric)
        self.is_fitted = False
    
    def fit(self, X):
        """
        모델 학습
        
        Args:
            X: 학습 데이터 (numpy array 또는 pandas DataFrame)
                shape: (n_samples, n_features)
                features: [sweet, acidity, body, tannin]
        """
        # numpy array로 변환
        if hasattr(X, 'values'):
            X = X.values
        
        # StandardScaler로 정규화
        X_scaled = self.scaler.fit_transform(X)
        
        # KNN 모델 학습
        self.model.fit(X_scaled)
        self.is_fitted = True
    
    def transform(self, X):
        """
        입력 데이터를 정규화
        
        Args:
            X: 입력 데이터 (numpy array 또는 list)
                shape: (n_samples, n_features) 또는 (n_features,)
        
        Returns:
            numpy array: 정규화된 데이터
        """
        if not self.is_fitted:
            raise ValueError("모델이 학습되지 않았습니다. fit()을 먼저 호출하세요.")
        
        # 1D 배열인 경우 2D로 변환
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        return self.scaler.transform(X)
    
    def predict(self, X):
        """
        입력 프로파일과 가장 가까운 와인들을 찾습니다.
        
        Args:
            X: 입력 프로파일 (numpy array 또는 list)
                shape: (n_samples, n_features) 또는 (n_features,)
                features: [sweet, acidity, body, tannin]
        
        Returns:
            tuple: (distances, indices)
                - distances: 각 이웃까지의 거리 (shape: (n_samples, n_neighbors))
                - indices: 가장 가까운 와인의 인덱스 (shape: (n_samples, n_neighbors))
        """
        if not self.is_fitted:
            raise ValueError("모델이 학습되지 않았습니다. fit()을 먼저 호출하세요.")
        
        # 입력 데이터 정규화
        X_scaled = self.transform(X)
        
        # KNN으로 가장 가까운 이웃 찾기
        distances, indices = self.model.kneighbors(X_scaled)
        
        return distances, indices

