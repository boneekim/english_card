import streamlit as st
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        position: relative;
    }
    .card-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        border-radius: 10px;
    }
    .emoji-display {
        font-size: 120px;
        text-align: center;
        line-height: 1;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
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

# 카테고리별 단어 목록 (실제 관련 이미지 URL 포함)
WORD_LISTS = {
    'animals': [
        {'korean': '강아지', 'english': 'dog', 'emoji': '🐶', 'image_urls': [
            'https://images.unsplash.com/photo-1552053831-71594a27632d?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1517849845537-4d257902454a?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '고양이', 'english': 'cat', 'emoji': '🐱', 'image_urls': [
            'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1513245543132-31f507417b26?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '토끼', 'english': 'rabbit', 'emoji': '🐰', 'image_urls': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1545156521-77bd85671d30?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '코끼리', 'english': 'elephant', 'emoji': '🐘', 'image_urls': [
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1459262838948-3e2de6c1ec80?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '사자', 'english': 'lion', 'emoji': '🦁', 'image_urls': [
            'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1552410260-0fd9b577afe6?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=320&h=240&fit=crop&auto=format'
        ]}
    ],
    'vehicles': [
        {'korean': '자동차', 'english': 'car', 'emoji': '��', 'image_urls': [
            'https://images.unsplash.com/photo-1549317336-206569e8475c?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1494976688153-ca3ce09cd2b5?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '버스', 'english': 'bus', 'emoji': '🚌', 'image_urls': [
            'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '기차', 'english': 'train', 'emoji': '🚂', 'image_urls': [
            'https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '비행기', 'english': 'airplane', 'emoji': '✈️', 'image_urls': [
            'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1564508709742-b05cb90cd4c8?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '배', 'english': 'ship', 'emoji': '🚢', 'image_urls': [
            'https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1565124019334-2ce5f09eb8a0?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1520637836862-4d197d17c7a4?w=320&h=240&fit=crop&auto=format'
        ]}
    ],
    'food': [
        {'korean': '사과', 'english': 'apple', 'emoji': '🍎', 'image_urls': [
            'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '바나나', 'english': 'banana', 'emoji': '🍌', 'image_urls': [
            'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '오렌지', 'english': 'orange', 'emoji': '🍊', 'image_urls': [
            'https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1557800636-894a64c1696f?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1582979512210-99b6a53386f9?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '딸기', 'english': 'strawberry', 'emoji': '🍓', 'image_urls': [
            'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1518635017498-87297b2dce5a?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1558818047-87b467c0b4c5?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '포도', 'english': 'grape', 'emoji': '🍇', 'image_urls': [
            'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1423483641154-5411ec9c0ddf?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1574856344991-aaa31b6f4ce3?w=320&h=240&fit=crop&auto=format'
        ]}
    ],
    'colors': [
        {'korean': '빨간색', 'english': 'red', 'emoji': '🔴', 'image_urls': [
            'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1604519331816-e555c3c4e6d9?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '파란색', 'english': 'blue', 'emoji': '🔵', 'image_urls': [
            'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '노란색', 'english': 'yellow', 'emoji': '🟡', 'image_urls': [
            'https://images.unsplash.com/photo-1558618047-5c8c75ca7d13?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1471879832106-c7ab9e0cee23?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '초록색', 'english': 'green', 'emoji': '🟢', 'image_urls': [
            'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '보라색', 'english': 'purple', 'emoji': '🟣', 'image_urls': [
            'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=320&h=240&fit=crop&auto=format'
        ]}
    ],
    'family': [
        {'korean': '가족', 'english': 'family', 'emoji': '👨‍👩‍👧‍👦', 'image_urls': [
            'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '엄마', 'english': 'mom', 'emoji': '👩', 'image_urls': [
            'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1494790108755-2616c9c8fcdc?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '아빠', 'english': 'dad', 'emoji': '👨', 'image_urls': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '아기', 'english': 'baby', 'emoji': '👶', 'image_urls': [
            'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1562542132-8555e1b583f3?w=320&h=240&fit=crop&auto=format'
        ]},
        {'korean': '친구', 'english': 'friend', 'emoji': '👫', 'image_urls': [
            'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?w=320&h=240&fit=crop&auto=format',
            'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=320&h=240&fit=crop&auto=format'
        ]}
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
if 'image_mode' not in st.session_state:
    st.session_state.image_mode = 'photo'

def get_cards(category, card_count):
    """카테고리별 단어 카드 생성"""
    words = WORD_LISTS.get(category, [])
    
    if len(words) < card_count:
        selected_words = (words * ((card_count // len(words)) + 1))[:card_count]
    else:
        selected_words = words[:card_count]
    
    cards = []
    for i, word in enumerate(selected_words):
        # 각 단어별로 관련 이미지 중 하나를 랜덤 선택
        image_url = random.choice(word['image_urls']) if word.get('image_urls') else None
        
        cards.append({
            'korean': word['korean'],
            'english': word['english'],
            'emoji': word['emoji'],
            'image_url': image_url,
            'image_urls': word.get('image_urls', []),
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
                speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance('{word}');
                utterance.lang = 'en-US';
                utterance.rate = 0.7;
                utterance.pitch = 1.0;
                utterance.volume = 0.8;
                speechSynthesis.speak(utterance);
            }}
        }}
        </script>
    </div>
    """
    return html_code

def render_card_image(card):
    """카드 이미지 렌더링"""
    if st.session_state.image_mode == 'emoji':
        return f'<div class="emoji-display">{card["emoji"]}</div>'
    else:
        if card.get('image_url'):
            return f'''
                <img src="{card['image_url']}" 
                     alt="{card['english']}" 
                     class="card-image"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                     loading="lazy">
                <div class="emoji-display" style="display: none;">{card["emoji"]}</div>
            '''
        else:
            return f'<div class="emoji-display">{card["emoji"]}</div>'

# 메인 헤더
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
    card_count = st.slider("카드 수", 3, min(len(WORD_LISTS.get(CATEGORIES.get(category, 'animals'), [])), 10), 5)
    
    st.divider()
    
    # 이미지 모드 선택
    st.header("🖼️ 이미지 모드")
    image_mode = st.radio(
        "표시 방식 선택",
        ["📸 실사 사진", "😊 이모지"],
        index=0 if st.session_state.image_mode == 'photo' else 1
    )
    
    if image_mode == "📸 실사 사진":
        st.session_state.image_mode = 'photo'
    else:
        st.session_state.image_mode = 'emoji'
    
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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            
            # 이미지 표시
            st.markdown('<div class="card-image-container">', unsafe_allow_html=True)
            st.markdown(render_card_image(current_card), unsafe_allow_html=True)
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
                    # 같은 단어의 다른 이미지로 변경
                    if current_card.get('image_urls') and st.session_state.image_mode == 'photo':
                        new_image_url = random.choice(current_card['image_urls'])
                        st.session_state.cards[actual_index]['image_url'] = new_image_url
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 네비게이션 버튼
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
        - 🖼️ **관련 이미지**: 각 단어와 정확히 일치하는 실사 사진
        - 🔊 **음성 읽기**: 영어 단어 발음 듣기
        - ✅ **학습 관리**: 외운 카드와 어려운 카드 분류
        - 📊 **통계 추적**: 학습 진행상황 실시간 확인
        """)
    
    with col2:
        st.markdown("""
        ## 🎮 사용법
        
        1. **왼쪽 사이드바**에서 연령과 카테고리 선택
        2. **이미지 모드** 선택 (실사 사진 또는 이모지)
        3. **'🚀 카드 시작하기'** 버튼 클릭
        4. **🔊 버튼**으로 영어 발음 듣기
        5. **✅ 외웠어요** 버튼으로 학습 완료 표시
        6. **❌ 어려워요** 버튼으로 복습 필요 표시
        7. **🔄 새로고침**으로 같은 단어의 다른 사진 보기
        """)
