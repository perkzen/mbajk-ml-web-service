import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import { useEffect } from 'react';
import { useBikeStations } from '@/lib/hooks/bike-stations';
import { useQueryParams } from '@/lib/hooks/use-querey-params';
import { useMap } from '@vis.gl/react-google-maps';
import { BikeStation } from '@/lib/models';
import { center, DEFAULT_ZOOM } from '@/components/map/bike-stations-map';


interface SearchMenuProps {
  open: boolean;
  setOpen: (open: boolean) => void;
}

export function SearchMenu({ open, setOpen }: SearchMenuProps) {
  const { data } = useBikeStations();
  const map = useMap();

  const { urlQuery, updateQueryParams } = useQueryParams();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen(!open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [open, setOpen]);

  const handleSelect = (station: BikeStation) => {
    setOpen(false);
    updateQueryParams({ ...urlQuery, station: station.number });

    map?.panTo({ lat: center.lat, lng: center.lng });
    map?.setZoom(DEFAULT_ZOOM);

    setTimeout(() => {
      map?.panTo({ lat: station.lat, lng: station.lon });
      map?.setZoom(18);
    }, 1000);


  };

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a location to find bike station..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Suggestions">
          {data?.map((station) => (
            <CommandItem key={station.number} onSelect={() => handleSelect(station)}>
              {station.name}
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
