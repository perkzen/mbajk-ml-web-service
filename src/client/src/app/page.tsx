import BikeStationsMap from '@/components/map/bike-stations-map';
import { getBikeStations } from '@/lib/api';
import { QueryClient } from '@tanstack/react-query';
import { BIKE_STATIONS_KEY } from '@/lib/hooks/bike-stations';

export default async function Home() {
  const queryClient = new QueryClient();

  await queryClient.prefetchQuery({
    queryKey: [BIKE_STATIONS_KEY],
    queryFn: getBikeStations,
  });


  return (
    <div className={'flex flex-grow flex-col w-full'}>
      <BikeStationsMap  />
    </div>
  );
}
