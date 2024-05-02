import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ReactNode, Suspense } from 'react';
import Navbar from '@/components/ui/navbar';
import { cn } from '@/lib/utils';
import Providers from '@/components/providers/providers';
import LoadingSpinner from '@/components/ui/loading-spinner';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'MBajk AI',
  description: 'MBajk AI is a smarter way to use Mbjak',
  authors: { url: 'https://www.domenperko.com/', name: 'Domen Perko' },
  keywords: ['MBajk', 'AI'],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: process.env.NEXT_PUBLIC_SITE_URL,
    images: [
      {
        url: `${process.env.NEXT_PUBLIC_SITE_URL}/opengraph-image.png`,
        width: 1200,
        height: 630,
        alt: 'MBajk AI',
      },
    ],
  },
};

export default function RootLayout({
                                     children,
                                   }: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
    <head>
      <meta property="og:image" content="<generated>" />
      <meta property="og:image:type" content="<generated>" />
      <meta property="og:image:width" content="<generated>" />
      <meta property="og:image:height" content="<generated>" />
    </head>
    <body className={cn(inter.className, 'flex flex-col w-full min-h-screen')}>
    <Providers>
      <Navbar />
      <main className={'flex-1 flex flex-col w-full bg-slate-200'}>
        <Suspense fallback={
          <div className={'self-center my-auto'}>
            <LoadingSpinner className={'w-8 h-8'} />
          </div>}
        >
          {children}
        </Suspense>
      </main>
    </Providers>
    </body>
    </html>
  );
}
