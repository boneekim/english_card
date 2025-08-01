class EnglishCardApp {
    constructor() {
        this.cards = [];
        this.currentCardIndex = 0;
        this.autoSlideInterval = null;
        this.isAutoSlideActive = false;
        this.slideTime = 3;
        this.memorizedCards = new Set();
        this.difficultCards = new Set();
        this.currentFilter = 'all';
        this.filteredCards = [];
        
        this.initializeElements();
        this.bindEvents();
    }
    
    initializeElements() {
        // 설정 요소들
        this.ageSelect = document.getElementById('age-select');
        this.categorySelect = document.getElementById('category-select');
        this.slideTimeInput = document.getElementById('slide-time');
        this.cardCountInput = document.getElementById('card-count');
        this.startBtn = document.getElementById('start-btn');
        this.autoSlideToggle = document.getElementById('auto-slide-toggle');
        
        // 필터 버튼들
        this.showAllBtn = document.getElementById('show-all');
        this.showMemorizedBtn = document.getElementById('show-memorized');
        this.showDifficultBtn = document.getElementById('show-difficult');
        
        // 진행 상황 요소들
        this.currentCardSpan = document.getElementById('current-card');
        this.totalCardsSpan = document.getElementById('total-cards');
        this.progressFill = document.getElementById('progress-fill');
        this.memorizedCount = document.getElementById('memorized-count');
        this.difficultCount = document.getElementById('difficult-count');
        
        // 카드 표시 요소들
        this.cardDisplay = document.getElementById('card-display');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.loading = document.getElementById('loading');
    }
    
    bindEvents() {
        // 시작 버튼
        this.startBtn.addEventListener('click', () => this.startCards());
        
        // 자동슬라이드 토글
        this.autoSlideToggle.addEventListener('click', () => this.toggleAutoSlide());
        
        // 슬라이드 시간 변경
        this.slideTimeInput.addEventListener('change', (e) => {
            this.slideTime = parseInt(e.target.value);
            if (this.isAutoSlideActive) {
                this.stopAutoSlide();
                this.startAutoSlide();
            }
        });
        
        // 필터 버튼들
        this.showAllBtn.addEventListener('click', () => this.setFilter('all'));
        this.showMemorizedBtn.addEventListener('click', () => this.setFilter('memorized'));
        this.showDifficultBtn.addEventListener('click', () => this.setFilter('difficult'));
        
        // 네비게이션 버튼들
        this.prevBtn.addEventListener('click', () => this.previousCard());
        this.nextBtn.addEventListener('click', () => this.nextCard());
        
        // 키보드 네비게이션
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.previousCard();
            if (e.key === 'ArrowRight') this.nextCard();
            if (e.key === ' ') {
                e.preventDefault();
                this.toggleAutoSlide();
            }
        });
    }
    
    async startCards() {
        const category = this.categorySelect.value;
        const ageGroup = this.ageSelect.value;
        const cardCount = parseInt(this.cardCountInput.value);
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/get_cards', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category,
                    age_group: ageGroup,
                    card_count: cardCount
                })
            });
            
            const data = await response.json();
            this.cards = data.cards;
            this.currentCardIndex = 0;
            this.memorizedCards.clear();
            this.difficultCards.clear();
            this.currentFilter = 'all';
            this.updateFilteredCards();
            this.displayCard();
            this.updateProgress();
            this.updateCounts();
            this.enableNavigation();
            
            // 활성 필터 버튼 업데이트
            this.setActiveFilterButton(this.showAllBtn);
            
        } catch (error) {
            console.error('카드 로딩 중 오류:', error);
            this.cardDisplay.innerHTML = '<div class="card-loading">카드를 불러오는 중 오류가 발생했습니다.</div>';
        } finally {
            this.showLoading(false);
        }
    }
    
    updateFilteredCards() {
        switch (this.currentFilter) {
            case 'memorized':
                this.filteredCards = this.cards.filter((_, index) => this.memorizedCards.has(index));
                break;
            case 'difficult':
                this.filteredCards = this.cards.filter((_, index) => this.difficultCards.has(index));
                break;
            default:
                this.filteredCards = [...this.cards];
        }
        
        // 현재 카드 인덱스 조정
        if (this.currentCardIndex >= this.filteredCards.length) {
            this.currentCardIndex = Math.max(0, this.filteredCards.length - 1);
        }
    }
    
    displayCard() {
        if (this.filteredCards.length === 0) {
            this.cardDisplay.innerHTML = '<div class="card-loading">표시할 카드가 없습니다.</div>';
            this.disableNavigation();
            return;
        }
        
        const card = this.filteredCards[this.currentCardIndex];
        const originalIndex = this.cards.indexOf(card);
        
        const isMemorized = this.memorizedCards.has(originalIndex);
        const isDifficult = this.difficultCards.has(originalIndex);
        
        this.cardDisplay.innerHTML = `
            <div class="card">
                <img src="${card.image_url}" alt="${card.english}" class="card-image" loading="lazy">
                <div class="card-text">
                    <span class="korean">${card.korean}</span>
                    <span class="english">${card.english}</span>
                </div>
                <div class="card-actions">
                    <button class="action-btn speak-btn" onclick="app.speakWord('${card.english}')" title="음성 듣기">
                        <i class="fas fa-volume-up"></i>
                    </button>
                    <button class="action-btn memorized-btn ${isMemorized ? 'active' : ''}" 
                            onclick="app.toggleMemorized(${originalIndex})" title="외웠어요">
                        <i class="fas fa-check"></i>
                    </button>
                    <button class="action-btn difficult-btn ${isDifficult ? 'active' : ''}" 
                            onclick="app.toggleDifficult(${originalIndex})" title="어려워요">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;
        
        this.updateProgress();
    }
    
    speakWord(word) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = 'en-US';
            utterance.rate = 0.8;
            utterance.pitch = 1.1;
            speechSynthesis.speak(utterance);
        } else {
            alert('이 브라우저는 음성 합성을 지원하지 않습니다.');
        }
    }
    
    toggleMemorized(cardIndex) {
        if (this.memorizedCards.has(cardIndex)) {
            this.memorizedCards.delete(cardIndex);
        } else {
            this.memorizedCards.add(cardIndex);
            // 외운 카드는 어려운 카드에서 제거
            this.difficultCards.delete(cardIndex);
        }
        
        this.updateCounts();
        this.updateFilteredCards();
        this.displayCard();
    }
    
    toggleDifficult(cardIndex) {
        if (this.difficultCards.has(cardIndex)) {
            this.difficultCards.delete(cardIndex);
        } else {
            this.difficultCards.add(cardIndex);
            // 어려운 카드는 외운 카드에서 제거
            this.memorizedCards.delete(cardIndex);
        }
        
        this.updateCounts();
        this.updateFilteredCards();
        this.displayCard();
    }
    
    setFilter(filter) {
        this.currentFilter = filter;
        this.currentCardIndex = 0;
        this.updateFilteredCards();
        this.displayCard();
        
        // 활성 필터 버튼 업데이트
        document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
        
        switch (filter) {
            case 'memorized':
                this.setActiveFilterButton(this.showMemorizedBtn);
                break;
            case 'difficult':
                this.setActiveFilterButton(this.showDifficultBtn);
                break;
            default:
                this.setActiveFilterButton(this.showAllBtn);
        }
    }
    
    setActiveFilterButton(button) {
        button.classList.add('active');
    }
    
    previousCard() {
        if (this.filteredCards.length === 0) return;
        
        this.currentCardIndex = this.currentCardIndex > 0 
            ? this.currentCardIndex - 1 
            : this.filteredCards.length - 1;
        this.displayCard();
    }
    
    nextCard() {
        if (this.filteredCards.length === 0) return;
        
        this.currentCardIndex = this.currentCardIndex < this.filteredCards.length - 1 
            ? this.currentCardIndex + 1 
            : 0;
        this.displayCard();
    }
    
    toggleAutoSlide() {
        if (this.isAutoSlideActive) {
            this.stopAutoSlide();
        } else {
            this.startAutoSlide();
        }
    }
    
    startAutoSlide() {
        if (this.filteredCards.length === 0) return;
        
        this.isAutoSlideActive = true;
        this.autoSlideToggle.textContent = '자동슬라이드 OFF';
        this.autoSlideToggle.style.background = '#f56565';
        
        this.autoSlideInterval = setInterval(() => {
            this.nextCard();
        }, this.slideTime * 1000);
    }
    
    stopAutoSlide() {
        this.isAutoSlideActive = false;
        this.autoSlideToggle.textContent = '자동슬라이드 ON';
        this.autoSlideToggle.style.background = '#48bb78';
        
        if (this.autoSlideInterval) {
            clearInterval(this.autoSlideInterval);
            this.autoSlideInterval = null;
        }
    }
    
    updateProgress() {
        if (this.filteredCards.length === 0) {
            this.currentCardSpan.textContent = '0';
            this.totalCardsSpan.textContent = '0';
            this.progressFill.style.width = '0%';
            return;
        }
        
        this.currentCardSpan.textContent = this.currentCardIndex + 1;
        this.totalCardsSpan.textContent = this.filteredCards.length;
        
        const progress = ((this.currentCardIndex + 1) / this.filteredCards.length) * 100;
        this.progressFill.style.width = progress + '%';
    }
    
    updateCounts() {
        this.memorizedCount.textContent = this.memorizedCards.size;
        this.difficultCount.textContent = this.difficultCards.size;
    }
    
    enableNavigation() {
        this.prevBtn.disabled = false;
        this.nextBtn.disabled = false;
    }
    
    disableNavigation() {
        this.prevBtn.disabled = true;
        this.nextBtn.disabled = true;
    }
    
    showLoading(show) {
        if (show) {
            this.loading.classList.remove('hidden');
        } else {
            this.loading.classList.add('hidden');
        }
    }
}

// 앱 초기화
const app = new EnglishCardApp();

// 페이지 로드 시 음성 합성 초기화 (일부 브라우저에서 필요)
window.addEventListener('load', () => {
    if ('speechSynthesis' in window) {
        // 빈 음성을 한 번 재생하여 음성 합성 엔진을 초기화
        const utterance = new SpeechSynthesisUtterance('');
        utterance.volume = 0;
        speechSynthesis.speak(utterance);
    }
});
