"""
GPT API를 사용하여 음식에 맞는 와인 프로파일을 생성하는 모듈
"""

import json
import os
from openai import OpenAI
import streamlit as st


# OpenAI API 키 (하드코딩)

def get_food_profile_from_gpt(food_name):
    """
    GPT API를 사용하여 음식에 맞는 와인 프로파일을 생성합니다.
    
    Args:
        food_name: 음식 이름
    
    Returns:
        tuple: (프로파일 리스트, 설명 문자열)
            - 프로파일: [sweet, acidity, body, tannin]
                - sweet: 1-5 (단맛 정도)
                - acidity: 1-4 (산도 정도)
                - body: 1-5 (바디감)
                - tannin: 1-5 (탄닌감)
            - 설명: 음식의 맛과 특징, 왜 이 프로파일을 추천하는지에 대한 설명
    
    Raises:
        Exception: API 호출 실패 시
    """
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OpenAI API Key가 설정되지 않았습니다.")

    client = OpenAI(api_key=api_key)
    #client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""당신은 와인 페어링 전문가입니다. 주어진 음식에 어울리는 와인의 맛 프로파일을 결정해주세요.

음식: {food_name}

⚠️ 중요: 음식의 맛 특성이 아니라, 이 음식에 어울리는 와인의 특성을 반환해야 합니다.
예를 들어, 달콤한 디저트라면 음식의 단맛이 아니라, 그 디저트와 잘 어울리는 와인의 단맛 정도를 평가해야 합니다.

다음 4가지 특성은 모두 "와인의 특성"입니다. 각각 숫자로 평가해주세요:
- sweet (와인의 단맛): 1-5 범위 (1=매우 드라이한 와인, 5=매우 달콤한 와인)
- acidity (와인의 산도): 1-4 범위 (1=낮은 산도의 와인, 4=높은 산도의 와인)
- body (와인의 바디감): 1-5 범위 (1=가벼운 바디의 와인, 5=풀 바디의 와인)
- tannin (와인의 탄닌감): 1-5 범위 (1=부드러운 탄닌의 와인, 5=강한 탄닌의 와인)

또한 이 음식의 맛과 특징, 그리고 왜 이 프로파일의 와인을 추천하는지 설명해주세요.

반드시 다음 JSON 형식으로만 응답해주세요:
{{
    "sweet": 숫자,
    "acidity": 숫자,
    "body": 숫자,
    "tannin": 숫자,
    "description": "이 음식의 맛과 특징, 왜 이 프로파일을 추천하는지에 대한 설명 (한국어로)"
}}

다른 설명 없이 JSON 형식만 응답해주세요."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 와인 페어링 전문가입니다. 음식의 특성이 아니라, 그 음식에 어울리는 와인의 특성(단맛, 산도, 바디, 탄닌)을 반환해야 합니다. 요청된 형식의 JSON만 응답합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        # 응답에서 JSON 추출
        content = response.choices[0].message.content.strip()
        
        # JSON 파싱 시도
        # JSON 코드 블록이 있는 경우 제거
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        profile_dict = json.loads(content)
        
        # 값 검증 및 반환
        sweet = int(profile_dict.get("sweet", 3))
        acidity = int(profile_dict.get("acidity", 3))
        body = int(profile_dict.get("body", 3))
        tannin = int(profile_dict.get("tannin", 3))
        description = profile_dict.get("description", "프로파일 설명을 가져올 수 없습니다.")
        
        # 범위 검증
        sweet = max(1, min(5, sweet))
        acidity = max(1, min(4, acidity))
        body = max(1, min(5, body))
        tannin = max(1, min(5, tannin))
        
        profile = [sweet, acidity, body, tannin]
        return profile, description
        
    except json.JSONDecodeError as e:
        raise Exception(f"GPT API 응답 파싱 오류: {str(e)}")
    except Exception as e:
        raise Exception(f"GPT API 호출 오류: {str(e)}")

