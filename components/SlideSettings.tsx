import { Button } from './ui/button';
import { Slider } from './ui/slider';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { Play, Pause, Heart } from 'lucide-react';

interface SlideSettingsProps {
  isPlaying: boolean;
  speed: number;
  showFavoritesOnly: boolean;
  onTogglePlay: () => void;
  onSpeedChange: (speed: number) => void;
  onToggleFavoritesOnly: () => void;
}

export function SlideSettings({
  isPlaying,
  speed,
  showFavoritesOnly,
  onTogglePlay,
  onSpeedChange,
  onToggleFavoritesOnly
}: SlideSettingsProps) {
  return (
    <div className="flex flex-wrap items-center gap-4 p-4 bg-muted rounded-lg">
      {/* 재생/정지 버튼 */}
      <Button
        variant={isPlaying ? "default" : "outline"}
        onClick={onTogglePlay}
        className="flex items-center gap-2"
      >
        {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
        {isPlaying ? '정지' : '재생'}
      </Button>

      {/* 속도 조절 */}
      <div className="flex items-center gap-2 min-w-[200px]">
        <Label htmlFor="speed-slider" className="text-sm whitespace-nowrap">
          속도: {speed}초
        </Label>
        <Slider
          id="speed-slider"
          value={[speed]}
          onValueChange={([value]) => onSpeedChange(value)}
          min={1}
          max={10}
          step={0.5}
          className="flex-1"
        />
      </div>

      {/* 즐겨찾기만 보기 */}
      <div className="flex items-center gap-2">
        <Switch
          id="favorites-only"
          checked={showFavoritesOnly}
          onCheckedChange={onToggleFavoritesOnly}
        />
        <Label htmlFor="favorites-only" className="flex items-center gap-1 text-sm">
          <Heart className="h-4 w-4" />
          즐겨찾기만
        </Label>
      </div>
    </div>
  );
}