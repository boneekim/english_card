import streamlit as st
import requests
from urllib.parse import quote
import time

# 페이지 설정
st.set_page_config(
    page_title="🌟 아이들을 위한 영어 카드",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #4a5568;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .card-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 3px solid #e2e8f0;
        margin: 20px 0;
    }
    .card-text {
        font-size: 24px;
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 20px;
    }
    .korean-text {
        color: #4a5568;
        display: block;
        margin-bottom: 10px;
        font-size: 26px;
    }
    .english-text {
        color: #667eea;
        font-size: 32px;
        font-weight: bold;
    }
    .progress-text {
        font-size: 18px;
        font-weight: bold;
        color: #4a5568;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 카테고리 및 연령대 설정
CATEGORIES = {
    '동물': 'animals',
    '탈것': 'vehicles', 
    '음식': 'food',
    '색깔': 'colors',
    '가족': 'family'
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

# 세션 상태 초기화
if 'cards' not in st.session_state:
    st.session_state.cards = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'memorized_cards' not in st.session_state:
    st.session_state.memorized_cards = set()
if 'difficult_cards' not in st.session_state:
    st.session_state.difficult_cards = set()

def get_cards(category, card_count):
    """카테고리별 단어 카드 생성"""
    words = WORD_LISTS.get(category, [])
    
    if len(words) < card_count:
        selected_words = (words * ((card_count // len(words)) + 1))[:card_count]
    else:
        selected_words = words[:card_count]
    
    cards = []
    for i, word in enumerate(selected_words):
        image_url = f"https://source.unsplash.com/400x300/?{quote(word['english'])}"
        cards.append({
            'korean': word['korean'],
            'english': word['english'],
            'image_url': image_url,
            'id': i
        })
    
    return cards

def create_tts_html(word):
    """TTS를 위한 HTML/JavaScript 생성"""
    html_code = f"""
    <div>
        <button onclick="speakWord()" style="
            background: linear-gradient(45deg, #48bb78, #38a169);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        ">🔊</button>
        <script>
        function speakWord() {{
            if ('speechSynthesis' in window) {{
                const utterance = new SpeechSynthesisUtterance('{word}');
                utterance.lang = 'en-US';
                utterance.rate = 0.8;
                utterance.pitch = 1.1;
                speechSynthesis.speak(utterance);
            }} else {{
                alert('이 브라우저는 음성 합성을 지원하지 않습니다.');
            }}
        }}
        </script>
    </div>
    """
    return html_code

# 메인 헤더
st.markdown('<h1 class="main-header">🌟 아이들을 위한 영어 카드 🌟</h1>', unsafe_allow_html=True)

# 사이드바 설정
with st.sidebar:
    st.header("📚 학습 설정")
    
    age_group = st.selectbox("아이 연령", list(AGE_GROUPS.keys()))
    category = st.selectbox("카테고리", list(CATEGORIES.keys()))
    slide_time = st.slider("자동슬라이드 시간(초)", 1, 10, 3)
    card_count = st.slider("카드 수", 5, 50, 20)
    
    if st.button("🚀 카드 시작하기", use_container_width=True):
        st.session_state.cards = get_cards(CATEGORIES[category], card_count)
        st.session_state.current_index = 0
        st.session_state.memorized_cards = set()
        st.session_state.difficult_cards = set()
        st.rerun()
    
    st.divider()
    
    # 필터 옵션
    st.header("🔍 필터")
    show_filter = st.selectbox(
        "보기 옵션",
        ["전체 카드", "외운 카드", "어려운 카드"]
    )

# 메인 콘텐츠
if st.session_state.cards:
    # 필터링된 카드 인덱스 계산
    if show_filter == "외운 카드":
        filtered_indices = [i for i in range(len(st.session_state.cards)) 
                          if i in st.session_state.memorized_cards]
    elif show_filter == "어려운 카드":
        filtered_indices = [i for i in range(len(st.session_state.cards)) 
                          if i in st.session_state.difficult_cards]
    else:
        filtered_indices = list(range(len(st.session_state.cards)))
    
    if filtered_indices:
        # 현재 인덱스가 필터된 범위를 벗어나면 조정
        if st.session_state.current_index >= len(filtered_indices):
            st.session_state.current_index = 0
        
        current_filtered_index = st.session_state.current_index
        actual_index = filtered_indices[current_filtered_index]
        current_card = st.session_state.cards[actual_index]
        
        # 진행률 표시
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f'<div class="progress-text">{current_filtered_index + 1} / {len(filtered_indices)}</div>',
                unsafe_allow_html=True
            )
            progress = (current_filtered_index + 1) / len(filtered_indices)
            st.progress(progress)
        
        # 카드 표시
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # 이미지 표시
            try:
                st.image(current_card['image_url'], use_container_width=True, caption=current_card['english'])
            except:
                st.info(f"📷 이미지: {current_card['english']}")
            
            # 텍스트 표시
            st.markdown(
                f'''
                <div class="card-text">
                    <span class="korean-text">{current_card['korean']}</span>
                    <span class="english-text">{current_card['english']}</span>
                </div>
                ''',
                unsafe_allow_html=True
            )
            
            # 음성 버튼
            st.components.v1.html(create_tts_html(current_card['english']), height=70)
            
            # 액션 버튼들
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                memorized_text = "✅ 외웠어요" if actual_index in st.session_state.memorized_cards else "☑️ 외웠어요"
                if st.button(memorized_text, key=f"memorized_{actual_index}"):
                    if actual_index in st.session_state.memorized_cards:
                        st.session_state.memorized_cards.remove(actual_index)
                    else:
                        st.session_state.memorized_cards.add(actual_index)
                        st.session_state.difficult_cards.discard(actual_index)
                    st.rerun()
            
            with col_b:
                difficult_text = "❌ 어려워요" if actual_index in st.session_state.difficult_cards else "⭕ 어려워요"
                if st.button(difficult_text, key=f"difficult_{actual_index}"):
                    if actual_index in st.session_state.difficult_cards:
                        st.session_state.difficult_cards.remove(actual_index)
                    else:
                        st.session_state.difficult_cards.add(actual_index)
                        st.session_state.memorized_cards.discard(actual_index)
                    st.rerun()
            
            with col_c:
                if st.button("🔄 새로고침", key=f"refresh_{actual_index}"):
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 네비게이션 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ 이전", disabled=(current_filtered_index == 0)):
                st.session_state.current_index = max(0, st.session_state.current_index - 1)
                st.rerun()
        
        with col3:
            if st.button("다음 ➡️", disabled=(current_filtered_index == len(filtered_indices) - 1)):
                st.session_state.current_index = min(len(filtered_indices) - 1, st.session_state.current_index + 1)
                st.rerun()
        
        # 통계 표시
        with st.sidebar:
            st.header("📊 학습 통계")
            st.write(f"외운 카드: {len(st.session_state.memorized_cards)}개")
            st.write(f"어려운 카드: {len(st.session_state.difficult_cards)}개")
            st.write(f"총 카드: {len(st.session_state.cards)}개")
            
            if st.button("🔄 통계 초기화"):
                st.session_state.memorized_cards = set()
                st.session_state.difficult_cards = set()
                st.rerun()
    
    else:
        st.info(f"선택한 필터에 해당하는 카드가 없습니다.")

else:
    st.info("설정을 선택하고 '카드 시작하기' 버튼을 눌러주세요! 👆")
    
    # 기능 소개
    st.markdown("""
    ## ✨ 주요 기능
    
    - 🎯 **연령별 맞춤**: 3-5세, 6-8세, 9-12세
    - 📚 **카테고리별**: 동물, 탈것, 음식, 색깔, 가족
    - 🔊 **음성 읽기**: 영어 단어 발음 듣기
    - ✅ **학습 관리**: 외운 카드와 어려운 카드 분류
    - 📱 **반응형**: 모바일, 태블릿, PC 모두 지원
    
    ## 🎮 사용법
    1. 왼쪽 사이드바에서 연령과 카테고리 선택
    2. '🚀 카드 시작하기' 버튼 클릭
    3. 🔊 버튼으로 음성 듣기
    4. ✅ 외웠어요, ❌ 어려워요 버튼으로 학습 관리
    5. ⬅️➡️ 버튼으로 카드 넘기기
    """)
