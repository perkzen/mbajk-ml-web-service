import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('en-GB', {
    hour: 'numeric',
    minute: 'numeric',
  }).format(date);
};


export const timeSince = (date: number): string => {
  const now = new Date();
  const target = new Date(date);

  const timeDiff = now.getTime() - target.getTime();

  const seconds = Math.floor(timeDiff / 1000);

  const formatter = new Intl.RelativeTimeFormat('en', {
    numeric: 'auto',
  });

  if (seconds > 60) {
    const minutes = Math.floor(seconds / 60);
    return formatter.format(-minutes, 'minute');
  }

  return formatter.format(-seconds, 'second');

};