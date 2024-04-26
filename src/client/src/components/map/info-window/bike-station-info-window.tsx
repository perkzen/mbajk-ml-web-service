import { DrawerClose, DrawerContent, DrawerDescription, DrawerHeader, DrawerTitle } from '@/components/ui/drawer';
import { useBikeStationByNumber, useBikeStationPredictions } from '@/lib/hooks/bike-stations';
import { useQueryParams } from '@/lib/hooks/use-querey-params';
import { timeSince } from '@/lib/utils';
import { Bike, ParkingSquare, X } from 'lucide-react';
import PredictionsTable from '@/components/map/info-window/predictions-table';
import { Skeleton } from '@/components/ui/skeleton';


interface BikeStationInfoWindowProps {
  onClose: () => void;
}

const BikeStationInfoWindow = ({ onClose }: BikeStationInfoWindowProps) => {
  const { urlQuery } = useQueryParams();

  const { data, isLoading } = useBikeStationByNumber(Number(urlQuery.station), {
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
      className="flex flex-col rounded-t-[10px] h-full  w-full sm:w-[400px] fixed top-20  bottom-0 left-0">
      <div className="mx-auto w-full max-w-sm">
        <DrawerHeader>
          <div className={'flex flex-row'}>
            <DrawerTitle className={'flex flex-row text-wrap text-start'}>
              <div className={'leading-6'}>
                {isLoading ? <Skeleton className="w-[300px] h-[20px] rounded-md" />
                  :
                  <>
                    {data?.name}
                    <span className={'font-light text-gray-400'}> - n&apos;{data?.number}</span>
                  </>}
              </div>
            </DrawerTitle>
            <DrawerClose onClick={onClose} className={'ml-auto self-start pl-2'}>
              <X width={16} height={16} />
            </DrawerClose>
          </div>
          {isLoading ? <Skeleton className="w-[100px] h-[20px] rounded-md" /> :
            <DrawerDescription className={'text-start'}>
              Last updated: {timeSince(Number(data?.last_updated))}
            </DrawerDescription>}
        </DrawerHeader>
        <div className="flex flex-col p-4 gap-8">
          <div className="flex flex-row gap-4">


            <div className="flex flex-col gap-2">
              <div className={'flex flex-row items-center gap-2'}>
                <Bike size={24} />
                {isLoading ? <Skeleton className="w-[32px] h-[28px] rounded-md" /> :
                  <div className="text-xl font-semibold text-primary">{data?.available_bikes}</div>}
              </div>
              <div className="text-gray-400">Available bikes</div>
            </div>


            <div className="flex flex-col gap-2">
              <div className={'flex flex-row items-center gap-2'}>
                <ParkingSquare size={24} />
                {isLoading ? <Skeleton className="w-[32px] h-[28px] rounded-md" /> :
                  <div className="text-xl font-semibold text-primary">{data?.available_bike_stands}</div>}
              </div>
              <div className="text-gray-400">Available stands</div>
            </div>
          </div>

          <PredictionsTable data={predictions || []} isLoading={isLoadingPredictions} />

        </div>
      </div>
    </DrawerContent>
  );
};

export default BikeStationInfoWindow;