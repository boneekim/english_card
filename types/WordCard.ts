export interface WordCard {
  id: string;
  word: string;
  translation: string;
  imageUrl: string;
  audioText: string;
  ageGroup: number;
}

export interface UserProgress {
  cardId: string;
  isFavorite: boolean;
  isLearned: boolean;
}