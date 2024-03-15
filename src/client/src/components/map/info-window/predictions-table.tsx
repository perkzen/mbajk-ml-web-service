import {
  ColumnDef,
  getCoreRowModel,
} from '@tanstack/table-core';
import { flexRender, useReactTable } from '@tanstack/react-table';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { BikeStationPrediction } from '@/lib/models';
import { Bike } from 'lucide-react';


const data: BikeStationPrediction[] = [
  { available_bike_stands: 10, date: '7:00' },
  { available_bike_stands: 9, date: '8:00' },
  { available_bike_stands: 8, date: '9:00' },
  { available_bike_stands: 7, date: '10:00' },
  { available_bike_stands: 6, date: '11:00' },
  { available_bike_stands: 5, date: '12:00' },
  { available_bike_stands: 4, date: '13:00' },
];

export const columns: ColumnDef<BikeStationPrediction>[] = [

  {
    accessorKey: 'date',
    header: 'Hour',
    cell: ({ row }) => (
      <div>{row.getValue('date')}</div>
    ),
  },
  {
    accessorKey: 'available_bike_stands',
    header: () => {
      return <div className={'flex flex-row items-center gap-2'}>
        {/*<Bike size={16} />*/}
        <div>Available bike stands</div>
      </div>;
    },
    cell: ({ row }) => (
      <div className={'flex flex-row items-center gap-2'}>
        <Bike size={16} />
        <div className={'font-semibold text-primary'}>{row.getValue('available_bike_stands')}</div>
      </div>),

  },
];

const PredictionsTable = () => {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });


  return (
    <div className={'flex flex-col gap-2'}>
      <h1 className="text-xl font-semibold">
        Predictions
      </h1>
      <div className="w-full">
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => {
                    return (
                      <TableHead key={header.id}>
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                            header.column.columnDef.header,
                            header.getContext(),
                          )}
                      </TableHead>
                    );
                  })}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows?.length ? (
                table.getRowModel().rows.map((row) => (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && 'selected'}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext(),
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={columns.length}
                    className="h-24 text-center"
                  >
                    No results.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

      </div>

    </div>

  )
    ;
};

export default PredictionsTable;