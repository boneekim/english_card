import streamlit as st
import requests
from urllib.parse import quote
import time
import random

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
        padding: 0;
        width: 100%;
    }
    .card-container {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        border: 3px solid #e2e8f0;
        margin: 20px auto;
        max-width: 450px;
        width: 100%;
    }
    .card-image-container {
        width: 100%;
        max-width: 320px;
        height: 240px;
        margin: 0 auto 20px auto;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f7fafc;
    }
    .card-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }
    .card-text {
        font-size: 24px;
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 25px;
        text-align: center;
    }
    .korean-text {
        color: #4a5568;
        display: block;
        margin-bottom: 10px;
        font-size: 28px;
        font-weight: bold;
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
        margin-bottom: 10px;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 20px;
        font-weight: bold;
        margin: 5px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    .audio-button {
        margin: 15px auto;
        text-align: center;
    }
    /* 이미지 로딩 상태 */
    .image-loading {
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, #f7fafc, #edf2f7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: #718096;
        border-radius: 10px;
    }
    /* 메인 컨테이너 중앙 정렬 */
    .main-content {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
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

# 카테고리별 단어 목록 (이미지 검색 키워드 포함)
WORD_LISTS = {
    'animals': [
        {'korean': '강아지', 'english': 'dog', 'search_terms': ['cute dog', 'puppy', 'golden retriever']},
        {'korean': '고양이', 'english': 'cat', 'search_terms': ['cute cat', 'kitten', 'orange cat']},
        {'korean': '토끼', 'english': 'rabbit', 'search_terms': ['white rabbit', 'bunny', 'cute rabbit']},
        {'korean': '코끼리', 'english': 'elephant', 'search_terms': ['baby elephant', 'elephant family', 'african elephant']},
        {'korean': '사자', 'english': 'lion', 'search_terms': ['lion cub', 'male lion', 'lion family']},
        {'korean': '호랑이', 'english': 'tiger', 'search_terms': ['tiger face', 'siberian tiger', 'tiger cub']},
        {'korean': '원숭이', 'english': 'monkey', 'search_terms': ['cute monkey', 'baby monkey', 'chimpanzee']},
        {'korean': '곰', 'english': 'bear', 'search_terms': ['brown bear', 'polar bear', 'bear cub']},
        {'korean': '새', 'english': 'bird', 'search_terms': ['colorful bird', 'parrot', 'canary']},
        {'korean': '물고기', 'english': 'fish', 'search_terms': ['tropical fish', 'goldfish', 'clownfish']},
        {'korean': '말', 'english': 'horse', 'search_terms': ['white horse', 'brown horse', 'horse running']},
        {'korean': '소', 'english': 'cow', 'search_terms': ['farm cow', 'black white cow', 'dairy cow']},
        {'korean': '돼지', 'english': 'pig', 'search_terms': ['pink pig', 'farm pig', 'cute piglet']},
        {'korean': '양', 'english': 'sheep', 'search_terms': ['fluffy sheep', 'white sheep', 'lamb']},
        {'korean': '닭', 'english': 'chicken', 'search_terms': ['farm chicken', 'rooster', 'hen with chicks']},
        {'korean': '오리', 'english': 'duck', 'search_terms': ['yellow duck', 'mallard duck', 'duckling']},
        {'korean': '펭귄', 'english': 'penguin', 'search_terms': ['emperor penguin', 'penguin family', 'cute penguin']},
        {'korean': '기린', 'english': 'giraffe', 'search_terms': ['tall giraffe', 'baby giraffe', 'giraffe eating']},
        {'korean': '얼룩말', 'english': 'zebra', 'search_terms': ['zebra stripes', 'zebra herd', 'baby zebra']},
        {'korean': '개구리', 'english': 'frog', 'search_terms': ['green frog', 'tree frog', 'cute frog']}
    ],
    'vehicles': [
        {'korean': '자동차', 'english': 'car', 'search_terms': ['red car', 'family car', 'modern car']},
        {'korean': '버스', 'english': 'bus', 'search_terms': ['school bus', 'city bus', 'yellow bus']},
        {'korean': '기차', 'english': 'train', 'search_terms': ['passenger train', 'steam train', 'high speed train']},
        {'korean': '비행기', 'english': 'airplane', 'search_terms': ['passenger airplane', 'boeing 747', 'commercial aircraft']},
        {'korean': '배', 'english': 'ship', 'search_terms': ['cruise ship', 'cargo ship', 'sailing boat']},
        {'korean': '자전거', 'english': 'bicycle', 'search_terms': ['red bicycle', 'mountain bike', 'kids bicycle']},
        {'korean': '오토바이', 'english': 'motorcycle', 'search_terms': ['sports motorcycle', 'harley davidson', 'racing bike']},
        {'korean': '트럭', 'english': 'truck', 'search_terms': ['delivery truck', 'pickup truck', 'semi truck']},
        {'korean': '택시', 'english': 'taxi', 'search_terms': ['yellow taxi', 'city taxi', 'cab']},
        {'korean': '앰뷸런스', 'english': 'ambulance', 'search_terms': ['emergency ambulance', 'medical vehicle', 'rescue ambulance']},
        {'korean': '소방차', 'english': 'fire truck', 'search_terms': ['red fire truck', 'fire engine', 'emergency vehicle']},
        {'korean': '경찰차', 'english': 'police car', 'search_terms': ['police patrol car', 'cop car', 'police vehicle']},
        {'korean': '헬리콥터', 'english': 'helicopter', 'search_terms': ['rescue helicopter', 'military helicopter', 'news helicopter']},
        {'korean': '지하철', 'english': 'subway', 'search_terms': ['subway train', 'metro train', 'underground train']},
        {'korean': '스쿠터', 'english': 'scooter', 'search_terms': ['electric scooter', 'vespa scooter', 'kick scooter']},
        {'korean': '로켓', 'english': 'rocket', 'search_terms': ['space rocket', 'nasa rocket', 'rocket launch']},
        {'korean': '요트', 'english': 'yacht', 'search_terms': ['luxury yacht', 'sailing yacht', 'motor yacht']},
        {'korean': '잠수함', 'english': 'submarine', 'search_terms': ['military submarine', 'yellow submarine', 'underwater vessel']},
        {'korean': '스케이트보드', 'english': 'skateboard', 'search_terms': ['skateboard deck', 'skateboard tricks', 'street skateboard']},
        {'korean': '롤러스케이트', 'english': 'roller skates', 'search_terms': ['roller skating', 'quad skates', 'inline skates']}
    ],
    'food': [
        {'korean': '사과', 'english': 'apple', 'search_terms': ['red apple', 'green apple', 'fresh apple']},
        {'korean': '바나나', 'english': 'banana', 'search_terms': ['yellow banana', 'ripe banana', 'banana bunch']},
        {'korean': '오렌지', 'english': 'orange', 'search_terms': ['fresh orange', 'orange slice', 'citrus orange']},
        {'korean': '딸기', 'english': 'strawberry', 'search_terms': ['fresh strawberry', 'ripe strawberry', 'strawberry close up']},
        {'korean': '포도', 'english': 'grape', 'search_terms': ['purple grapes', 'green grapes', 'grape cluster']},
        {'korean': '수박', 'english': 'watermelon', 'search_terms': ['watermelon slice', 'fresh watermelon', 'red watermelon']},
        {'korean': '빵', 'english': 'bread', 'search_terms': ['fresh bread', 'whole wheat bread', 'artisan bread']},
        {'korean': '우유', 'english': 'milk', 'search_terms': ['glass of milk', 'fresh milk', 'dairy milk']},
        {'korean': '치즈', 'english': 'cheese', 'search_terms': ['cheddar cheese', 'swiss cheese', 'cheese slices']},
        {'korean': '달걀', 'english': 'egg', 'search_terms': ['chicken eggs', 'brown eggs', 'fresh eggs']},
        {'korean': '쌀', 'english': 'rice', 'search_terms': ['white rice', 'cooked rice', 'rice grains']},
        {'korean': '면', 'english': 'noodles', 'search_terms': ['pasta noodles', 'ramen noodles', 'italian pasta']},
        {'korean': '고기', 'english': 'meat', 'search_terms': ['grilled meat', 'beef steak', 'cooked meat']},
        {'korean': '생선', 'english': 'fish', 'search_terms': ['grilled fish', 'salmon fillet', 'cooked fish']},
        {'korean': '야채', 'english': 'vegetables', 'search_terms': ['fresh vegetables', 'mixed vegetables', 'healthy vegetables']},
        {'korean': '당근', 'english': 'carrot', 'search_terms': ['orange carrot', 'fresh carrot', 'baby carrots']},
        {'korean': '토마토', 'english': 'tomato', 'search_terms': ['red tomato', 'fresh tomato', 'cherry tomato']},
        {'korean': '감자', 'english': 'potato', 'search_terms': ['russet potato', 'fresh potato', 'baked potato']},
        {'korean': '아이스크림', 'english': 'ice cream', 'search_terms': ['vanilla ice cream', 'chocolate ice cream', 'ice cream cone']},
        {'korean': '케이크', 'english': 'cake', 'search_terms': ['birthday cake', 'chocolate cake', 'layer cake']}
    ],
    'colors': [
        {'korean': '빨간색', 'english': 'red', 'search_terms': ['red color', 'bright red', 'red background']},
        {'korean': '파란색', 'english': 'blue', 'search_terms': ['blue color', 'sky blue', 'blue background']},
        {'korean': '노란색', 'english': 'yellow', 'search_terms': ['yellow color', 'bright yellow', 'yellow background']},
        {'korean': '초록색', 'english': 'green', 'search_terms': ['green color', 'forest green', 'green background']},
        {'korean': '주황색', 'english': 'orange', 'search_terms': ['orange color', 'bright orange', 'orange background']},
        {'korean': '보라색', 'english': 'purple', 'search_terms': ['purple color', 'violet purple', 'purple background']},
        {'korean': '분홍색', 'english': 'pink', 'search_terms': ['pink color', 'hot pink', 'pink background']},
        {'korean': '갈색', 'english': 'brown', 'search_terms': ['brown color', 'chocolate brown', 'brown background']},
        {'korean': '검은색', 'english': 'black', 'search_terms': ['black color', 'pure black', 'black background']},
        {'korean': '하얀색', 'english': 'white', 'search_terms': ['white color', 'pure white', 'white background']},
        {'korean': '회색', 'english': 'gray', 'search_terms': ['gray color', 'light gray', 'gray background']},
        {'korean': '금색', 'english': 'gold', 'search_terms': ['gold color', 'metallic gold', 'golden background']},
        {'korean': '은색', 'english': 'silver', 'search_terms': ['silver color', 'metallic silver', 'silver background']},
        {'korean': '하늘색', 'english': 'sky blue', 'search_terms': ['sky blue color', 'light blue', 'azure blue']},
        {'korean': '연두색', 'english': 'light green', 'search_terms': ['light green color', 'lime green', 'pale green']},
        {'korean': '남색', 'english': 'navy', 'search_terms': ['navy blue color', 'dark blue', 'navy background']},
        {'korean': '청록색', 'english': 'turquoise', 'search_terms': ['turquoise color', 'cyan blue', 'teal color']},
        {'korean': '자주색', 'english': 'violet', 'search_terms': ['violet color', 'deep purple', 'violet background']},
        {'korean': '크림색', 'english': 'cream', 'search_terms': ['cream color', 'off white', 'cream background']},
        {'korean': '베이지색', 'english': 'beige', 'search_terms': ['beige color', 'tan color', 'beige background']}
    ],
    'family': [
        {'korean': '엄마', 'english': 'mom', 'search_terms': ['happy mother', 'mom with child', 'loving mother']},
        {'korean': '아빠', 'english': 'dad', 'search_terms': ['happy father', 'dad with child', 'loving father']},
        {'korean': '할머니', 'english': 'grandmother', 'search_terms': ['smiling grandmother', 'elderly woman', 'grandma portrait']},
        {'korean': '할아버지', 'english': 'grandfather', 'search_terms': ['smiling grandfather', 'elderly man', 'grandpa portrait']},
        {'korean': '형', 'english': 'older brother', 'search_terms': ['teenage boy', 'young man', 'brother portrait']},
        {'korean': '누나', 'english': 'older sister', 'search_terms': ['teenage girl', 'young woman', 'sister portrait']},
        {'korean': '동생', 'english': 'younger sibling', 'search_terms': ['young child', 'little kid', 'cute child']},
        {'korean': '아기', 'english': 'baby', 'search_terms': ['cute baby', 'smiling baby', 'infant portrait']},
        {'korean': '이모', 'english': 'aunt', 'search_terms': ['young woman', 'friendly woman', 'aunt portrait']},
        {'korean': '삼촌', 'english': 'uncle', 'search_terms': ['young man', 'friendly man', 'uncle portrait']},
        {'korean': '사촌', 'english': 'cousin', 'search_terms': ['children together', 'kids playing', 'young relatives']},
        {'korean': '가족', 'english': 'family', 'search_terms': ['happy family', 'family portrait', 'family together']},
        {'korean': '부모님', 'english': 'parents', 'search_terms': ['mother father together', 'happy parents', 'parent couple']},
        {'korean': '자녀', 'english': 'children', 'search_terms': ['happy children', 'kids together', 'brother sister']},
        {'korean': '아들', 'english': 'son', 'search_terms': ['young boy', 'little boy', 'son portrait']},
        {'korean': '딸', 'english': 'daughter', 'search_terms': ['young girl', 'little girl', 'daughter portrait']},
        {'korean': '손자', 'english': 'grandson', 'search_terms': ['little boy', 'young grandson', 'cute boy']},
        {'korean': '손녀', 'english': 'granddaughter', 'search_terms': ['little girl', 'young granddaughter', 'cute girl']},
        {'korean': '조카', 'english': 'nephew/niece', 'search_terms': ['young child', 'nephew niece', 'little relative']},
        {'korean': '친구', 'english': 'friend', 'search_terms': ['children friends', 'kids playing together', 'best friends']}
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

def get_image_url(word_data, index):
    """각 단어별로 고유한 이미지 URL 생성"""
    search_term = random.choice(word_data['search_terms'])
    
    # 여러 이미지 소스 사용
    image_sources = [
        f"https://images.unsplash.com/photo-1574158622682-e40e69881006?w=320&h=240&fit=crop&auto=format&q=80&fm=jpg&crop=faces&facepad=3&ixid={search_term.replace(' ', '')}{index}",
        f"https://images.unsplash.com/photo-1544568100-847a948585b9?w=320&h=240&fit=crop&auto=format&q=80&fm=jpg&crop=entropy&ixid={search_term.replace(' ', '')}{index}",
        f"https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=320&h=240&fit=crop&auto=format&q=80&fm=jpg&crop=entropy&ixid={search_term.replace(' ', '')}{index}",
        f"https://picsum.photos/320/240?random={abs(hash(search_term + str(index))) % 1000}",
        f"https://via.placeholder.com/320x240/4299e1/ffffff?text={word_data['english'].replace(' ', '+')}"
    ]
    
    return random.choice(image_sources)

def get_cards(category, card_count):
    """카테고리별 단어 카드 생성"""
    words = WORD_LISTS.get(category, [])
    
    if len(words) < card_count:
        selected_words = (words * ((card_count // len(words)) + 1))[:card_count]
    else:
        selected_words = words[:card_count]
    
    cards = []
    for i, word in enumerate(selected_words):
        image_url = get_image_url(word, i)
        
        cards.append({
            'korean': word['korean'],
            'english': word['english'],
            'image_url': image_url,
            'search_terms': word['search_terms'],
            'id': i
        })
    
    return cards

def create_tts_html(word):
    """TTS를 위한 HTML/JavaScript 생성"""
    html_code = f"""
    <div class="audio-button">
        <button onclick="speakWord()" style="
            background: linear-gradient(45deg, #48bb78, #38a169);
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">🔊</button>
        <script>
        function speakWord() {{
            if ('speechSynthesis' in window) {{
                // 기존 음성 중지
                speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance('{word}');
                utterance.lang = 'en-US';
                utterance.rate = 0.7;
                utterance.pitch = 1.0;
                utterance.volume = 0.8;
                speechSynthesis.speak(utterance);
            }} else {{
                alert('이 브라우저는 음성 합성을 지원하지 않습니다.');
            }}
        }}
        </script>
    </div>
    """
    return html_code

# 메인 헤더 - 중앙 정렬 보장
st.markdown(
    '<div style="width: 100%; display: flex; justify-content: center;">'
    '<h1 class="main-header">🌟 아이들을 위한 영어 카드 ��</h1>'
    '</div>', 
    unsafe_allow_html=True
)

# 사이드바 설정
with st.sidebar:
    st.header("📚 학습 설정")
    
    age_group = st.selectbox("아이 연령", list(AGE_GROUPS.keys()))
    category = st.selectbox("카테고리", list(CATEGORIES.keys()))
    card_count = st.slider("카드 수", 5, 20, 10)
    
    if st.button("🚀 카드 시작하기", use_container_width=True):
        st.session_state.cards = get_cards(CATEGORIES[category], card_count)
        st.session_state.current_index = 0
        st.session_state.memorized_cards = set()
        st.session_state.difficult_cards = set()
        st.rerun()
    
    st.divider()
    
    # 자동 슬라이드 설정
    st.header("⏰ 자동 슬라이드")
    auto_slide = st.toggle("🔄 자동 슬라이드 활성화")
    if auto_slide:
        slide_interval = st.slider("슬라이드 간격(초)", 2, 10, 4)
    
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
        
        # 진행률 표시 - 중앙 정렬
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f'<div class="progress-text">{current_filtered_index + 1} / {len(filtered_indices)}</div>',
                unsafe_allow_html=True
            )
            progress = (current_filtered_index + 1) / len(filtered_indices)
            st.progress(progress)
        
        # 카드 표시 - 완전 중앙 정렬
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            
            # 이미지 표시 - 컨테이너 내부에서 중앙 정렬
            st.markdown('<div class="card-image-container">', unsafe_allow_html=True)
            try:
                st.image(
                    current_card['image_url'], 
                    use_container_width=True
                )
            except:
                st.markdown('<div class="image-loading">📷 이미지 로딩중...</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
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
            st.components.v1.html(create_tts_html(current_card['english']), height=80)
            
            # 액션 버튼들
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                memorized_text = "✅ 외웠어요!" if actual_index in st.session_state.memorized_cards else "☑️ 외웠어요"
                if st.button(memorized_text, key=f"memorized_{actual_index}", use_container_width=True):
                    if actual_index in st.session_state.memorized_cards:
                        st.session_state.memorized_cards.remove(actual_index)
                    else:
                        st.session_state.memorized_cards.add(actual_index)
                        st.session_state.difficult_cards.discard(actual_index)
                    st.rerun()
            
            with col_b:
                difficult_text = "❌ 어려워요!" if actual_index in st.session_state.difficult_cards else "⭕ 어려워요"
                if st.button(difficult_text, key=f"difficult_{actual_index}", use_container_width=True):
                    if actual_index in st.session_state.difficult_cards:
                        st.session_state.difficult_cards.remove(actual_index)
                    else:
                        st.session_state.difficult_cards.add(actual_index)
                        st.session_state.memorized_cards.discard(actual_index)
                    st.rerun()
            
            with col_c:
                if st.button("🔄 새로고침", key=f"refresh_{actual_index}", use_container_width=True):
                    # 새로운 이미지 URL 생성
                    new_image_url = get_image_url({
                        'english': current_card['english'],
                        'search_terms': current_card['search_terms']
                    }, actual_index + random.randint(1000, 9999))
                    st.session_state.cards[actual_index]['image_url'] = new_image_url
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 네비게이션 버튼 - 중앙 정렬
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        
        with col2:
            if st.button("⬅️ 이전", disabled=(current_filtered_index == 0), use_container_width=True):
                st.session_state.current_index = max(0, st.session_state.current_index - 1)
                st.rerun()
        
        with col4:
            if st.button("다음 ➡️", disabled=(current_filtered_index == len(filtered_indices) - 1), use_container_width=True):
                st.session_state.current_index = min(len(filtered_indices) - 1, st.session_state.current_index + 1)
                st.rerun()
        
        # 자동 슬라이드 기능
        if auto_slide and len(filtered_indices) > 1:
            time.sleep(slide_interval)
            if current_filtered_index < len(filtered_indices) - 1:
                st.session_state.current_index += 1
            else:
                st.session_state.current_index = 0
            st.rerun()
        
        # 통계 표시
        with st.sidebar:
            st.header("📊 학습 통계")
            total_cards = len(st.session_state.cards)
            memorized_count = len(st.session_state.memorized_cards)
            difficult_count = len(st.session_state.difficult_cards)
            
            st.metric("외운 카드", f"{memorized_count}개", f"{memorized_count/total_cards*100:.1f}%")
            st.metric("어려운 카드", f"{difficult_count}개", f"{difficult_count/total_cards*100:.1f}%")
            st.metric("총 카드", f"{total_cards}개")
            
            if st.button("🔄 통계 초기화", use_container_width=True):
                st.session_state.memorized_cards = set()
                st.session_state.difficult_cards = set()
                st.rerun()
    
    else:
        st.info(f"선택한 필터 '{show_filter}'에 해당하는 카드가 없습니다.")

else:
    st.info("설정을 선택하고 '🚀 카드 시작하기' 버튼을 눌러주세요! 👆")
    
    # 기능 소개
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## ✨ 주요 기능
        
        - 🎯 **연령별 맞춤**: 3-5세, 6-8세, 9-12세
        - 📚 **카테고리별**: 동물, 탈것, 음식, 색깔, 가족
        - 🔊 **음성 읽기**: 영어 단어 발음 듣기
        - ✅ **학습 관리**: 외운 카드와 어려운 카드 분류
        - 📊 **통계 추적**: 학습 진행상황 실시간 확인
        - 📱 **반응형**: 모바일, 태블릿, PC 모두 지원
        """)
    
    with col2:
        st.markdown("""
        ## 🎮 사용법
        
        1. **왼쪽 사이드바**에서 연령과 카테고리 선택
        2. **'🚀 카드 시작하기'** 버튼 클릭
        3. **🔊 버튼**으로 영어 발음 듣기
        4. **✅ 외웠어요** 버튼으로 학습 완료 표시
        5. **❌ 어려워요** 버튼으로 복습 필요 표시
        6. **⬅️➡️ 버튼**으로 카드 넘기기
        7. **🔄 새로고침**으로 다른 이미지 보기
        """)
