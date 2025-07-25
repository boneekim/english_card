# 🎯 아이 연령별 단어 카드 슬라이드 프로그램

유아부터 초등학생 전까지의 아이들을 위한 맞춤형 단어 학습 프로그램입니다.
연령에 적합한 단어와 이미지, 음성을 제공하여 효과적인 학습을 도와줍니다.

## ✨ 주요 기능

- 📅 **연령별 맞춤 콘텐츠**: 3세~7세 아이들을 위한 연령별 단어 제공
- 🖼️ **시각적 학습**: 단어와 연상되는 고품질 이미지 카드
- 🔊 **음성 지원**: 한국어 TTS(Text-to-Speech)로 정확한 발음 제공
- ⏰ **자동 슬라이드**: 1~10초 간격으로 자동 재생 (기본 2초)
- 🎮 **수동 제어**: 이전/다음 버튼으로 직접 슬라이드 조작
- ⭐ **즐겨찾기**: 자주 보고 싶은 카드 표시 및 필터링
- ✅ **학습 체크**: 외운 단어 표시로 학습 진도 관리
- 📊 **진행률 추적**: 학습 완료율과 통계 시각화
- 💾 **자동 저장**: SQLite 데이터베이스로 학습 진행상황 자동 저장

## 🚀 설치 및 실행

### 옵션 1: 로컬 실행 🖥️

1. **Supabase 설정**
   - 📋 **[SUPABASE_SETUP.md](SUPABASE_SETUP.md)** 가이드를 따라 설정
   - 무료로 클라우드 데이터베이스 사용 가능

2. **필요한 패키지 설치**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **앱 실행**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **브라우저에서 접속**
   - 기본 주소: `http://localhost:8501`

### 옵션 2: Streamlit Cloud 배포 ☁️ ⭐ 추천

1. **Streamlit Cloud 배포**
   - ☁️ **[STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)** 가이드를 따라 설정
   - **완전 무료로 온라인 배포!**
   - 전 세계 어디서나 접속 가능
   - 모바일에서도 완벽 동작

## 📱 사용법

### 기본 설정
1. **사이드바**에서 아이의 연령(3~7세) 선택
2. **슬라이드 설정**에서 자동 재생 여부와 속도 조절
3. **즐겨찾기만 보기** 체크박스로 필터링

### 학습하기
1. **🔊 음성듣기**: 단어 발음을 들을 수 있습니다
2. **⭐ 즐겨찾기**: 자주 보고 싶은 카드를 표시합니다
3. **✅ 외웠어요**: 아이가 외운 단어를 체크합니다
4. **⬅️ 이전 / ➡️ 다음**: 수동으로 카드를 넘길 수 있습니다

### 진행상황 관리
- 하단의 **학습 진행 상황**에서 통계 확인
- **진행상황 초기화** 버튼으로 모든 기록 리셋

## 📋 연령별 학습 내용

| 연령 | 학습 주제 | 예시 단어 |
|------|-----------|-----------|
| 3세 | 기본 사물 | 사과, 강아지, 고양이, 자동차, 공 |
| 4세 | 자연/환경 | 나비, 꽃, 집, 해, 달 |
| 5세 | 사회생활 | 가족, 학교, 친구, 책, 연필 |
| 6세 | 개념어 | 숫자, 색깔, 모양, 날씨, 계절 |
| 7세 | 추상어 | 생각, 마음, 꿈, 희망, 용기 |

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Database**: Supabase PostgreSQL
- **TTS**: Google Text-to-Speech (gTTS)
- **Images**: Unsplash API
- **Language**: Python 3.8+
- **Cloud**: Supabase (Backend-as-a-Service) + Streamlit Cloud (호스팅)

## 📁 프로젝트 구조

```
아이 연령별 단어 카드 슬라이드 프로그램/
├── streamlit_app.py                      # 메인 애플리케이션 ⭐
├── requirements.txt                      # 패키지 의존성
├── README.md                            # 프로젝트 설명서
├── SUPABASE_SETUP.md                    # Supabase 설정 가이드
├── STREAMLIT_CLOUD_DEPLOYMENT.md        # Streamlit Cloud 배포 가이드
├── supabase_config.py.example           # 로컬 실행용 설정 예시
├── .streamlit/
│   └── secrets.toml.example             # Streamlit Cloud용 설정 예시
└── components/                          # 기존 React 컴포넌트들 (참고용)
```

## 🎯 향후 개선 계획

- [ ] 더 많은 연령대 추가 (8~10세)
- [ ] 카테고리별 단어 분류 (동물, 음식, 색깔 등)
- [ ] 게임 요소 추가 (퀴즈, 매칭 게임)
- [ ] 다국어 지원 (영어, 중국어 등)
- [ ] 학습 리포트 생성
- [ ] 부모님용 대시보드

## 🤝 기여하기

1. Fork 프로젝트
2. 새 기능 브랜치 생성 (`git checkout -b feature/new-feature`)
3. 변경사항 커밋 (`git commit -am 'Add new feature'`)
4. 브랜치에 푸시 (`git push origin feature/new-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 문의사항이나 제안이 있으시면 이슈를 생성해 주세요.

---

**즐거운 학습 되세요! 📚✨** 