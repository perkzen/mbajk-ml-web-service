import {
  ColumnDef,
  getCoreRowModel,
} from '@tanstack/table-core';
import { flexRender, useReactTable } from '@tanstack/react-table';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Prediction } from '@/lib/models';
import { ParkingSquare } from 'lucide-react';
import { formatDate } from '@/lib/utils';
import { Skeleton } from '@/components/ui/skeleton';


export const columns: ColumnDef<Prediction>[] = [
  {
    accessorKey: 'date',
    header: 'Time',
    cell: ({ row }) => (
      <div>{formatDate(row.getValue('date'))}</div>
    ),
  },
  {
    accessorKey: 'prediction',
    header: 'Available stands',
    cell: ({ row }) => (
      <div className={'flex flex-row items-center gap-2'}>
        <ParkingSquare size={16} />
        <div className={'font-semibold text-primary'}>{row.getValue('prediction')}</div>
      </div>),

  },
];

const PredictionsTable = ({ data, isLoading }: { data: Prediction[], isLoading: boolean }) => {

  const table = useReactTable({
    data: data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });


  return (
    <div className={'flex flex-col gap-2 mb-2'}>
      <h1 className="text-lg font-semibold">
        Available stands predictions
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
              ) : !isLoading ? (
                  <TableRow>
                    <TableCell
                      colSpan={columns.length}
                      className="h-24 text-center"
                    >
                      No results.
                    </TableCell>
                  </TableRow>
                ) :
                <>
                  {Array.from({ length: 7 }, (_, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <Skeleton className="w-full h-[20px] rounded-full" />
                      </TableCell>
                      <TableCell>
                        <Skeleton className="w-full h-[20px] rounded-full" />
                      </TableCell>
                    </TableRow>))}
                </>
              }
            </TableBody>
          </Table>
        </div>
      </div>
    </div>

  );
};

export default PredictionsTable;