import BikeStationsMap from '@/components/bike-stations-map';
import { getBikeStations } from '@/lib/api';

export default async function Home() {
  const locations = await getBikeStations();
  console.log(locations);

  return (
    <main className="flex w-full min-h-screen bg-red-400 flex-col">
      <BikeStationsMap />
    </main>
  );
}
