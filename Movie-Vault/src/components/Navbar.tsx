import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { LogOut, User, Users, LayoutGrid, Menu, X } from 'lucide-react';
import { useState } from 'react';

export function Navbar() {
  const { user, profile, signOut } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-border/50 bg-card/80 backdrop-blur-md">
      <div className="container flex items-center justify-between h-14 px-4">
        <Link to="/" className="text-lg font-bold text-foreground tracking-tight">
          Movie <span className="text-primary">Vault</span>
        </Link>

        {/* Desktop nav */}
        {user && (
          <nav className="hidden md:flex items-center gap-1">
            <Button variant="ghost" size="sm" asChild>
              <Link to="/"><LayoutGrid size={16} className="mr-1.5" />Dashboard</Link>
            </Button>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/users"><Users size={16} className="mr-1.5" />Users</Link>
            </Button>
            <Button variant="ghost" size="sm" asChild>
              <Link to={`/profile/${profile?.username || ''}`}><User size={16} className="mr-1.5" />Profile</Link>
            </Button>
            <Button variant="ghost" size="sm" onClick={() => { signOut(); navigate('/login'); }}>
              <LogOut size={16} className="mr-1.5" />Logout
            </Button>
          </nav>
        )}

        {/* Mobile hamburger */}
        {user && (
          <button className="md:hidden p-2" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        )}

        {!user && (
          <div className="flex gap-2">
            <Button variant="ghost" size="sm" asChild><Link to="/login">Login</Link></Button>
            <Button size="sm" asChild><Link to="/signup">Sign Up</Link></Button>
          </div>
        )}
      </div>

      {/* Mobile menu */}
      {menuOpen && user && (
        <nav className="md:hidden border-t border-border/50 bg-card p-4 space-y-2">
          <Button variant="ghost" className="w-full justify-start" onClick={() => { navigate('/'); setMenuOpen(false); }}>
            <LayoutGrid size={16} className="mr-2" />Dashboard
          </Button>
          <Button variant="ghost" className="w-full justify-start" onClick={() => { navigate('/users'); setMenuOpen(false); }}>
            <Users size={16} className="mr-2" />Users
          </Button>
          <Button variant="ghost" className="w-full justify-start" onClick={() => { navigate(`/profile/${profile?.username || ''}`); setMenuOpen(false); }}>
            <User size={16} className="mr-2" />Profile
          </Button>
          <Button variant="ghost" className="w-full justify-start" onClick={() => { signOut(); navigate('/login'); setMenuOpen(false); }}>
            <LogOut size={16} className="mr-2" />Logout
          </Button>
        </nav>
      )}
    </header>
  );
}
