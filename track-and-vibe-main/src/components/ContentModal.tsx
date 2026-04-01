import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { supabase } from '@/integrations/supabase/client';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';
import { Upload } from 'lucide-react';

const GENRES = ['Action', 'Comedy', 'Drama', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Anime', 'Documentary'];
const TYPES = [
  { value: 'movie', label: 'Movie 🎬' },
  { value: 'series', label: 'Web Series 📺' },
  { value: 'game', label: 'Game 🎮' },
  { value: 'youtube', label: 'YouTube ▶️' },
  { value: 'productivity', label: 'Productivity ⚡' },
];

interface ContentModalProps {
  open: boolean;
  onClose: () => void;
  editId?: string | null;
  onSaved: () => void;
}

export function ContentModal({ open, onClose, editId, onSaved }: ContentModalProps) {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [form, setForm] = useState({
    title: '', type: 'movie', genre: '', rating: 0, review: '',
    image_url: '', status: 'wishlist', year: new Date().getFullYear(), seasons: 1,
  });

  useEffect(() => {
    if (editId && open) {
      supabase.from('content').select('*').eq('id', editId).single().then(({ data }) => {
        if (data) setForm({
          title: data.title,
          type: data.type,
          genre: data.genre || '',
          rating: Number(data.rating) || 0,
          review: data.review || '',
          image_url: data.image_url || '',
          status: data.status,
          year: data.year,
          seasons: data.seasons || 1,
        });
      });
    } else if (open) {
      setForm({ title: '', type: 'movie', genre: '', rating: 0, review: '', image_url: '', status: 'wishlist', year: new Date().getFullYear(), seasons: 1 });
    }
  }, [editId, open]);

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !user) return;
    setUploading(true);
    const ext = file.name.split('.').pop();
    const path = `${user.id}/${Date.now()}.${ext}`;
    const { error } = await supabase.storage.from('movie-posters').upload(path, file);
    if (error) {
      toast.error('Upload failed');
      setUploading(false);
      return;
    }
    const { data: { publicUrl } } = supabase.storage.from('movie-posters').getPublicUrl(path);
    setForm(f => ({ ...f, image_url: publicUrl }));
    setUploading(false);
  };

  const handleSave = async () => {
    if (!user || !form.title || !form.year) {
      toast.error('Title and year are required');
      return;
    }
    setLoading(true);
    const payload = {
      title: form.title,
      type: form.type,
      genre: ['game', 'productivity'].includes(form.type) ? null : (form.genre || null),
      rating: form.rating,
      review: form.review || null,
      image_url: form.image_url || null,
      status: form.status,
      year: form.year,
      seasons: ['series', 'youtube'].includes(form.type) ? form.seasons : null,
      user_id: user.id,
    };

    const { error } = editId
      ? await supabase.from('content').update(payload).eq('id', editId)
      : await supabase.from('content').insert(payload);

    if (error) {
      toast.error(error.message);
    } else {
      toast.success(editId ? 'Updated!' : 'Added!');
      onSaved();
      onClose();
    }
    setLoading(false);
  };

  const showGenre = !['game', 'productivity'].includes(form.type);
  const showSeasons = ['series', 'youtube'].includes(form.type);

  return (
    <Dialog open={open} onOpenChange={() => onClose()}>
      <DialogContent className="max-w-md max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{editId ? 'Edit Content' : 'Add Content'}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <Label>Title *</Label>
            <Input value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} placeholder="Enter title" />
          </div>
          <div>
            <Label>Type</Label>
            <Select value={form.type} onValueChange={v => setForm(f => ({ ...f, type: v }))}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                {TYPES.map(t => <SelectItem key={t.value} value={t.value}>{t.label}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          {showGenre && (
            <div>
              <Label>Genre</Label>
              <Select value={form.genre} onValueChange={v => setForm(f => ({ ...f, genre: v }))}>
                <SelectTrigger><SelectValue placeholder="Select genre" /></SelectTrigger>
                <SelectContent>
                  {GENRES.map(g => <SelectItem key={g} value={g}>{g}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          )}
          <div>
            <Label>Year *</Label>
            <Input type="number" value={form.year} onChange={e => setForm(f => ({ ...f, year: parseInt(e.target.value) || 0 }))} />
          </div>
          {showSeasons && (
            <div>
              <Label>Seasons</Label>
              <Input type="number" min={1} value={form.seasons} onChange={e => setForm(f => ({ ...f, seasons: parseInt(e.target.value) || 1 }))} />
            </div>
          )}
          <div>
            <Label>Rating: {form.rating.toFixed(1)}</Label>
            <Slider min={0} max={5} step={0.1} value={[form.rating]} onValueChange={([v]) => setForm(f => ({ ...f, rating: v }))} className="mt-2" />
          </div>
          <div>
            <Label>Status</Label>
            <Select value={form.status} onValueChange={v => setForm(f => ({ ...f, status: v }))}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="wishlist">Wishlist</SelectItem>
                <SelectItem value="watching">Watching</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label>Review</Label>
            <Textarea value={form.review} onChange={e => setForm(f => ({ ...f, review: e.target.value }))} placeholder="Write your review..." rows={3} />
          </div>
          <div>
            <Label>Image</Label>
            {form.image_url && (
              <img src={form.image_url} alt="Preview" className="w-full h-32 object-cover rounded-lg mb-2" />
            )}
            <label className="flex items-center gap-2 cursor-pointer border border-dashed border-border rounded-lg p-3 hover:bg-muted/50 transition-colors">
              <Upload size={16} className="text-muted-foreground" />
              <span className="text-sm text-muted-foreground">{uploading ? 'Uploading...' : 'Upload image'}</span>
              <input type="file" accept="image/*" className="hidden" onChange={handleImageUpload} disabled={uploading} />
            </label>
          </div>
          <Button onClick={handleSave} disabled={loading} className="w-full">
            {loading ? 'Saving...' : editId ? 'Update' : 'Add'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
