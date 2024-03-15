import { ReactNode } from 'react';
import LoadingSpinner from '@/components/ui/loading-spinner';

interface LoadingProviderProps {
  isLoading: boolean;
  children: ReactNode;
}

const LoadingProvider = ({ children, isLoading }: LoadingProviderProps) => {

  if (isLoading) {
    return (
      <div className={'relative flex h-full'}>
        <LoadingSpinner className={'absolute left-[50%] top-[40%] h-8 w-8'} />
      </div>
    );
  }

  return (
    <>{children}</>
  );

};

export default LoadingProvider;