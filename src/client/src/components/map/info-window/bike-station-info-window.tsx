import { DrawerContent, DrawerDescription, DrawerHeader, DrawerTitle } from '@/components/ui/drawer';
import { useBikeStationByNumber, useBikeStationPredictions } from '@/lib/hooks/bike-stations';
import { useQueryParams } from '@/lib/hooks/use-querey-params';
import { timeSince } from '@/lib/utils';
import { Bike, ParkingSquare } from 'lucide-react';
import PredictionsTable from '@/components/map/info-window/predictions-table';
import LoadingProvider from '@/components/providers/loading-provider';


const BikeStationInfoWindow = () => {
  const { urlQuery } = useQueryParams();

  const { data, isLoading, isFetching } = useBikeStationByNumber(Number(urlQuery.station), {
    enabled: Number(urlQuery.station) > 0,
  });

  const {
    data: predictions,
    isLoading: isLoadingPredictions,
  } = useBikeStationPredictions(Number(urlQuery.station), 7, {
    enabled: Number(urlQuery.station) > 0,
  });

  return (
    <DrawerContent
      className="flex flex-col rounded-t-[10px] h-full  w-full sm:w-[400px] fixed top-20 sm:top-24 bottom-0 left-0">
      <LoadingProvider isLoading={isLoading || isFetching}>
        <div className="mx-auto w-full max-w-sm">
          <DrawerHeader>
            <DrawerTitle className={'flex flex-row text-wrap'}>
              <div className={'leading-6'}>
                {data?.name}
                <span className={'font-light text-gray-400'}> - n&apos;{data?.number}</span>
              </div>
            </DrawerTitle>
            <DrawerDescription className={'text-start'}>Last
              updated: {timeSince(Number(data?.last_updated))}</DrawerDescription>
          </DrawerHeader>
          <div className="flex flex-col p-4 pb-0 gap-8">
            <div className="flex flex-row gap-4">


              <div className="flex flex-col gap-2">
                <div className={'flex flex-row items-center gap-2'}>
                  <Bike size={24} />
                  <div className="text-xl font-semibold text-primary">{data?.available_bikes}</div>
                </div>
                <div className="text-gray-400">Available bikes</div>
              </div>


              <div className="flex flex-col gap-2">
                <div className={'flex flex-row items-center gap-2'}>
                  <ParkingSquare size={24} />
                  <div className="text-xl font-semibold text-primary">{data?.available_bike_stands}</div>
                </div>
                <div className="text-gray-400">Available stands</div>
              </div>

            </div>


            <PredictionsTable data={predictions || []} isLoading={isLoadingPredictions} />

          </div>
        </div>
      </LoadingProvider>
    </DrawerContent>
  );
};

export default BikeStationInfoWindow;