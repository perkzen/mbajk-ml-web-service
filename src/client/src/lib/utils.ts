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
  const now = Date.now();
  const seconds = Math.floor((now - date) / 1000);

  const intervals = {
    year: Math.floor(seconds / 31536000),
    month: Math.floor(seconds / 2592000),
    day: Math.floor(seconds / 86400),
    hour: Math.floor(seconds / 3600),
    minute: Math.floor(seconds / 60),
    second: Math.floor(seconds),
  };

  if (intervals.year > 1) {
    return intervals.year + ' years';
  } else if (intervals.month > 1) {
    return intervals.month + ' months';
  } else if (intervals.day > 1) {
    return intervals.day + ' days';
  } else if (intervals.hour > 1) {
    return intervals.hour + ' h';
  } else if (intervals.minute >= 1) {
    return intervals.minute + ' min';
  } else {
    return intervals.second + ' s';
  }
};