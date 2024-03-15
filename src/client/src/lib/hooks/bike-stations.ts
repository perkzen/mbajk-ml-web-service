import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { getBikeStationByNumber, getBikeStations } from '@/lib/api';
import { BikeStation } from '@/lib/models';
import { AxiosError } from 'axios';

export const BIKE_STATIONS_KEY = 'bike-stations';

export const useBikeStations = (opts?: UseQueryOptions<BikeStation[], AxiosError, BikeStation[], [typeof BIKE_STATIONS_KEY]>) => {
  return useQuery({
      queryKey: [BIKE_STATIONS_KEY],
      queryFn: getBikeStations,
      ...opts,
    },
  );
};

export const BIKE_STATION_BY_NUMBER_KEY = 'bike-station-by-number';

export const useBikeStationByNumber = (number: number, opts?: Omit<UseQueryOptions<BikeStation, AxiosError, BikeStation, [typeof BIKE_STATION_BY_NUMBER_KEY, number]>, 'queryKey'>) => {
  return useQuery({
      queryKey: [BIKE_STATION_BY_NUMBER_KEY, number],
      queryFn: () => getBikeStationByNumber(number),
      ...opts,
    },
  );
};

