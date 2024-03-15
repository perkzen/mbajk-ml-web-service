import { DrawerContent, DrawerDescription, DrawerFooter, DrawerHeader, DrawerTitle } from '@/components/ui/drawer';
import { Button } from '@/components/ui/button';
import { useBikeStationByNumber } from '@/lib/hooks/bike-stations';
import { useQueryParams } from '@/lib/hooks/use-querey-params';
import { timeSince } from '@/lib/utils';
import { Bike, ParkingSquare } from 'lucide-react';
import PredictionsTable from '@/components/map/info-window/predictions-table';

interface BikeStationInfoWindowProps {
  handleClose: () => void;
}

const BikeStationInfoWindow = ({ handleClose }: BikeStationInfoWindowProps) => {
  const { urlQuery } = useQueryParams();


  const { data } = useBikeStationByNumber(Number(urlQuery.station), {
    enabled: !!urlQuery.station,
  });

  return (
    <DrawerContent className="flex flex-col rounded-t-[10px] h-full w-[400px] mt-24 fixed top-2 bottom-0 left-0">
      <div className="mx-auto w-full max-w-sm">
        <DrawerHeader>
          <DrawerTitle className={'flex flex-row gap-2'}>{data?.name}
            <div className={'font-light text-gray-400'}> - n'{data?.number}</div>
          </DrawerTitle>
          <DrawerDescription>Last updated: {timeSince(Number(data?.last_updated))}</DrawerDescription>
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


          <PredictionsTable />

        </div>
      </div>
    </DrawerContent>
  );
};

export default BikeStationInfoWindow;