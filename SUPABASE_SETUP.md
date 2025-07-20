# 🗄️ Supabase 데이터베이스 설정 가이드

이 프로젝트는 [Supabase](https://supabase.com/)를 데이터베이스로 사용합니다. 다음 단계를 따라 설정해주세요.

## 📋 1단계: Supabase 프로젝트 생성

1. **[Supabase 웹사이트](https://supabase.com/)** 접속
2. **"Start your project"** 또는 **"Sign Up"** 클릭
3. GitHub 계정으로 로그인 (boneekim)
4. **"New Project"** 클릭
5. 프로젝트 정보 입력:
   - **Name**: `english-card` 또는 원하는 이름
   - **Database Password**: 강력한 비밀번호 생성 (저장해두세요!)
   - **Region**: `Northeast Asia (Seoul)` 선택 (한국 서버)
6. **"Create new project"** 클릭
7. 프로젝트 생성 완료까지 약 2-3분 대기

## 🔧 2단계: API 키 및 URL 확인

프로젝트가 생성되면:

1. **왼쪽 사이드바** → **Settings** → **API** 클릭
2. 다음 정보 복사:
   - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
   - **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## ⚙️ 3단계: 로컬 설정 파일 생성

1. `supabase_config.py.example` 파일을 `supabase_config.py`로 복사:
   ```bash
   cp supabase_config.py.example supabase_config.py
   ```

2. `supabase_config.py` 파일을 열어서 실제 값으로 수정:
   ```python
   # Supabase 설정
   SUPABASE_URL = "https://your-project-ref.supabase.co"  # 실제 Project URL로 변경
   SUPABASE_ANON_KEY = "your-anon-key-here"  # 실제 anon public key로 변경
   ```

## 🗃️ 4단계: 데이터베이스 테이블 생성

1. Supabase Dashboard에서 **SQL Editor** 클릭
2. **"New query"** 클릭  
3. 다음 SQL 코드를 복사해서 붙여넣기:

```sql
-- 단어 카드 테이블
CREATE TABLE word_cards (
    id TEXT PRIMARY KEY,
    word TEXT NOT NULL,
    translation TEXT,
    image_url TEXT,
    audio_text TEXT,
    age_group INTEGER NOT NULL
);

-- 사용자 진행상황 테이블
CREATE TABLE user_progress (
    card_id TEXT PRIMARY KEY,
    is_favorite BOOLEAN DEFAULT FALSE,
    is_learned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS 정책 설정 (선택사항)
ALTER TABLE word_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기 가능
CREATE POLICY "Public read access" ON word_cards FOR SELECT USING (true);
CREATE POLICY "Public read access" ON user_progress FOR SELECT USING (true);

-- 모든 사용자가 쓰기 가능 (실제 운영환경에서는 수정 필요)
CREATE POLICY "Public write access" ON word_cards FOR ALL USING (true);
CREATE POLICY "Public write access" ON user_progress FOR ALL USING (true);
```

4. **"Run"** 버튼 클릭하여 실행

## 🚀 5단계: 앱 실행

1. 필요한 패키지 설치:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. Supabase 버전 앱 실행:
   ```bash
   streamlit run streamlit_app_supabase.py
   ```

3. 브라우저에서 `http://localhost:8501` 접속

## ✅ 연결 확인

앱이 정상적으로 실행되면:
- 사이드바에 "🟢 Supabase 연결됨" 표시
- 초기 단어 데이터가 자동으로 로드됨
- 즐겨찾기/학습완료 상태가 데이터베이스에 저장됨

## 🔒 보안 참고사항

- `supabase_config.py` 파일은 `.gitignore`에 포함되어 있어 GitHub에 업로드되지 않습니다
- 실제 운영환경에서는 RLS(Row Level Security) 정책을 더 엄격하게 설정하세요
- anon key는 클라이언트에서 사용해도 안전하도록 설계되었습니다

## 🆘 문제 해결

### "supabase_config.py 파일이 필요합니다" 오류
- `supabase_config.py.example`을 복사해서 `supabase_config.py` 파일을 만들어주세요

### "Supabase 연결 실패" 오류  
- URL과 API Key가 정확한지 확인하세요
- 인터넷 연결 상태를 확인하세요

### "테이블이 존재하지 않습니다" 오류
- 4단계의 SQL 코드를 Supabase SQL Editor에서 실행해주세요

## 📞 도움이 필요하시면

문제가 지속되면 GitHub Issues에 문의해주세요! 