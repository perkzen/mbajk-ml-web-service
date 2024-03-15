import { api } from '@/lib/axios';
import { AxiosResponse } from 'axios';
import { BikeStation, Prediction } from '@/lib/models';

export const getBikeStations = async () => {
  const res = (await api.get('/mbajk/stations')) as AxiosResponse<BikeStation[]>;
  return res.data;
};

export const getBikeStationByNumber = async (number: number) => {
  const res = (await api.get(`/mbajk/stations/${number}`)) as AxiosResponse<BikeStation>;
  return res.data;
};


export const getPredictions = async (numberOfPredictions: number) => {
  const res = (await api.get(`/mbajk/predict/${numberOfPredictions}`)) as AxiosResponse<Prediction[]>;
  return res.data;
};