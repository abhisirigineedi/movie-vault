# Movie Vault

Movie Vault is a comprehensive personal library tracker that helps you manage your movies, TV series, games, YouTube content, and productivity tools all in one place.

## Features

- **Centralized Tracking:** Organize your media into Wishlist, Watching, and Completed categories.
- **Categorization:** Easily filter your content by Movies, Series, Games, YouTube, and Productivity.
- **User Authentication:** Secure access powered by Supabase.
- **Responsive Design:** A modern, clean UI built with React, Vite, Tailwind CSS, and shadcn/ui.

## Technologies Used

- [React](https://reactjs.org/) & [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Supabase](https://supabase.com/) (Auth & Database)

## Getting Started

### Prerequisites

- Node.js installed
- A Supabase project with a `content` table (or use the provided migrations if applicable).

### Installation

1. Clone the repository and navigate into the `track-and-vibe-main` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables for Supabase in a `.env` file:
   ```env
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```

## Deployment

The project is configured for deployment on Vercel.

1. Import the project into your Vercel dashboard.
2. Add your `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` to the Vercel Environment Variables settings.
3. Deploy! A custom `vercel.json` is included to handle React Router client-side routing.
