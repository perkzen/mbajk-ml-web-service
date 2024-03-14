import { api } from '@/lib/axios';
import { AxiosResponse } from 'axios';

export const getBikeStations = async () => {
  const res = (await api.get('/mbajk/stations')) as AxiosResponse<BikeStation[]>;
  return res.data;
};