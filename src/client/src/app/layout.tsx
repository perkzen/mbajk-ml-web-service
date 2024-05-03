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
  keywords: ['MBajk', 'AI', "domen perko", "perkzen", "mbajk ai"],
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL as string),
  applicationName: 'MBajk AI'
};

export default function RootLayout({
                                     children,
                                   }: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
    <body className={cn(inter.className, 'flex flex-col w-full h-svh')}>
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
