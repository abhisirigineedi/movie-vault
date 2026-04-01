import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { supabase } from '@/integrations/supabase/client';
import { Navbar } from '@/components/Navbar';
import { StarRating } from '@/components/StarRating';
import { StatusBadge } from '@/components/StatusBadge';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Film, Tv, Gamepad2, Youtube, Zap, Calendar, Layers } from 'lucide-react';

const typeIcons: Record<string, typeof Film> = { movie: Film, series: Tv, game: Gamepad2, youtube: Youtube, productivity: Zap };
const typeLabels: Record<string, string> = { movie: 'Movie', series: 'Web Series', game: 'Game', youtube: 'YouTube', productivity: 'Productivity' };

export default function ContentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    supabase.from('content').select('*').eq('id', id).single().then(({ data }) => {
      setItem(data);
      setLoading(false);
    });
  }, [id]);

  if (loading) return <div className="min-h-screen bg-background"><Navbar /><div className="flex items-center justify-center py-20 text-muted-foreground">Loading...</div></div>;
  if (!item) return <div className="min-h-screen bg-background"><Navbar /><div className="flex items-center justify-center py-20 text-muted-foreground">Not found</div></div>;

  const Icon = typeIcons[item.type] || Film;

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="container max-w-4xl px-4 py-6">
        <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">
          <ArrowLeft size={16} className="mr-1.5" />Back
        </Button>
        <div className="grid md:grid-cols-[300px_1fr] gap-8">
          <div className="rounded-xl overflow-hidden bg-muted aspect-[2/3]">
            {item.image_url ? (
              <img src={item.image_url} alt={item.title} className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <Icon size={64} className="text-muted-foreground/30" />
              </div>
            )}
          </div>
          <div>
            <div className="flex items-center gap-2 mb-2">
              <StatusBadge status={item.status} />
              <span className="flex items-center gap-1 text-xs text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
                <Icon size={12} />{typeLabels[item.type]}
              </span>
            </div>
            <h1 className="text-3xl font-bold text-foreground mb-2">{item.title}</h1>
            <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
              <span className="flex items-center gap-1"><Calendar size={14} />{item.year}</span>
              {item.genre && <span>{item.genre}</span>}
              {item.seasons && <span className="flex items-center gap-1"><Layers size={14} />{item.seasons} season{item.seasons > 1 ? 's' : ''}</span>}
            </div>
            <div className="mb-6">
              <StarRating rating={Number(item.rating) || 0} size={20} />
            </div>
            {item.review && (
              <div>
                <h2 className="font-semibold text-foreground mb-2">Review</h2>
                <p className="text-muted-foreground leading-relaxed whitespace-pre-wrap">{item.review}</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
