import { useState, useMemo } from 'react';
import { AgeSelector } from './components/AgeSelector';
import { SlideSettings } from './components/SlideSettings';
import { WordCardSlideshow } from './components/WordCardSlideshow';
import { wordCardData } from './data/wordData';
import { UserProgress } from './types/WordCard';

export default function App() {
  const [selectedAge, setSelectedAge] = useState(3);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(2);
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
  const [userProgress, setUserProgress] = useState<UserProgress[]>([]);

  // 연령별 카드 필터링
  const filteredCards = useMemo(() => {
    let cards = wordCardData.filter(card => card.ageGroup === selectedAge);
    
    if (showFavoritesOnly) {
      const favoriteCardIds = userProgress
        .filter(p => p.isFavorite)
        .map(p => p.cardId);
      cards = cards.filter(card => favoriteCardIds.includes(card.id));
    }
    
    return cards;
  }, [selectedAge, showFavoritesOnly, userProgress]);

  // 즐겨찾기 토글
  const handleToggleFavorite = (cardId: string) => {
    setUserProgress(prev => {
      const existing = prev.find(p => p.cardId === cardId);
      if (existing) {
        return prev.map(p => 
          p.cardId === cardId 
            ? { ...p, isFavorite: !p.isFavorite }
            : p
        );
      } else {
        return [...prev, { cardId, isFavorite: true, isLearned: false }];
      }
    });
  };

  // 학습완료 토글
  const handleToggleLearned = (cardId: string) => {
    setUserProgress(prev => {
      const existing = prev.find(p => p.cardId === cardId);
      if (existing) {
        return prev.map(p => 
          p.cardId === cardId 
            ? { ...p, isLearned: !p.isLearned }
            : p
        );
      } else {
        return [...prev, { cardId, isFavorite: false, isLearned: true }];
      }
    });
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* 헤더 */}
        <div className="text-center">
          <h1 className="text-3xl mb-2">단어 카드 학습</h1>
          <p className="text-muted-foreground">
            연령에 맞는 단어를 배워보세요!
          </p>
        </div>

        {/* 연령 선택 */}
        <AgeSelector
          selectedAge={selectedAge}
          onAgeSelect={(age) => {
            setSelectedAge(age);
            setIsPlaying(false); // 연령 변경시 재생 정지
          }}
        />

        {/* 슬라이드 설정 */}
        <SlideSettings
          isPlaying={isPlaying}
          speed={speed}
          showFavoritesOnly={showFavoritesOnly}
          onTogglePlay={() => setIsPlaying(!isPlaying)}
          onSpeedChange={setSpeed}
          onToggleFavoritesOnly={setShowFavoritesOnly}
        />

        {/* 슬라이드쇼 */}
        <WordCardSlideshow
          cards={filteredCards}
          isPlaying={isPlaying}
          speed={speed}
          progress={userProgress}
          onToggleFavorite={handleToggleFavorite}
          onToggleLearned={handleToggleLearned}
        />

        {/* 통계 정보 */}
        <div className="text-center text-sm text-muted-foreground border-t pt-4">
          <div className="flex justify-center gap-6">
            <span>
              전체 카드: {wordCardData.filter(card => card.ageGroup === selectedAge).length}개
            </span>
            <span>
              즐겨찾기: {userProgress.filter(p => p.isFavorite).length}개
            </span>
            <span>
              학습완료: {userProgress.filter(p => p.isLearned).length}개
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}