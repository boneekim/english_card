import { useState, useEffect } from 'react';
import { WordCard } from './WordCard';
import { Button } from './ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { WordCard as WordCardType, UserProgress } from '../types/WordCard';

interface WordCardSlideshowProps {
  cards: WordCardType[];
  isPlaying: boolean;
  speed: number;
  progress: UserProgress[];
  onToggleFavorite: (cardId: string) => void;
  onToggleLearned: (cardId: string) => void;
}

export function WordCardSlideshow({
  cards,
  isPlaying,
  speed,
  progress,
  onToggleFavorite,
  onToggleLearned
}: WordCardSlideshowProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  // 자동 슬라이드
  useEffect(() => {
    if (!isPlaying || cards.length === 0) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % cards.length);
    }, speed * 1000);

    return () => clearInterval(interval);
  }, [isPlaying, speed, cards.length]);

  // 수동 슬라이드 조작
  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev - 1 + cards.length) % cards.length);
  };

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % cards.length);
  };

  // 키보드 조작
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === 'ArrowLeft') {
        goToPrevious();
      } else if (event.key === 'ArrowRight') {
        goToNext();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  if (cards.length === 0) {
    return (
      <div className="text-center text-muted-foreground p-8">
        표시할 카드가 없습니다.
      </div>
    );
  }

  const currentCard = cards[currentIndex];
  const currentProgress = progress.find(p => p.cardId === currentCard.id);

  return (
    <div className="relative">
      {/* 카드 표시 */}
      <div className="mb-6">
        <WordCard
          card={currentCard}
          progress={currentProgress}
          onToggleFavorite={onToggleFavorite}
          onToggleLearned={onToggleLearned}
        />
      </div>

      {/* 네비게이션 */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          size="lg"
          onClick={goToPrevious}
          className="flex items-center gap-2"
        >
          <ChevronLeft className="h-5 w-5" />
          이전
        </Button>

        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            {currentIndex + 1} / {cards.length}
          </p>
          <div className="flex gap-1 mt-2">
            {cards.map((_, index) => (
              <button
                key={index}
                className={`w-2 h-2 rounded-full ${
                  index === currentIndex ? 'bg-primary' : 'bg-muted'
                }`}
                onClick={() => setCurrentIndex(index)}
              />
            ))}
          </div>
        </div>

        <Button
          variant="outline"
          size="lg"
          onClick={goToNext}
          className="flex items-center gap-2"
        >
          다음
          <ChevronRight className="h-5 w-5" />
        </Button>
      </div>
    </div>
  );
}