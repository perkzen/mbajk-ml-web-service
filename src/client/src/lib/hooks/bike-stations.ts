import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import { getBikeStationByNumber, getBikeStations, getPredictions } from '@/lib/api';
import { BikeStation, Prediction } from '@/lib/models';
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


export const BIKE_STATION_PREDICTIONS_KEY = 'bike-station-predictions';
export const useBikeStationPredictions = (number: number, opts?: UseQueryOptions<Prediction[], AxiosError, Prediction[], (typeof BIKE_STATION_PREDICTIONS_KEY | number)[]>) => {
  return useQuery({
      queryKey: [BIKE_STATION_PREDICTIONS_KEY, number],
      queryFn: () => getPredictions(number),
    },
  );
};