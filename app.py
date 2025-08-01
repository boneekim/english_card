from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
import json
import requests
from urllib.parse import quote

load_dotenv()

app = Flask(__name__)

# OpenAI API 키 설정 (환경변수에서 읽기)
openai.api_key = os.getenv('OPENAI_API_KEY')

# 카테고리 및 연령대 설정
CATEGORIES = {
    '동물': 'animals',
    '탈것': 'vehicles', 
    '음식': 'food',
    '색깔': 'colors',
    '가족': 'family',
    '자연': 'nature',
    '직업': 'jobs',
    '집안': 'home',
    '운동': 'sports',
    '학용품': 'school supplies'
}

AGE_GROUPS = {
    '3-5세': '3-5 years old',
    '6-8세': '6-8 years old', 
    '9-12세': '9-12 years old'
}

# 카테고리별 단어 목록
WORD_LISTS = {
    'animals': [
        {'korean': '강아지', 'english': 'dog'},
        {'korean': '고양이', 'english': 'cat'},
        {'korean': '토끼', 'english': 'rabbit'},
        {'korean': '코끼리', 'english': 'elephant'},
        {'korean': '사자', 'english': 'lion'},
        {'korean': '호랑이', 'english': 'tiger'},
        {'korean': '원숭이', 'english': 'monkey'},
        {'korean': '곰', 'english': 'bear'},
        {'korean': '새', 'english': 'bird'},
        {'korean': '물고기', 'english': 'fish'},
        {'korean': '말', 'english': 'horse'},
        {'korean': '소', 'english': 'cow'},
        {'korean': '돼지', 'english': 'pig'},
        {'korean': '양', 'english': 'sheep'},
        {'korean': '닭', 'english': 'chicken'},
        {'korean': '오리', 'english': 'duck'},
        {'korean': '펭귄', 'english': 'penguin'},
        {'korean': '기린', 'english': 'giraffe'},
        {'korean': '얼룩말', 'english': 'zebra'},
        {'korean': '개구리', 'english': 'frog'}
    ],
    'vehicles': [
        {'korean': '자동차', 'english': 'car'},
        {'korean': '버스', 'english': 'bus'},
        {'korean': '기차', 'english': 'train'},
        {'korean': '비행기', 'english': 'airplane'},
        {'korean': '배', 'english': 'ship'},
        {'korean': '자전거', 'english': 'bicycle'},
        {'korean': '오토바이', 'english': 'motorcycle'},
        {'korean': '트럭', 'english': 'truck'},
        {'korean': '택시', 'english': 'taxi'},
        {'korean': '앰뷸런스', 'english': 'ambulance'},
        {'korean': '소방차', 'english': 'fire truck'},
        {'korean': '경찰차', 'english': 'police car'},
        {'korean': '헬리콥터', 'english': 'helicopter'},
        {'korean': '지하철', 'english': 'subway'},
        {'korean': '스쿠터', 'english': 'scooter'},
        {'korean': '로켓', 'english': 'rocket'},
        {'korean': '요트', 'english': 'yacht'},
        {'korean': '잠수함', 'english': 'submarine'},
        {'korean': '스케이트보드', 'english': 'skateboard'},
        {'korean': '롤러스케이트', 'english': 'roller skates'}
    ],
    'food': [
        {'korean': '사과', 'english': 'apple'},
        {'korean': '바나나', 'english': 'banana'},
        {'korean': '오렌지', 'english': 'orange'},
        {'korean': '딸기', 'english': 'strawberry'},
        {'korean': '포도', 'english': 'grape'},
        {'korean': '수박', 'english': 'watermelon'},
        {'korean': '빵', 'english': 'bread'},
        {'korean': '우유', 'english': 'milk'},
        {'korean': '치즈', 'english': 'cheese'},
        {'korean': '달걀', 'english': 'egg'},
        {'korean': '쌀', 'english': 'rice'},
        {'korean': '면', 'english': 'noodles'},
        {'korean': '고기', 'english': 'meat'},
        {'korean': '생선', 'english': 'fish'},
        {'korean': '야채', 'english': 'vegetables'},
        {'korean': '당근', 'english': 'carrot'},
        {'korean': '토마토', 'english': 'tomato'},
        {'korean': '감자', 'english': 'potato'},
        {'korean': '아이스크림', 'english': 'ice cream'},
        {'korean': '케이크', 'english': 'cake'}
    ],
    'colors': [
        {'korean': '빨간색', 'english': 'red'},
        {'korean': '파란색', 'english': 'blue'},
        {'korean': '노란색', 'english': 'yellow'},
        {'korean': '초록색', 'english': 'green'},
        {'korean': '주황색', 'english': 'orange'},
        {'korean': '보라색', 'english': 'purple'},
        {'korean': '분홍색', 'english': 'pink'},
        {'korean': '갈색', 'english': 'brown'},
        {'korean': '검은색', 'english': 'black'},
        {'korean': '하얀색', 'english': 'white'},
        {'korean': '회색', 'english': 'gray'},
        {'korean': '금색', 'english': 'gold'},
        {'korean': '은색', 'english': 'silver'},
        {'korean': '하늘색', 'english': 'sky blue'},
        {'korean': '연두색', 'english': 'light green'},
        {'korean': '남색', 'english': 'navy'},
        {'korean': '청록색', 'english': 'turquoise'},
        {'korean': '자주색', 'english': 'violet'},
        {'korean': '크림색', 'english': 'cream'},
        {'korean': '베이지색', 'english': 'beige'}
    ],
    'family': [
        {'korean': '엄마', 'english': 'mom'},
        {'korean': '아빠', 'english': 'dad'},
        {'korean': '할머니', 'english': 'grandmother'},
        {'korean': '할아버지', 'english': 'grandfather'},
        {'korean': '형', 'english': 'older brother'},
        {'korean': '누나', 'english': 'older sister'},
        {'korean': '동생', 'english': 'younger sibling'},
        {'korean': '아기', 'english': 'baby'},
        {'korean': '이모', 'english': 'aunt'},
        {'korean': '삼촌', 'english': 'uncle'},
        {'korean': '사촌', 'english': 'cousin'},
        {'korean': '가족', 'english': 'family'},
        {'korean': '부모님', 'english': 'parents'},
        {'korean': '자녀', 'english': 'children'},
        {'korean': '아들', 'english': 'son'},
        {'korean': '딸', 'english': 'daughter'},
        {'korean': '손자', 'english': 'grandson'},
        {'korean': '손녀', 'english': 'granddaughter'},
        {'korean': '조카', 'english': 'nephew/niece'},
        {'korean': '친구', 'english': 'friend'}
    ]
}

@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORIES, age_groups=AGE_GROUPS)

@app.route('/get_cards', methods=['POST'])
def get_cards():
    data = request.json
    category = data.get('category')
    age_group = data.get('age_group')
    card_count = int(data.get('card_count', 20))
    
    # 해당 카테고리의 단어 목록 가져오기
    words = WORD_LISTS.get(category, [])
    
    # 요청된 카드 수만큼 선택 (중복 가능)
    if len(words) < card_count:
        # 단어가 부족하면 반복해서 선택
        selected_words = (words * ((card_count // len(words)) + 1))[:card_count]
    else:
        selected_words = words[:card_count]
    
    cards = []
    for word in selected_words:
        # Unsplash API를 사용하여 실제 이미지 URL 생성
        image_url = f"https://source.unsplash.com/400x300/?{quote(word['english'])}"
        
        cards.append({
            'korean': word['korean'],
            'english': word['english'],
            'image_url': image_url,
            'id': len(cards)
        })
    
    return jsonify({'cards': cards})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
