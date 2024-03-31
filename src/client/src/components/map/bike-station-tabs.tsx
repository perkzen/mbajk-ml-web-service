'use client';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Bike, ParkingSquare } from 'lucide-react';
import { DisplayProperty, useQueryParams } from '@/lib/hooks/use-querey-params';

const BikeStationTabs = () => {
  const { urlQuery, updateQueryParams } = useQueryParams();

  const handleClick = (value: DisplayProperty) => {
    updateQueryParams({ ...urlQuery, show: value });
  };


  return (
    <Tabs value={urlQuery.show} className="absolute top-6 left-1/2 transform -translate-x-1/2" onValueChange={v => handleClick(v as DisplayProperty)}>
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value={'available_bikes'}>
          <div className={'flex flex-row items-center gap-2'}>
            <Bike size={16} />
            <div className={'hidden sm:block'}>
              Available bikes
            </div>
          </div>
        </TabsTrigger>
        <TabsTrigger value={'available_bike_stands'}>
          <div className={'flex flex-row items-center gap-2'}>
            <ParkingSquare size={16} />
            <div className={"hidden sm:block"}>
              Free bike stands
            </div>
          </div>
        </TabsTrigger>
      </TabsList>
    </Tabs>
  );
};

export default BikeStationTabs;