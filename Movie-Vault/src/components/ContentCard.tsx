import { Pencil, Trash2, Film, Tv, Gamepad2, Youtube, Zap } from 'lucide-react';
import { StarRating } from './StarRating';
import { StatusBadge } from './StatusBadge';
import { useNavigate } from 'react-router-dom';

const typeIcons: Record<string, typeof Film> = {
  movie: Film,
  series: Tv,
  game: Gamepad2,
  youtube: Youtube,
  productivity: Zap,
};

interface ContentCardProps {
  item: {
    id: string;
    title: string;
    type: string;
    genre: string | null;
    rating: number | null;
    image_url: string | null;
    status: string;
    year: number;
    user_id: string;
  };
  isOwner?: boolean;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export function ContentCard({ item, isOwner, onEdit, onDelete }: ContentCardProps) {
  const navigate = useNavigate();
  const Icon = typeIcons[item.type] || Film;

  return (
    <div
      className="group card-glow rounded-xl bg-card overflow-hidden cursor-pointer shadow-sm border border-border/50"
      onClick={() => navigate(`/content/${item.id}`)}
    >
      <div className="relative aspect-[2/3] overflow-hidden bg-muted">
        {item.image_url ? (
          <img
            src={item.image_url}
            alt={item.title}
            className="w-full h-full object-cover image-zoom"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Icon size={48} className="text-muted-foreground/30" />
          </div>
        )}
        <div className="absolute top-2 left-2">
          <StatusBadge status={item.status} />
        </div>
        <div className="absolute top-2 right-2 bg-card/80 backdrop-blur-sm rounded-full p-1.5">
          <Icon size={14} className="text-foreground/70" />
        </div>
        {isOwner && (
          <div className="absolute bottom-2 right-2 flex gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={(e) => { e.stopPropagation(); onEdit?.(item.id); }}
              className="bg-card/90 backdrop-blur-sm p-1.5 rounded-lg hover:bg-primary hover:text-primary-foreground transition-colors"
            >
              <Pencil size={14} />
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); onDelete?.(item.id); }}
              className="bg-card/90 backdrop-blur-sm p-1.5 rounded-lg hover:bg-destructive hover:text-destructive-foreground transition-colors"
            >
              <Trash2 size={14} />
            </button>
          </div>
        )}
      </div>
      <div className="p-3">
        <h3 className="font-semibold text-sm text-foreground truncate">{item.title}</h3>
        <div className="flex items-center justify-between mt-1">
          <span className="text-xs text-muted-foreground">{item.year}{item.genre ? ` · ${item.genre}` : ''}</span>
        </div>
        <div className="mt-1.5">
          <StarRating rating={item.rating ?? 0} size={12} />
        </div>
      </div>
    </div>
  );
}
