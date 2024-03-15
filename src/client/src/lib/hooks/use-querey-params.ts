'use client';
import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { BikeStation } from '@/lib/models';

export type DisplayProperty = Extract<keyof BikeStation, 'available_bikes' | 'available_bike_stands'>;

interface URLQueryParams {
  station: number | null;
  show: DisplayProperty;
}

export const useQueryParams = () => {
  const { push } = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const query = new URLSearchParams(searchParams);

  const updateQueryParams = (params: URLQueryParams) => {
    Object.entries(params).forEach(([key, value]) => {
      if (value) {
        query.set(key, value);
      } else {
        query.delete(key);
      }
    });

    push(`${pathname}?${query.toString()}`);
  };

  const deleteQueryParams = (name: string) => {
    query.delete(name);

    push(`?${query.toString()}`);
  };

  const parseQueryParams = (): URLQueryParams => {
    return {
      station: Number(query.get('station')),
      show: query.get('show') as DisplayProperty || 'available_bike_stands',
    };
  };

  return {
    updateQueryParams,
    deleteQueryParams,
    urlQuery: parseQueryParams(),
  };
};