import React from 'react';
import { LocateIcon, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';

const MapActions = () => {
  return (
    <div className={'flex flex-col gap-4 absolute bottom-8 right-4'}>
      <Button variant={'default'} size={'icon'} className={'rounded-full '}>
        <LocateIcon size={24} />
      </Button>
      <Button variant={'default'} size={'icon'} className={'rounded-full '}>
        <Search size={24} />
      </Button>
    </div>
  );
};

export default MapActions;