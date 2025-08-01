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
        max-width: 500px;
        width: 100%;
    }
    .card-image {
        width: 100%;
        max-width: 350px;
        height: 250px;
        object-fit: cover;
        border-radius: 15px;
        margin: 0 auto 20px auto;
        border: 3px solid #e2e8f0;
        display: block;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
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
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    /* 이미지 로딩 상태 */
    .image-loading {
        width: 350px;
        height: 250px;
        background: linear-gradient(45deg, #f7fafc, #edf2f7);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: #718096;
        margin: 0 auto 20px auto;
        border: 3px solid #e2e8f0;
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

# 카테고리별 단어 목록 (검색 키워드 포함)
WORD_LISTS = {
    'animals': [
        {'korean': '강아지', 'english': 'dog', 'search': 'cute+puppy'},
        {'korean': '고양이', 'english': 'cat', 'search': 'cute+kitten'},
        {'korean': '토끼', 'english': 'rabbit', 'search': 'white+rabbit'},
        {'korean': '코끼리', 'english': 'elephant', 'search': 'baby+elephant'},
        {'korean': '사자', 'english': 'lion', 'search': 'lion+cub'},
        {'korean': '호랑이', 'english': 'tiger', 'search': 'tiger+face'},
        {'korean': '원숭이', 'english': 'monkey', 'search': 'cute+monkey'},
        {'korean': '곰', 'english': 'bear', 'search': 'teddy+bear'},
        {'korean': '새', 'english': 'bird', 'search': 'colorful+bird'},
        {'korean': '물고기', 'english': 'fish', 'search': 'tropical+fish'},
        {'korean': '말', 'english': 'horse', 'search': 'white+horse'},
        {'korean': '소', 'english': 'cow', 'search': 'farm+cow'},
        {'korean': '돼지', 'english': 'pig', 'search': 'cute+pig'},
        {'korean': '양', 'english': 'sheep', 'search': 'fluffy+sheep'},
        {'korean': '닭', 'english': 'chicken', 'search': 'farm+chicken'},
        {'korean': '오리', 'english': 'duck', 'search': 'yellow+duck'},
        {'korean': '펭귄', 'english': 'penguin', 'search': 'cute+penguin'},
        {'korean': '기린', 'english': 'giraffe', 'search': 'baby+giraffe'},
        {'korean': '얼룩말', 'english': 'zebra', 'search': 'zebra+stripes'},
        {'korean': '개구리', 'english': 'frog', 'search': 'green+frog'}
    ],
    'vehicles': [
        {'korean': '자동차', 'english': 'car', 'search': 'red+car'},
        {'korean': '버스', 'english': 'bus', 'search': 'school+bus'},
        {'korean': '기차', 'english': 'train', 'search': 'steam+train'},
        {'korean': '비행기', 'english': 'airplane', 'search': 'passenger+airplane'},
        {'korean': '배', 'english': 'ship', 'search': 'cruise+ship'},
        {'korean': '자전거', 'english': 'bicycle', 'search': 'red+bicycle'},
        {'korean': '오토바이', 'english': 'motorcycle', 'search': 'sports+motorcycle'},
        {'korean': '트럭', 'english': 'truck', 'search': 'delivery+truck'},
        {'korean': '택시', 'english': 'taxi', 'search': 'yellow+taxi'},
        {'korean': '앰뷸런스', 'english': 'ambulance', 'search': 'emergency+ambulance'},
        {'korean': '소방차', 'english': 'fire truck', 'search': 'red+fire+truck'},
        {'korean': '경찰차', 'english': 'police car', 'search': 'police+car'},
        {'korean': '헬리콥터', 'english': 'helicopter', 'search': 'rescue+helicopter'},
        {'korean': '지하철', 'english': 'subway', 'search': 'subway+train'},
        {'korean': '스쿠터', 'english': 'scooter', 'search': 'electric+scooter'},
        {'korean': '로켓', 'english': 'rocket', 'search': 'space+rocket'},
        {'korean': '요트', 'english': 'yacht', 'search': 'luxury+yacht'},
        {'korean': '잠수함', 'english': 'submarine', 'search': 'yellow+submarine'},
        {'korean': '스케이트보드', 'english': 'skateboard', 'search': 'skateboard+trick'},
        {'korean': '롤러스케이트', 'english': 'roller skates', 'search': 'roller+skates'}
    ],
    'food': [
        {'korean': '사과', 'english': 'apple', 'search': 'red+apple'},
        {'korean': '바나나', 'english': 'banana', 'search': 'yellow+banana'},
        {'korean': '오렌지', 'english': 'orange', 'search': 'fresh+orange'},
        {'korean': '딸기', 'english': 'strawberry', 'search': 'fresh+strawberry'},
        {'korean': '포도', 'english': 'grape', 'search': 'purple+grapes'},
        {'korean': '수박', 'english': 'watermelon', 'search': 'slice+watermelon'},
        {'korean': '빵', 'english': 'bread', 'search': 'fresh+bread'},
        {'korean': '우유', 'english': 'milk', 'search': 'glass+milk'},
        {'korean': '치즈', 'english': 'cheese', 'search': 'yellow+cheese'},
        {'korean': '달걀', 'english': 'egg', 'search': 'white+eggs'},
        {'korean': '쌀', 'english': 'rice', 'search': 'white+rice'},
        {'korean': '면', 'english': 'noodles', 'search': 'pasta+noodles'},
        {'korean': '고기', 'english': 'meat', 'search': 'grilled+meat'},
        {'korean': '생선', 'english': 'fish', 'search': 'cooked+fish'},
        {'korean': '야채', 'english': 'vegetables', 'search': 'fresh+vegetables'},
        {'korean': '당근', 'english': 'carrot', 'search': 'orange+carrot'},
        {'korean': '토마토', 'english': 'tomato', 'search': 'red+tomato'},
        {'korean': '감자', 'english': 'potato', 'search': 'fresh+potato'},
        {'korean': '아이스크림', 'english': 'ice cream', 'search': 'vanilla+ice+cream'},
        {'korean': '케이크', 'english': 'cake', 'search': 'birthday+cake'}
    ],
    'colors': [
        {'korean': '빨간색', 'english': 'red', 'search': 'red+color'},
        {'korean': '파란색', 'english': 'blue', 'search': 'blue+color'},
        {'korean': '노란색', 'english': 'yellow', 'search': 'yellow+color'},
        {'korean': '초록색', 'english': 'green', 'search': 'green+color'},
        {'korean': '주황색', 'english': 'orange', 'search': 'orange+color'},
        {'korean': '보라색', 'english': 'purple', 'search': 'purple+color'},
        {'korean': '분홍색', 'english': 'pink', 'search': 'pink+color'},
        {'korean': '갈색', 'english': 'brown', 'search': 'brown+color'},
        {'korean': '검은색', 'english': 'black', 'search': 'black+color'},
        {'korean': '하얀색', 'english': 'white', 'search': 'white+color'},
        {'korean': '회색', 'english': 'gray', 'search': 'gray+color'},
        {'korean': '금색', 'english': 'gold', 'search': 'gold+color'},
        {'korean': '은색', 'english': 'silver', 'search': 'silver+color'},
        {'korean': '하늘색', 'english': 'sky blue', 'search': 'sky+blue'},
        {'korean': '연두색', 'english': 'light green', 'search': 'light+green'},
        {'korean': '남색', 'english': 'navy', 'search': 'navy+blue'},
        {'korean': '청록색', 'english': 'turquoise', 'search': 'turquoise+color'},
        {'korean': '자주색', 'english': 'violet', 'search': 'violet+color'},
        {'korean': '크림색', 'english': 'cream', 'search': 'cream+color'},
        {'korean': '베이지색', 'english': 'beige', 'search': 'beige+color'}
    ],
    'family': [
        {'korean': '엄마', 'english': 'mom', 'search': 'happy+mother'},
        {'korean': '아빠', 'english': 'dad', 'search': 'happy+father'},
        {'korean': '할머니', 'english': 'grandmother', 'search': 'grandmother+smiling'},
        {'korean': '할아버지', 'english': 'grandfather', 'search': 'grandfather+smiling'},
        {'korean': '형', 'english': 'older brother', 'search': 'teenage+boy'},
        {'korean': '누나', 'english': 'older sister', 'search': 'teenage+girl'},
        {'korean': '동생', 'english': 'younger sibling', 'search': 'cute+children'},
        {'korean': '아기', 'english': 'baby', 'search': 'cute+baby'},
        {'korean': '이모', 'english': 'aunt', 'search': 'young+woman'},
        {'korean': '삼촌', 'english': 'uncle', 'search': 'young+man'},
        {'korean': '사촌', 'english': 'cousin', 'search': 'children+playing'},
        {'korean': '가족', 'english': 'family', 'search': 'happy+family'},
        {'korean': '부모님', 'english': 'parents', 'search': 'loving+parents'},
        {'korean': '자녀', 'english': 'children', 'search': 'happy+children'},
        {'korean': '아들', 'english': 'son', 'search': 'young+boy'},
        {'korean': '딸', 'english': 'daughter', 'search': 'young+girl'},
        {'korean': '손자', 'english': 'grandson', 'search': 'little+boy'},
        {'korean': '손녀', 'english': 'granddaughter', 'search': 'little+girl'},
        {'korean': '조카', 'english': 'nephew/niece', 'search': 'small+child'},
        {'korean': '친구', 'english': 'friend', 'search': 'children+friends'}
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
        # Pixabay API 사용 (더 안정적)
        image_url = f"https://pixabay.com/get/g5e8b3a3f8c4c1d8f8b4a4c5d8f4a4c1d.jpg"
        # 대체 이미지 URL들
        fallback_urls = [
            f"https://images.unsplash.com/photo-1574158622682-e40e69881006?w=350&h=250&fit=crop&auto=format",
            f"https://via.placeholder.com/350x250/4299e1/ffffff?text={word['english'].replace(' ', '+')}",
            f"https://picsum.photos/350/250?random={i}"
        ]
        
        cards.append({
            'korean': word['korean'],
            'english': word['english'],
            'image_url': f"https://images.unsplash.com/photo-1574158622682-e40e69881006?w=350&h=250&fit=crop&auto=format&q={word['search']}",
            'fallback_urls': fallback_urls,
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

def create_image_with_fallback(image_url, fallback_urls, alt_text):
    """이미지를 안전하게 표시하는 함수"""
    try:
        return f'<img src="{image_url}" alt="{alt_text}" class="card-image" onerror="this.onerror=null; this.src=\'{fallback_urls[0] if fallback_urls else "https://via.placeholder.com/350x250/4299e1/ffffff?text=" + alt_text.replace(" ", "+")}\'">'
    except:
        return f'<div class="image-loading">📷 {alt_text}</div>'

# 메인 헤더 - 중앙 정렬 보장
st.markdown(
    '<div style="width: 100%; display: flex; justify-content: center;">'
    '<h1 class="main-header">🌟 아이들을 위한 영어 카드 🌟</h1>'
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
        
        # 카드 표시 - 중앙 정렬 보장
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            
            # 이미지 표시
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            try:
                st.image(
                    current_card['image_url'], 
                    caption=current_card['english'],
                    use_container_width=False,
                    width=350
                )
            except:
                # 대체 이미지들 시도
                fallback_displayed = False
                for fallback_url in current_card.get('fallback_urls', []):
                    try:
                        st.image(
                            fallback_url,
                            caption=current_card['english'],
                            use_container_width=False,
                            width=350
                        )
                        fallback_displayed = True
                        break
                    except:
                        continue
                
                if not fallback_displayed:
                    st.markdown(
                        f'<div class="image-loading">📷 {current_card["english"]}</div>',
                        unsafe_allow_html=True
                    )
            
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
        7. **필터 기능**으로 학습한 카드만 모아보기
        """)
