import { cn } from '@/lib/utils';

const statusConfig = {
  wishlist: { label: 'Wishlist', className: 'bg-muted text-badge-wishlist' },
  watching: { label: 'Watching', className: 'bg-primary/10 text-badge-watching' },
  completed: { label: 'Completed', className: 'bg-green-50 text-badge-completed' },
};

export function StatusBadge({ status }: { status: string }) {
  const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.wishlist;
  return (
    <span className={cn('inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium', config.className)}>
      {config.label}
    </span>
  );
}
