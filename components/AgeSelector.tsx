import { Button } from './ui/button';

interface AgeSelectorProps {
  selectedAge: number;
  onAgeSelect: (age: number) => void;
}

export function AgeSelector({ selectedAge, onAgeSelect }: AgeSelectorProps) {
  const ages = [3, 4, 5, 6, 7];

  return (
    <div className="flex flex-wrap gap-2 justify-center">
      <span className="text-sm mr-2 self-center">연령 선택:</span>
      {ages.map((age) => (
        <Button
          key={age}
          variant={selectedAge === age ? "default" : "outline"}
          size="sm"
          onClick={() => onAgeSelect(age)}
        >
          {age}세
        </Button>
      ))}
    </div>
  );
}