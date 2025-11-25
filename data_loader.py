"""
데이터 로드 및 전처리 모듈
CSV 파일을 읽고, taste profile 컬럼을 숫자로 변환합니다.
"""

import pandas as pd
import re


def preprocess_taste_profile(value):
    """
    taste profile 문자열을 숫자로 변환
    예: "SWEET1" -> 1, "ACIDITY4" -> 4
    
    Args:
        value: 문자열 값 (예: "SWEET1", "ACIDITY4")
    
    Returns:
        int: 추출된 숫자 값, 변환 실패 시 None
    """
    if pd.isna(value) or value == '':
        return None
    
    # 정규표현식으로 숫자 추출
    match = re.search(r'(\d+)', str(value))
    if match:
        return int(match.group(1))
    return None


def load_wine_data(file_path="cleansingWine.csv"):
    """
    CSV 파일을 로드합니다.
    
    Args:
        file_path: CSV 파일 경로
    
    Returns:
        pd.DataFrame: 로드된 데이터프레임
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        raise Exception(f"파일 읽기 중 오류 발생: {str(e)}")


def prepare_features(df):
    """
    필요한 컬럼을 선택하고 taste profile을 전처리합니다.
    
    Args:
        df: 원본 데이터프레임
    
    Returns:
        pd.DataFrame: 전처리된 데이터프레임 (name, sweet, acidity, body, tannin 포함)
    """
    # 필요한 컬럼만 선택
    required_columns = ['name', 'sweet', 'acidity', 'body', 'tannin']
    
    # 컬럼이 존재하는지 확인
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"필수 컬럼이 없습니다: {missing_columns}")
    
    # 필요한 컬럼만 선택
    df_processed = df[required_columns].copy()
    
    # taste profile 컬럼을 숫자로 변환
    for column in ['sweet', 'acidity', 'body', 'tannin']:
        df_processed[column] = df_processed[column].apply(preprocess_taste_profile)
    
    # 결측치가 있는 행 제거
    df_processed = df_processed.dropna(subset=['sweet', 'acidity', 'body', 'tannin'])
    
    # name이 비어있는 행 제거
    df_processed = df_processed.dropna(subset=['name'])
    
    # 빈 문자열 name 제거
    df_processed = df_processed[df_processed['name'].astype(str).str.strip() != '']
    
    return df_processed.reset_index(drop=True)

