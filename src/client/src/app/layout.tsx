import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import {ReactNode, Suspense} from 'react';
import Navbar from '@/components/ui/navbar';
import { cn } from '@/lib/utils';
import Providers from '@/components/providers/providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'MBajk AI',
  description: 'MBajk AI is a smarter way to use Mbjak',
};

export default function RootLayout({
                                     children,
                                   }: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
    <body className={cn(inter.className, 'flex flex-col w-full min-h-screen')}>
    <Providers>
      <Navbar />
      <main className={'flex flex-1 flex-col w-full'}>
        <Suspense fallback={<div>Loading...</div>}>
            {children}
        </Suspense>
      </main>
    </Providers>
    </body>
    </html>
  );
}
