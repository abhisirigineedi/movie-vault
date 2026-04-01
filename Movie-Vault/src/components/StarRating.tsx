import { Star } from 'lucide-react';

interface StarRatingProps {
  rating: number;
  showValue?: boolean;
  size?: number;
}

export function StarRating({ rating, showValue = true, size = 16 }: StarRatingProps) {
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    const fill = Math.min(1, Math.max(0, rating - (i - 1)));
    stars.push(
      <div key={i} className="relative" style={{ width: size, height: size }}>
        <Star size={size} className="text-star-empty" fill="hsl(var(--star-empty))" strokeWidth={0} />
        <div className="absolute inset-0 overflow-hidden" style={{ width: `${fill * 100}%` }}>
          <Star size={size} className="text-star-filled" fill="hsl(var(--star-filled))" strokeWidth={0} />
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-0.5">
      {stars}
      {showValue && (
        <span className="ml-1.5 text-sm font-medium text-muted-foreground">
          {rating.toFixed(1)}
        </span>
      )}
    </div>
  );
}
