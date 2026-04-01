import { useState, useEffect, useMemo } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/integrations/supabase/client';
import { ContentCard } from '@/components/ContentCard';
import { ContentModal } from '@/components/ContentModal';
import { DeleteConfirmDialog } from '@/components/DeleteConfirmDialog';
import { Navbar } from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Plus, Search, Film, Tv, Gamepad2, Youtube, Zap, PackageOpen } from 'lucide-react';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';

const CATEGORIES = [
  { key: 'all', label: 'All', icon: null },
  { key: 'movie', label: 'Movies', icon: Film },
  { key: 'series', label: 'Series', icon: Tv },
  { key: 'game', label: 'Games', icon: Gamepad2 },
  { key: 'youtube', label: 'YouTube', icon: Youtube },
  { key: 'productivity', label: 'Productivity', icon: Zap },
];

export default function Dashboard() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [content, setContent] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState<string | null>(null);
  const [deleteId, setDeleteId] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) navigate('/login');
  }, [user, authLoading, navigate]);

  const fetchContent = async () => {
    if (!user) return;
    setLoading(true);
    const { data, error } = await supabase
      .from('content')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });
    if (error) toast.error('Failed to load content');
    else setContent(data || []);
    setLoading(false);
  };

  useEffect(() => { if (user) fetchContent(); }, [user]);

  const filtered = useMemo(() => {
    let items = content;
    if (category !== 'all') items = items.filter(i => i.type === category);
    if (statusFilter !== 'all') items = items.filter(i => i.status === statusFilter);
    if (search) items = items.filter(i => i.title.toLowerCase().includes(search.toLowerCase()));
    if (sortBy === 'oldest') items = [...items].reverse();
    return items;
  }, [content, category, statusFilter, search, sortBy]);

  const handleDelete = async () => {
    if (!deleteId) return;
    const { error } = await supabase.from('content').delete().eq('id', deleteId);
    if (error) toast.error('Delete failed');
    else { toast.success('Deleted'); fetchContent(); }
    setDeleteId(null);
  };

  const deleteItem = content.find(c => c.id === deleteId);

  if (authLoading) return <div className="min-h-screen flex items-center justify-center bg-background"><div className="animate-pulse text-muted-foreground">Loading...</div></div>;

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="container px-4 py-6 max-w-6xl">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <h1 className="text-2xl font-bold text-foreground">My Collection</h1>
          <Button onClick={() => { setEditId(null); setModalOpen(true); }} className="shadow-lg shadow-primary/20">
            <Plus size={16} className="mr-1.5" />Add Content
          </Button>
        </div>

        {/* Filters */}
        <div className="space-y-4 mb-6">
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <Input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search by title..." className="pl-9" />
          </div>

          {/* Category tabs */}
          <div className="flex gap-1.5 overflow-x-auto pb-1">
            {CATEGORIES.map(cat => (
              <button
                key={cat.key}
                onClick={() => setCategory(cat.key)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                  category === cat.key
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground hover:text-foreground'
                }`}
              >
                {cat.icon && <cat.icon size={14} />}
                {cat.label}
              </button>
            ))}
          </div>

          <div className="flex gap-2">
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[140px]"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="wishlist">Wishlist</SelectItem>
                <SelectItem value="watching">Watching</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
              </SelectContent>
            </Select>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-[120px]"><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="newest">Newest</SelectItem>
                <SelectItem value="oldest">Oldest</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Content Grid */}
        {loading ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {Array.from({ length: 10 }).map((_, i) => (
              <div key={i} className="rounded-xl bg-muted animate-pulse aspect-[2/3]" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-20">
            <PackageOpen size={48} className="mx-auto text-muted-foreground/30 mb-4" />
            <h3 className="text-lg font-semibold text-foreground mb-1">No content yet</h3>
            <p className="text-muted-foreground text-sm">Add your first movie, series, or game to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {filtered.map((item, i) => (
              <div key={item.id} className="animate-fade-in" style={{ animationDelay: `${i * 50}ms` }}>
                <ContentCard
                  item={item}
                  isOwner
                  onEdit={(id) => { setEditId(id); setModalOpen(true); }}
                  onDelete={(id) => setDeleteId(id)}
                />
              </div>
            ))}
          </div>
        )}
      </main>

      <ContentModal open={modalOpen} onClose={() => setModalOpen(false)} editId={editId} onSaved={fetchContent} />
      <DeleteConfirmDialog
        open={!!deleteId}
        onClose={() => setDeleteId(null)}
        onConfirm={handleDelete}
        title={deleteItem?.title}
      />
    </div>
  );
}
