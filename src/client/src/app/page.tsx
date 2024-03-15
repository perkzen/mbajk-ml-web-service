import BikeStationsMap from '@/components/bike-stations-map';
import { getBikeStations } from '@/lib/api';

export default async function Home() {
  const stations = await getBikeStations();

  return (
    <main className="flex w-full min-h-screen">
      <BikeStationsMap stations={stations} />
    </main>
  );
}
