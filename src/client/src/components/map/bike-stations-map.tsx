'use client';
import { useState } from 'react';
import { env } from '@/env.mjs';
import { APIProvider, Map as GoogleMap } from '@vis.gl/react-google-maps';
import StationMarker from '@/components/map/station-marker';
import { Drawer } from '@/components/ui/drawer';
import BikeStationInfoWindow from '@/components/map/info-window/bike-station-info-window';
import { useQueryParams } from '@/lib/hooks/use-querey-params';
import { useBikeStations } from '@/lib/hooks/bike-stations';


const center = {
  lat: 46.5590,
  lng: 15.6381,
};


const BikeStationsMap = () => {
  const { data: stations = [] } = useBikeStations();

  const [isOpen, setIsOpen] = useState(false);
  const { urlQuery, updateQueryParams, deleteQueryParams } = useQueryParams();

  const handleOpen = (stationNumber: number) => {
    updateQueryParams({ station: stationNumber });
    setIsOpen(true);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleOpenChange = (open: boolean) => {
    if (!open) {
      deleteQueryParams('station');
    }

    setIsOpen(open);
  };

  return (
    <Drawer open={isOpen} dismissible={true} direction={'left'} onOpenChange={handleOpenChange}>
      <APIProvider apiKey={env.NEXT_PUBLIC_GOOGLE_MAPS_KEY}>
        <GoogleMap
          defaultCenter={center}
          defaultZoom={14}
          gestureHandling={'greedy'}
          disableDefaultUI={true}
          className={'w-full h-full flex-grow'}
          mapId={'google-map-id'}
        >
          {stations.map((station) => (
            <StationMarker station={station} key={station.number} onClick={() => handleOpen(station.number)} />
          ))}
        </GoogleMap>
      </APIProvider>
      <BikeStationInfoWindow handleClose={handleClose} />
    </Drawer>);
};

export default BikeStationsMap;