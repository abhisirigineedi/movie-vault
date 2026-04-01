import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '@/integrations/supabase/client';
import { useAuth } from '@/contexts/AuthContext';
import { Navbar } from '@/components/Navbar';
import { ContentCard } from '@/components/ContentCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Upload, BarChart3, Film, Tv, Gamepad2, Youtube, Zap } from 'lucide-react';
import { toast } from 'sonner';

const typeIcons: Record<string, typeof Film> = { movie: Film, series: Tv, game: Gamepad2, youtube: Youtube, productivity: Zap };

export default function Profile() {
  const { username } = useParams();
  const { user, profile: myProfile, refreshProfile } = useAuth();
  const [profileData, setProfileData] = useState<any>(null);
  const [content, setContent] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const isOwner = myProfile?.username === username;

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const { data: prof } = await supabase.from('profiles').select('*').eq('username', username).single();
      if (!prof) { setLoading(false); return; }
      setProfileData(prof);

      const { data: items } = await supabase
        .from('content')
        .select('*')
        .eq('user_id', prof.user_id)
        .order('created_at', { ascending: false });
      setContent(items || []);
      setLoading(false);
    };
    if (username) load();
  }, [username]);

  const handleAvatarUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !user) return;
    const ext = file.name.split('.').pop();
    const path = `avatars/${user.id}.${ext}`;
    await supabase.storage.from('movie-posters').upload(path, file, { upsert: true });
    const { data: { publicUrl } } = supabase.storage.from('movie-posters').getPublicUrl(path);
    await supabase.from('profiles').update({ avatar_url: publicUrl }).eq('user_id', user.id);
    toast.success('Avatar updated!');
    refreshProfile();
    setProfileData((p: any) => ({ ...p, avatar_url: publicUrl }));
  };

  // Analytics
  const totalItems = content.length;
  const typeCounts = content.reduce((acc, c) => { acc[c.type] = (acc[c.type] || 0) + 1; return acc; }, {} as Record<string, number>);
  const topCategory = Object.entries(typeCounts).sort(([, a], [, b]) => (b as number) - (a as number))[0];

  const wishlist = content.filter(c => c.status === 'wishlist');
  const watching = content.filter(c => c.status === 'watching');
  const completed = content.filter(c => c.status === 'completed');

  if (loading) return <div className="min-h-screen bg-background"><Navbar /><div className="flex items-center justify-center py-20 text-muted-foreground">Loading...</div></div>;
  if (!profileData) return <div className="min-h-screen bg-background"><Navbar /><div className="flex items-center justify-center py-20 text-muted-foreground">User not found</div></div>;

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="container max-w-6xl px-4 py-6">
        {/* Profile Header */}
        <div className="flex items-center gap-4 mb-8">
          <div className="relative">
            <div className="w-20 h-20 rounded-full bg-muted overflow-hidden flex items-center justify-center text-2xl font-bold text-muted-foreground">
              {profileData.avatar_url ? (
                <img src={profileData.avatar_url} alt="" className="w-full h-full object-cover" />
              ) : (
                profileData.username[0].toUpperCase()
              )}
            </div>
            {isOwner && (
              <label className="absolute -bottom-1 -right-1 bg-primary text-primary-foreground p-1 rounded-full cursor-pointer hover:bg-primary/90 transition-colors">
                <Upload size={12} />
                <input type="file" accept="image/*" className="hidden" onChange={handleAvatarUpload} />
              </label>
            )}
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground">@{profileData.username}</h1>
            <p className="text-sm text-muted-foreground">Joined {new Date(profileData.created_at).toLocaleDateString()}</p>
          </div>
        </div>

        {/* Analytics */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">
          <div className="bg-card border border-border/50 rounded-xl p-4">
            <p className="text-sm text-muted-foreground">Total Items</p>
            <p className="text-2xl font-bold text-foreground">{totalItems}</p>
          </div>
          <div className="bg-card border border-border/50 rounded-xl p-4">
            <p className="text-sm text-muted-foreground">Top Category</p>
            <p className="text-2xl font-bold text-foreground flex items-center gap-2">
              {topCategory ? (
                <>
                  {(() => { const I = typeIcons[topCategory[0]]; return I ? <I size={18} /> : null; })()}
                  {topCategory[1] as number}
                </>
              ) : '—'}
            </p>
          </div>
          <div className="bg-card border border-border/50 rounded-xl p-4">
            <p className="text-sm text-muted-foreground">Completed</p>
            <p className="text-2xl font-bold text-foreground">{completed.length}</p>
          </div>
        </div>

        {/* Content Sections */}
        {[
          { title: 'Wishlist', items: wishlist },
          { title: 'Watching', items: watching },
          { title: 'Completed', items: completed },
        ].map(section => section.items.length > 0 && (
          <div key={section.title} className="mb-8">
            <h2 className="text-lg font-semibold text-foreground mb-3">{section.title}</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {section.items.map(item => (
                <ContentCard key={item.id} item={item} />
              ))}
            </div>
          </div>
        ))}

        {content.length === 0 && (
          <div className="text-center py-16 text-muted-foreground">
            <p>No content added yet</p>
          </div>
        )}
      </main>
    </div>
  );
}
