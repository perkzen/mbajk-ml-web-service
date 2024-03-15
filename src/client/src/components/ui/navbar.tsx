import Image from 'next/image';
import Logo from '@/assets/logo.png';

const Navbar = () => {
  return (
    <nav className={'w-full py-4 px-8'}>
      <div className={'flex flex-row items-center gap-2 rounded-full bg-primary w-fit py-1 px-3'}>
        <Image src={Logo} alt={'MBajk AI'} width={24} height={24} className={"rounded-full"} />
        <div className={'text-white text-lg font-semibold'}>mbajk ejaj</div>
      </div>
    </nav>
  );
};

export default Navbar;