import { WordCard as WordCardType, UserProgress } from '../types/WordCard';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Heart, Check, Volume2 } from 'lucide-react';

interface WordCardProps {
  card: WordCardType;
  progress: UserProgress | undefined;
  onToggleFavorite: (cardId: string) => void;
  onToggleLearned: (cardId: string) => void;
}

export function WordCard({ card, progress, onToggleFavorite, onToggleLearned }: WordCardProps) {
  const playAudio = () => {
    // Web Speech API를 사용한 음성 재생
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(card.audioText);
      utterance.lang = 'ko-KR';
      utterance.rate = 0.8;
      speechSynthesis.speak(utterance);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto h-[500px] relative">
      <CardContent className="p-6 h-full flex flex-col items-center justify-center">
        {/* 즐겨찾기 및 학습완료 버튼 */}
        <div className="absolute top-4 right-4 flex gap-2">
          <Button
            size="sm"
            variant={progress?.isFavorite ? "default" : "outline"}
            onClick={() => onToggleFavorite(card.id)}
          >
            <Heart className={`h-4 w-4 ${progress?.isFavorite ? 'fill-current' : ''}`} />
          </Button>
          <Button
            size="sm"
            variant={progress?.isLearned ? "default" : "outline"}
            onClick={() => onToggleLearned(card.id)}
          >
            <Check className={`h-4 w-4 ${progress?.isLearned ? 'fill-current' : ''}`} />
          </Button>
        </div>

        {/* 이미지 */}
        <div className="mb-6">
          <ImageWithFallback
            src={card.imageUrl}
            alt={card.word}
            className="w-64 h-64 object-cover rounded-lg shadow-lg"
          />
        </div>

        {/* 단어 정보 */}
        <div className="text-center mb-4">
          <h2 className="text-3xl mb-2">{card.word}</h2>
          <p className="text-xl text-muted-foreground">{card.translation}</p>
        </div>

        {/* 음성 재생 버튼 */}
        <Button
          size="lg"
          onClick={playAudio}
          className="flex items-center gap-2"
        >
          <Volume2 className="h-5 w-5" />
          음성 듣기
        </Button>
      </CardContent>
    </Card>
  );
}