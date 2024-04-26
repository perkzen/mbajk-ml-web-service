'use client';
import { LocateIcon, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { SearchMenu } from '@/components/map/search-menu';
import { useMap } from '@vis.gl/react-google-maps';
import { useState } from 'react';

const MapActions = () => {
  const [open, setOpen] = useState(false);

  const map = useMap();

  const centerCamera = () => {
    map?.panTo({ lat: 46.5590, lng: 15.6381 });
  };

  return (

    <div className={'flex flex-col gap-4 absolute bottom-8 right-4'}>
      <Button variant={'secondary'} size={'icon'} className={'rounded-full'} onClick={centerCamera}>
        <LocateIcon size={24} />
      </Button>
      <Button variant={'default'} size={'icon'} className={'rounded-full'} onClick={() => setOpen(true)}>
        <Search size={24} />
      </Button>
      <SearchMenu open={open} setOpen={setOpen} />
    </div>
  );
};

export default MapActions;