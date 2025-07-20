import streamlit as st
import pandas as pd
import time
from gtts import gTTS
import base64
from streamlit_autorefresh import st_autorefresh
import os
import json
import random
from typing import List, Dict, Tuple, Optional
from supabase import create_client, Client
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="아이 연령별 단어 카드",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Supabase 클라이언트 초기화
@st.cache_resource
def init_supabase():
    """Supabase 클라이언트 초기화"""
    try:
        # Streamlit Cloud의 secrets 또는 로컬 config 파일에서 설정 불러오기
        supabase_url = None
        supabase_key = None
        
        # 먼저 Streamlit Cloud secrets 시도
        try:
            if hasattr(st, 'secrets') and "SUPABASE_URL" in st.secrets:
                # Streamlit Cloud에서 실행 (secrets 사용)
                supabase_url = st.secrets["SUPABASE_URL"]
                supabase_key = st.secrets["SUPABASE_ANON_KEY"]
        except:
            pass
        
        # secrets가 없으면 로컬 config 파일 사용
        if not supabase_url:
            try:
                import supabase_config
                supabase_url = supabase_config.SUPABASE_URL
                supabase_key = supabase_config.SUPABASE_ANON_KEY
            except ImportError:
                st.error("❌ Streamlit Cloud에서는 Secrets에 SUPABASE_URL과 SUPABASE_ANON_KEY를 설정하거나, 로컬에서는 supabase_config.py 파일이 필요합니다.")
                st.info("📋 로컬 설정: supabase_config.py.example을 참고하여 설정하세요.")
                st.info("☁️ Streamlit Cloud 설정: App settings > Secrets에서 설정하세요.")
                st.stop()
            except AttributeError:
                st.error("❌ Supabase URL과 Key가 supabase_config.py에 설정되지 않았습니다.")
                st.stop()
    
        if not supabase_url or supabase_url == "https://your-project-ref.supabase.co":
            st.error("❌ 실제 Supabase URL을 설정해주세요.")
            st.stop()
    
        if not supabase_key or supabase_key == "your-anon-key-here":
            st.error("❌ 실제 Supabase Anon Key를 설정해주세요.")
            st.stop()
    
        try:
            supabase: Client = create_client(supabase_url, supabase_key)
            return supabase
        except Exception as e:
            st.error(f"❌ Supabase 연결 실패: {e}")
            st.stop()
    except Exception as e:
        st.error(f"❌ 설정 로드 실패: {e}")
        st.stop()

# OpenAI 클라이언트 초기화
@st.cache_resource
def init_openai():
    """OpenAI 클라이언트 초기화"""
    try:
        # OpenAI API 키 가져오기
        openai_key = None
        
        # 먼저 Streamlit Cloud secrets 시도
        try:
            if hasattr(st, 'secrets') and "OPENAI_API_KEY" in st.secrets:
                openai_key = st.secrets["OPENAI_API_KEY"]
        except:
            pass
        
        # secrets가 없으면 로컬 config 파일 시도
        if not openai_key:
            try:
                import supabase_config
                if hasattr(supabase_config, 'OPENAI_API_KEY'):
                    openai_key = supabase_config.OPENAI_API_KEY
            except:
                pass
        
        # 환경변수에서 시도
        if not openai_key:
            openai_key = os.getenv('OPENAI_API_KEY')
        
        if not openai_key:
            st.warning("⚠️ OpenAI API 키가 설정되지 않았습니다. 미리 준비된 단어들을 사용합니다.")
            return None
        
        return OpenAI(api_key=openai_key)
    except Exception as e:
        st.warning(f"⚠️ OpenAI 연결 실패: {e}. 미리 준비된 단어들을 사용합니다.")
        return None

def create_tables(supabase: Client):
    """데이터베이스 테이블 생성 (즐겨찾기만)"""
    try:
        # 즐겨찾기 테이블만 확인 - 더 간단한 방법으로 변경
        result = supabase.table('favorites').select('id').limit(1).execute()
        st.success("✅ 데이터베이스 연결 성공!")
        return True  # 테이블이 존재하고 접근 가능
    except Exception as e:
        error_message = str(e).lower()
        
        # 권한이나 접근 문제인 경우 - 계속 진행하도록 수정
        if ("permission" in error_message or 
            "policy" in error_message or 
            "rls" in error_message or
            "row level security" in error_message or
            "insufficient privilege" in error_message):
            st.warning("⚠️ 데이터베이스 접근 권한 문제가 있습니다. RLS 정책을 확인해주세요.")
            st.info("📋 Supabase Dashboard에서 다음 RLS 정책만 실행하세요:")
            
            rls_policy = """
-- RLS 정책 설정 (테이블이 이미 존재하는 경우)
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public access" ON favorites FOR ALL USING (true);
            """
            st.code(rls_policy, language='sql')
            st.warning("⚠️ 위 SQL 실행 후 새로고침하거나, 일단 앱을 계속 사용해보세요.")
            return True  # 일단 계속 진행
        else:
            st.info("📋 즐겨찾기 테이블을 생성합니다...")
            st.warning("⚠️ Supabase Dashboard에서 다음 SQL을 실행해주세요:")
            
            sql_create_tables = """
-- 즐겨찾기 테이블 (북마크한 단어들만 저장)
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    word TEXT NOT NULL,
    translation TEXT,
    image_url TEXT,
    age_group INTEGER NOT NULL,
    is_learned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS 정책 설정
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기/쓰기 가능
CREATE POLICY "Public access" ON favorites FOR ALL USING (true);
        """
        
        st.code(sql_create_tables, language='sql')
        st.info("💡 SQL 실행 후 브라우저를 새로고침하세요.")
        st.stop()
        
    return False  # 테이블 접근 불가

def generate_word_with_openai(openai_client: OpenAI, age_group: int) -> Dict:
    """OpenAI로 연령별 단어 생성"""
    try:
        age_descriptions = {
            3: "3세 유아를 위한 매우 간단하고 기본적인 단어 (동물, 과일, 장난감 등)",
            4: "4세 유아를 위한 일상생활 단어 (가족, 집, 자연 등)",
            5: "5세 어린이를 위한 사회생활 관련 단어 (학교, 친구, 활동 등)",
            6: "6세 어린이를 위한 개념어와 감정 표현 단어",
            7: "7세 어린이를 위한 추상적 개념과 가치관 관련 단어"
        }
        
        prompt = f"""
        {age_descriptions[age_group]}에 적합한 한국어 단어 1개와 영어 번역, 그리고 이미지 검색에 적합한 영어 키워드를 생성해주세요.
        
        JSON 형식으로 답변해주세요:
        {{
            "word": "한국어 단어",
            "translation": "영어 번역",
            "image_keyword": "이미지 검색용 영어 키워드"
        }}
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.8
        )
        
        content = response.choices[0].message.content.strip()
        # JSON 파싱
        import json
        word_data = json.loads(content)
        
        return {
            'word': word_data['word'],
            'translation': word_data['translation'],
            'image_keyword': word_data['image_keyword'],
            'age_group': age_group
        }
    except Exception as e:
        st.error(f"OpenAI 단어 생성 실패: {e}")
        return None

def get_fallback_words(age_group: int) -> List[Dict]:
    """OpenAI 사용 불가 시 미리 준비된 단어들"""
    fallback_data = {
        3: [
            {'word': '사과', 'translation': 'Apple', 'image_keyword': 'red apple fruit'},
            {'word': '강아지', 'translation': 'Dog', 'image_keyword': 'cute puppy dog'},
            {'word': '고양이', 'translation': 'Cat', 'image_keyword': 'cute kitten cat'},
            {'word': '자동차', 'translation': 'Car', 'image_keyword': 'colorful toy car'},
            {'word': '공', 'translation': 'Ball', 'image_keyword': 'colorful ball toy'},
        ],
        4: [
            {'word': '나비', 'translation': 'Butterfly', 'image_keyword': 'beautiful butterfly'},
            {'word': '꽃', 'translation': 'Flower', 'image_keyword': 'colorful flowers'},
            {'word': '집', 'translation': 'House', 'image_keyword': 'cute house home'},
            {'word': '해', 'translation': 'Sun', 'image_keyword': 'bright sun sunshine'},
            {'word': '달', 'translation': 'Moon', 'image_keyword': 'moon night sky'},
        ],
        5: [
            {'word': '가족', 'translation': 'Family', 'image_keyword': 'happy family'},
            {'word': '학교', 'translation': 'School', 'image_keyword': 'school building'},
            {'word': '친구', 'translation': 'Friend', 'image_keyword': 'children friends playing'},
            {'word': '책', 'translation': 'Book', 'image_keyword': 'colorful books'},
            {'word': '연필', 'translation': 'Pencil', 'image_keyword': 'colorful pencils'},
        ],
        6: [
            {'word': '숫자', 'translation': 'Number', 'image_keyword': 'colorful numbers'},
            {'word': '색깔', 'translation': 'Color', 'image_keyword': 'rainbow colors'},
            {'word': '모양', 'translation': 'Shape', 'image_keyword': 'geometric shapes'},
            {'word': '날씨', 'translation': 'Weather', 'image_keyword': 'weather icons'},
            {'word': '계절', 'translation': 'Season', 'image_keyword': 'four seasons'},
        ],
        7: [
            {'word': '생각', 'translation': 'Thought', 'image_keyword': 'child thinking'},
            {'word': '마음', 'translation': 'Heart', 'image_keyword': 'heart love'},
            {'word': '꿈', 'translation': 'Dream', 'image_keyword': 'child dreaming stars'},
            {'word': '희망', 'translation': 'Hope', 'image_keyword': 'hope light sunshine'},
            {'word': '용기', 'translation': 'Courage', 'image_keyword': 'brave child superhero'},
        ]
    }
    
    return fallback_data.get(age_group, fallback_data[3])

def search_unsplash_image(keyword: str) -> str:
    """Unsplash에서 이미지 검색"""
    try:
        # Unsplash Source API 사용 (API 키 불필요)
        # 키워드별로 랜덤 이미지 반환
        keyword_clean = keyword.replace(' ', ',')
        return f"https://source.unsplash.com/400x400/?{keyword_clean}"
        
    except Exception as e:
        # 기본 이미지 반환
        return "https://images.unsplash.com/photo-1560807707-b4d0d17ada03?w=400&h=400&fit=crop"

def generate_word_card(openai_client: OpenAI, age_group: int) -> Dict:
    """단어 카드 생성 (OpenAI + Unsplash)"""
    # OpenAI로 단어 생성 시도
    if openai_client:
        word_data = generate_word_with_openai(openai_client, age_group)
        if word_data:
            # 이미지 검색
            image_url = search_unsplash_image(word_data['image_keyword'])
            word_data['image_url'] = image_url
            word_data['id'] = f"generated_{random.randint(1000, 9999)}"
            return word_data
    
    # 폴백: 미리 준비된 단어 사용
    fallback_words = get_fallback_words(age_group)
    word_data = random.choice(fallback_words)
    word_data['image_url'] = search_unsplash_image(word_data['image_keyword'])
    word_data['id'] = f"fallback_{random.randint(1000, 9999)}"
    word_data['age_group'] = age_group
    
    return word_data

def get_favorites(supabase: Client, age_group: int) -> List[Dict]:
    """즐겨찾기한 단어들 가져오기"""
    try:
        result = supabase.table('favorites')\
            .select('*')\
            .eq('age_group', age_group)\
            .execute()
        
        favorites = []
        for item in result.data:
            favorites.append({
                'id': f"fav_{item['id']}",
                'word': item['word'],
                'translation': item['translation'],
                'image_url': item['image_url'],
                'age_group': item['age_group'],
                'is_favorite': True,
                'is_learned': item['is_learned']
            })
        return favorites
        
    except Exception as e:
        st.error(f"❌ 즐겨찾기 조회 실패: {e}")
        return []

def add_to_favorites(supabase: Client, word_data: Dict):
    """즐겨찾기에 추가"""
    try:
        supabase.table('favorites').insert({
            'word': word_data['word'],
            'translation': word_data['translation'],
            'image_url': word_data['image_url'],
            'age_group': word_data['age_group']
        }).execute()
    except Exception as e:
        st.error(f"❌ 즐겨찾기 추가 실패: {e}")

def remove_from_favorites(supabase: Client, word: str, age_group: int):
    """즐겨찾기에서 제거"""
    try:
        supabase.table('favorites')\
            .delete()\
            .eq('word', word)\
            .eq('age_group', age_group)\
            .execute()
    except Exception as e:
        st.error(f"❌ 즐겨찾기 제거 실패: {e}")

def toggle_learned(supabase: Client, word: str, age_group: int):
    """학습완료 토글"""
    try:
        # 현재 상태 확인
        result = supabase.table('favorites')\
            .select('is_learned')\
            .eq('word', word)\
            .eq('age_group', age_group)\
            .execute()
        
        if result.data:
            current_state = result.data[0]['is_learned']
            supabase.table('favorites')\
                .update({'is_learned': not current_state})\
                .eq('word', word)\
                .eq('age_group', age_group)\
                .execute()
    except Exception as e:
        st.error(f"❌ 학습완료 토글 실패: {e}")

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

def display_word_card(card: Dict, container, supabase: Client):
    """단어 카드 표시"""
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # 이미지 표시
            try:
                # 직접 URL로 이미지 표시 (더 안정적)
                st.image(card['image_url'], use_container_width=True, caption=f"{card['word']} ({card['translation']})")
            except Exception as e:
                st.error(f"이미지 로드 실패: {e}")
                # 기본 이미지 표시
                st.markdown(f"""
                <div style='background-color: #f0f2f6; border: 2px dashed #ccc; 
                           height: 200px; display: flex; align-items: center; 
                           justify-content: center; border-radius: 10px;'>
                    <div style='text-align: center;'>
                        <div style='font-size: 48px;'>🖼️</div>
                        <div style='color: #666;'>{card['word']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # 단어 표시
            st.markdown(f"<h1 style='text-align: center; color: #4A90E2; font-size: 48px;'>{card['word']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #666; font-style: italic;'>{card['translation']}</h3>", unsafe_allow_html=True)
            
            # 버튼들
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("🔊 음성듣기", key=f"audio_{card['id']}"):
                    audio_base64 = generate_audio(card['word'])
                    if audio_base64:
                        audio_html = f"""
                        <audio autoplay>
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                        """
                        st.markdown(audio_html, unsafe_allow_html=True)
            
            with col_btn2:
                is_favorite = card.get('is_favorite', False)
                fav_emoji = "⭐" if is_favorite else "☆"
                if st.button(f"{fav_emoji} 즐겨찾기", key=f"fav_{card['id']}"):
                    if is_favorite:
                        remove_from_favorites(supabase, card['word'], card['age_group'])
                    else:
                        add_to_favorites(supabase, card)
                    st.rerun()
            
            with col_btn3:
                if card.get('is_favorite', False):  # 즐겨찾기된 항목만 학습완료 가능
                    learned_emoji = "✅" if card.get('is_learned') else "□"
                    if st.button(f"{learned_emoji} 외웠어요", key=f"learned_{card['id']}"):
                        toggle_learned(supabase, card['word'], card['age_group'])
                        st.rerun()

# 메인 앱
def main():
    # 클라이언트 초기화
    supabase = init_supabase()
    openai_client = init_openai()
    
    # 테이블 생성 확인
    create_tables(supabase)
    
    # 사이드바
    with st.sidebar:
        st.title("📚 설정")
        
        # 연결 상태 표시
        st.success("🟢 Supabase 연결됨")
        if openai_client:
            st.success("🤖 OpenAI 연결됨")
        else:
            st.info("📝 기본 단어 사용")
        
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
        
        # 새 단어 생성
        if not show_favorites_only:
            if st.button("🔄 새 단어 생성"):
                if 'current_cards' in st.session_state:
                    del st.session_state.current_cards
                st.rerun()
    
    # 메인 컨텐츠
    st.title(f"🎯 {selected_age}세 단어 카드")
    
    # 카드 데이터 생성/가져오기
    if show_favorites_only:
        # 즐겨찾기 모드: DB에서 가져오기
        cards = get_favorites(supabase, selected_age)
        if not cards:
            st.warning("즐겨찾기한 단어가 없습니다! 일반 모드에서 단어를 즐겨찾기에 추가해보세요.")
            return
    else:
        # 일반 모드: 새로운 단어 생성
        if 'current_cards' not in st.session_state or len(st.session_state.current_cards) == 0:
            with st.spinner("새로운 단어들을 생성하고 있습니다..."):
                cards = []
                for _ in range(5):  # 5개 단어 미리 생성
                    card = generate_word_card(openai_client, selected_age)
                    if card:
                        cards.append(card)
                st.session_state.current_cards = cards
        else:
            cards = st.session_state.current_cards
    
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
        # 마지막 카드에 도달하면 새 카드 생성 (일반 모드만)
        if st.session_state.current_index >= len(cards) - 1 and not show_favorites_only:
            new_card = generate_word_card(openai_client, selected_age)
            if new_card:
                st.session_state.current_cards.append(new_card)
        
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
            # 마지막 카드에서 다음 버튼 누르면 새 카드 생성 (일반 모드만)
            if st.session_state.current_index >= len(cards) - 1 and not show_favorites_only:
                new_card = generate_word_card(openai_client, selected_age)
                if new_card:
                    st.session_state.current_cards.append(new_card)
                    cards = st.session_state.current_cards
            
            st.session_state.current_index = (st.session_state.current_index + 1) % len(cards)
            st.rerun()
    
    # 현재 카드 표시
    current_card = cards[st.session_state.current_index]
    card_container = st.container()
    display_word_card(current_card, card_container, supabase)
    
    # 진행 상황 표시
    if show_favorites_only:
        st.subheader("📊 즐겨찾기 학습 현황")
        learned_count = sum(1 for card in cards if card.get('is_learned'))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("즐겨찾기 단어", len(cards))
        with col2:
            st.metric("✅ 외운 단어", learned_count)
        with col3:
            if len(cards) > 0:
                progress = learned_count / len(cards)
                st.metric("학습률", f"{progress:.1%}")
        
        # 진행률 바
        if len(cards) > 0:
            progress = learned_count / len(cards)
            st.progress(progress)
    else:
        st.info("💡 마음에 드는 단어는 ⭐ 즐겨찾기에 추가해보세요!")

if __name__ == "__main__":
    main() 