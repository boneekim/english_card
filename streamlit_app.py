import streamlit as st
import sqlite3
import pandas as pd
import time
from gtts import gTTS
import io
import base64
from PIL import Image
import requests
from streamlit_autorefresh import st_autorefresh
import os
from typing import List, Dict, Tuple, Optional

# 페이지 설정
st.set_page_config(
    page_title="아이 연령별 단어 카드",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터베이스 초기화
def init_database():
    """데이터베이스 테이블 초기화"""
    conn = sqlite3.connect('word_cards.db')
    c = conn.cursor()
    
    # 단어 카드 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS word_cards (
            id TEXT PRIMARY KEY,
            word TEXT NOT NULL,
            translation TEXT,
            image_url TEXT,
            audio_text TEXT,
            age_group INTEGER NOT NULL
        )
    ''')
    
    # 사용자 진행상황 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            card_id TEXT PRIMARY KEY,
            is_favorite BOOLEAN DEFAULT FALSE,
            is_learned BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def load_word_data():
    """초기 단어 데이터 로드"""
    word_data = [
        # 3세 단어들
        {'id': '3-1', 'word': '사과', 'translation': 'Apple', 'image_url': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&h=400&fit=crop', 'audio_text': '사과', 'age_group': 3},
        {'id': '3-2', 'word': '강아지', 'translation': 'Dog', 'image_url': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=400&fit=crop', 'audio_text': '강아지', 'age_group': 3},
        {'id': '3-3', 'word': '고양이', 'translation': 'Cat', 'image_url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop', 'audio_text': '고양이', 'age_group': 3},
        {'id': '3-4', 'word': '자동차', 'translation': 'Car', 'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=400&fit=crop', 'audio_text': '자동차', 'age_group': 3},
        {'id': '3-5', 'word': '공', 'translation': 'Ball', 'image_url': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400&h=400&fit=crop', 'audio_text': '공', 'age_group': 3},
        
        # 4세 단어들
        {'id': '4-1', 'word': '나비', 'translation': 'Butterfly', 'image_url': 'https://images.unsplash.com/photo-1587613863926-42ba05f6f7c4?w=400&h=400&fit=crop', 'audio_text': '나비', 'age_group': 4},
        {'id': '4-2', 'word': '꽃', 'translation': 'Flower', 'image_url': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop', 'audio_text': '꽃', 'age_group': 4},
        {'id': '4-3', 'word': '집', 'translation': 'House', 'image_url': 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400&h=400&fit=crop', 'audio_text': '집', 'age_group': 4},
        {'id': '4-4', 'word': '해', 'translation': 'Sun', 'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop', 'audio_text': '해', 'age_group': 4},
        {'id': '4-5', 'word': '달', 'translation': 'Moon', 'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=400&h=400&fit=crop', 'audio_text': '달', 'age_group': 4},
        
        # 5세 단어들
        {'id': '5-1', 'word': '가족', 'translation': 'Family', 'image_url': 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=400&h=400&fit=crop', 'audio_text': '가족', 'age_group': 5},
        {'id': '5-2', 'word': '학교', 'translation': 'School', 'image_url': 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400&h=400&fit=crop', 'audio_text': '학교', 'age_group': 5},
        {'id': '5-3', 'word': '친구', 'translation': 'Friend', 'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop', 'audio_text': '친구', 'age_group': 5},
        {'id': '5-4', 'word': '책', 'translation': 'Book', 'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop', 'audio_text': '책', 'age_group': 5},
        {'id': '5-5', 'word': '연필', 'translation': 'Pencil', 'image_url': 'https://images.unsplash.com/photo-1514999024924-a1746e96ce28?w=400&h=400&fit=crop', 'audio_text': '연필', 'age_group': 5},
        
        # 6세 단어들
        {'id': '6-1', 'word': '숫자', 'translation': 'Number', 'image_url': 'https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=400&h=400&fit=crop', 'audio_text': '숫자', 'age_group': 6},
        {'id': '6-2', 'word': '색깔', 'translation': 'Color', 'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop', 'audio_text': '색깔', 'age_group': 6},
        {'id': '6-3', 'word': '모양', 'translation': 'Shape', 'image_url': 'https://images.unsplash.com/photo-1564951434112-64d74cc2a2d7?w=400&h=400&fit=crop', 'audio_text': '모양', 'age_group': 6},
        {'id': '6-4', 'word': '날씨', 'translation': 'Weather', 'image_url': 'https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?w=400&h=400&fit=crop', 'audio_text': '날씨', 'age_group': 6},
        {'id': '6-5', 'word': '계절', 'translation': 'Season', 'image_url': 'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400&h=400&fit=crop', 'audio_text': '계절', 'age_group': 6},
        
        # 7세 단어들
        {'id': '7-1', 'word': '생각', 'translation': 'Thought', 'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop', 'audio_text': '생각', 'age_group': 7},
        {'id': '7-2', 'word': '마음', 'translation': 'Heart/Mind', 'image_url': 'https://images.unsplash.com/photo-1494790108755-2616c04e3295?w=400&h=400&fit=crop', 'audio_text': '마음', 'age_group': 7},
        {'id': '7-3', 'word': '꿈', 'translation': 'Dream', 'image_url': 'https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=400&h=400&fit=crop', 'audio_text': '꿈', 'age_group': 7},
        {'id': '7-4', 'word': '희망', 'translation': 'Hope', 'image_url': 'https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=400&h=400&fit=crop', 'audio_text': '희망', 'age_group': 7},
        {'id': '7-5', 'word': '용기', 'translation': 'Courage', 'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop', 'audio_text': '용기', 'age_group': 7},
    ]
    
    conn = sqlite3.connect('word_cards.db')
    c = conn.cursor()
    
    # 데이터가 이미 있는지 확인
    c.execute("SELECT COUNT(*) FROM word_cards")
    if c.fetchone()[0] == 0:
        # 데이터 삽입
        for word in word_data:
            c.execute("""
                INSERT INTO word_cards (id, word, translation, image_url, audio_text, age_group)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (word['id'], word['word'], word['translation'], word['image_url'], word['audio_text'], word['age_group']))
    
    conn.commit()
    conn.close()

def get_cards_by_age(age_group: int, favorites_only: bool = False) -> List[Dict]:
    """연령별 카드 가져오기"""
    conn = sqlite3.connect('word_cards.db')
    
    if favorites_only:
        query = """
            SELECT wc.*, up.is_favorite, up.is_learned
            FROM word_cards wc
            JOIN user_progress up ON wc.id = up.card_id
            WHERE wc.age_group = ? AND up.is_favorite = 1
        """
    else:
        query = """
            SELECT wc.*, 
                   COALESCE(up.is_favorite, 0) as is_favorite,
                   COALESCE(up.is_learned, 0) as is_learned
            FROM word_cards wc
            LEFT JOIN user_progress up ON wc.id = up.card_id
            WHERE wc.age_group = ?
        """
    
    df = pd.read_sql_query(query, conn, params=(age_group,))
    conn.close()
    
    return df.to_dict('records')

def toggle_favorite(card_id: str):
    """즐겨찾기 토글"""
    conn = sqlite3.connect('word_cards.db')
    c = conn.cursor()
    
    # 현재 상태 확인
    c.execute("SELECT is_favorite FROM user_progress WHERE card_id = ?", (card_id,))
    result = c.fetchone()
    
    if result:
        new_state = not result[0]
        c.execute("UPDATE user_progress SET is_favorite = ? WHERE card_id = ?", (new_state, card_id))
    else:
        c.execute("INSERT INTO user_progress (card_id, is_favorite) VALUES (?, 1)", (card_id,))
    
    conn.commit()
    conn.close()

def toggle_learned(card_id: str):
    """학습완료 토글"""
    conn = sqlite3.connect('word_cards.db')
    c = conn.cursor()
    
    # 현재 상태 확인
    c.execute("SELECT is_learned FROM user_progress WHERE card_id = ?", (card_id,))
    result = c.fetchone()
    
    if result:
        new_state = not result[0]
        c.execute("UPDATE user_progress SET is_learned = ? WHERE card_id = ?", (new_state, card_id))
    else:
        c.execute("INSERT INTO user_progress (card_id, is_learned) VALUES (?, 1)", (card_id,))
    
    conn.commit()
    conn.close()

def generate_audio(text: str) -> str:
    """TTS로 오디오 생성 및 base64 인코딩"""
    try:
        tts = gTTS(text=text, lang='ko')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        return audio_base64
    except Exception as e:
        st.error(f"음성 생성 오류: {e}")
        return ""

def display_word_card(card: Dict, container):
    """단어 카드 표시"""
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # 이미지 표시
            try:
                response = requests.get(card['image_url'])
                img = Image.open(io.BytesIO(response.content))
                st.image(img, use_container_width=True, caption=f"{card['word']} ({card['translation']})")
            except Exception as e:
                st.error(f"이미지 로드 실패: {e}")
                st.text("🖼️ 이미지를 불러올 수 없습니다")
            
            # 단어 표시
            st.markdown(f"<h1 style='text-align: center; color: #4A90E2; font-size: 48px;'>{card['word']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #666; font-style: italic;'>{card['translation']}</h3>", unsafe_allow_html=True)
            
            # 버튼들
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("🔊 음성듣기", key=f"audio_{card['id']}"):
                    audio_base64 = generate_audio(card['audio_text'])
                    if audio_base64:
                        audio_html = f"""
                        <audio autoplay>
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                        """
                        st.markdown(audio_html, unsafe_allow_html=True)
            
            with col_btn2:
                fav_emoji = "⭐" if card.get('is_favorite') else "☆"
                if st.button(f"{fav_emoji} 즐겨찾기", key=f"fav_{card['id']}"):
                    toggle_favorite(card['id'])
                    st.rerun()
            
            with col_btn3:
                learned_emoji = "✅" if card.get('is_learned') else "□"
                if st.button(f"{learned_emoji} 외웠어요", key=f"learned_{card['id']}"):
                    toggle_learned(card['id'])
                    st.rerun()

# 메인 앱
def main():
    # 데이터베이스 초기화
    init_database()
    load_word_data()
    
    # 사이드바
    with st.sidebar:
        st.title("📚 설정")
        
        # 연령 선택
        selected_age = st.selectbox(
            "아이 연령",
            options=[3, 4, 5, 6, 7],
            format_func=lambda x: f"{x}세",
            key="age_selector"
        )
        
        # 즐겨찾기만 보기
        show_favorites_only = st.checkbox("⭐ 즐겨찾기만 보기")
        
        # 슬라이드 설정
        st.subheader("🎮 슬라이드 설정")
        auto_play = st.checkbox("자동 재생", value=False)
        slide_speed = st.slider("슬라이드 속도 (초)", min_value=1, max_value=10, value=2)
        
        # 진행 상황 리셋
        if st.button("🔄 진행상황 초기화"):
            conn = sqlite3.connect('word_cards.db')
            c = conn.cursor()
            c.execute("DELETE FROM user_progress")
            conn.commit()
            conn.close()
            st.success("진행상황이 초기화되었습니다!")
            st.rerun()
    
    # 메인 컨텐츠
    st.title(f"🎯 {selected_age}세 단어 카드")
    
    # 카드 데이터 가져오기
    cards = get_cards_by_age(selected_age, show_favorites_only)
    
    if not cards:
        st.warning("표시할 카드가 없습니다!")
        return
    
    # 세션 상태 초기화
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    
    # 현재 인덱스가 카드 수를 초과하지 않도록 조정
    if st.session_state.current_index >= len(cards):
        st.session_state.current_index = 0
    
    # 자동 재생 설정
    if auto_play:
        # 자동 새로고침 설정
        st_autorefresh(interval=slide_speed * 1000, key="autorefresh")
        st.session_state.current_index = (st.session_state.current_index + 1) % len(cards)
    
    # 네비게이션 버튼
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("⬅️ 이전", use_container_width=True):
            st.session_state.current_index = (st.session_state.current_index - 1) % len(cards)
            st.rerun()
    
    with col_info:
        st.markdown(f"<h4 style='text-align: center;'>{st.session_state.current_index + 1} / {len(cards)}</h4>", unsafe_allow_html=True)
    
    with col_next:
        if st.button("➡️ 다음", use_container_width=True):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(cards)
            st.rerun()
    
    # 현재 카드 표시
    current_card = cards[st.session_state.current_index]
    card_container = st.container()
    display_word_card(current_card, card_container)
    
    # 진행 상황 표시
    st.subheader("📊 학습 진행 상황")
    learned_count = sum(1 for card in cards if card.get('is_learned'))
    favorite_count = sum(1 for card in cards if card.get('is_favorite'))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("전체 카드", len(cards))
    with col2:
        st.metric("✅ 외운 카드", learned_count)
    with col3:
        st.metric("⭐ 즐겨찾기", favorite_count)
    
    # 진행률 바
    if len(cards) > 0:
        progress = learned_count / len(cards)
        st.progress(progress)
        st.caption(f"학습 완료율: {progress:.1%}")

if __name__ == "__main__":
    main() 