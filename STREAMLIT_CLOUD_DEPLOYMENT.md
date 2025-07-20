# ☁️ Streamlit Cloud 배포 가이드

이 가이드를 따라하면 **아이 연령별 단어 카드** 앱을 Streamlit Cloud에 무료로 배포할 수 있습니다!

## 🚀 1단계: Supabase 설정 (필수)

먼저 [SUPABASE_SETUP.md](SUPABASE_SETUP.md)를 따라 Supabase 프로젝트를 생성하고 설정하세요.

중요한 정보를 미리 복사해두세요:
- **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
- **anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## 🌐 2단계: Streamlit Cloud 배포

### 1. Streamlit Cloud 가입

1. **[Streamlit Cloud](https://share.streamlit.io/)** 접속
2. **"Sign up"** 클릭
3. **GitHub 계정(boneekim)**으로 로그인

### 2. 새 앱 배포

1. **"New app"** 클릭
2. 설정 입력:
   - **Repository**: `boneekim/english_card`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: 원하는 URL (예: `english-card-boneekim`)

### 3. Secrets 설정 (중요!)

배포 전에 **"Advanced settings"** 클릭 후 **"Secrets"** 탭에서:

```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key-here"
```

**실제 Supabase URL과 Key를 입력하세요!**

### 4. 배포 완료

1. **"Deploy!"** 클릭
2. 2-3분 대기하면 앱이 배포됩니다
3. 생성된 URL로 접속하여 확인

## ✅ 배포 후 확인사항

배포가 성공하면:
- ✅ 사이드바에 "🟢 Supabase 연결됨" 표시
- ✅ 연령별 단어 카드 정상 동작
- ✅ 즐겨찾기/학습완료 기능 정상 동작
- ✅ 음성 재생 기능 정상 동작

## 🔧 앱 관리

### URL 확인
배포된 앱 URL: `https://your-app-name.streamlit.app`

### Secrets 수정
1. **Streamlit Cloud Dashboard** → **앱 선택**
2. **⚙️ Settings** → **Secrets**에서 언제든 수정 가능

### 앱 업데이트
- GitHub에 새 코드를 푸시하면 자동으로 앱이 업데이트됩니다!

## 🆘 문제 해결

### "Supabase 연결 실패" 오류
- Secrets에 올바른 SUPABASE_URL과 SUPABASE_ANON_KEY가 설정되었는지 확인
- URL 끝에 슬래시(/)가 없는지 확인

### "테이블이 존재하지 않습니다" 오류
- [SUPABASE_SETUP.md](SUPABASE_SETUP.md)의 4단계 SQL 실행 확인

### 앱이 로딩되지 않는 경우
- Streamlit Cloud 대시보드에서 로그 확인
- requirements.txt에 모든 패키지가 포함되었는지 확인

## 🎯 완성!

이제 전 세계 어디서나 접속할 수 있는 **아이 연령별 단어 카드** 앱이 완성되었습니다!

📱 **모바일에서도 완벽하게 동작합니다!**

---

### 📞 도움이 필요하시면
- GitHub Issues에 문의
- Streamlit Community Forum 활용 