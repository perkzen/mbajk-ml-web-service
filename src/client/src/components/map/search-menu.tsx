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


interface SearchMenuProps {
  open: boolean;
  setOpen: (open: boolean) => void;
}

export function SearchMenu({ open, setOpen }: SearchMenuProps) {
  const { data } = useBikeStations();

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

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a location to find bike station..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Suggestions">
          {data?.map((station) => (
            <CommandItem key={station.number} onSelect={() => {
              updateQueryParams({ ...urlQuery, station: station.number });
              setOpen(false);
            }}>
              {station.name}
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
