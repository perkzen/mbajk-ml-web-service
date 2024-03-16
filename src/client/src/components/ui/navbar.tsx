import Image from 'next/image';
import Logo from '@/assets/logo.png';
import Link from 'next/link';
import { Github } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className={'flex flex-row w-full py-4 px-8 shadow-lg'}>
      <div className={'flex flex-row items-center gap-2 rounded-full bg-primary w-fit py-1 px-3'}>
        <Image src={Logo} alt={'MBajk AI'} width={24} height={24} className={'rounded-full'} />
        <div className={'text-white text-lg font-semibold'}>mbajk ejaj</div>
      </div>
      <div className={'ml-auto bg-black h-fit rounded-full p-2'}>
        <Link target="_blank" href={'https://github.com/perkzen/mbajk-ml-web-service'}>
          <Github size={24} stroke={'#fff'} />
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;