
import Login from '../pages/Login';

function Header() {
  return (
    <div className="flex h-24 bg-yellow-50 px-4 items-center rounded-md">
      <h1 className="font-bold">MIA Proyecto 2</h1>
      <button className="ml-auto w-1/6 h-1/2 bg-gradient-to-r from-gray-500 to-blue-950  text-white font-bold border-2 hover:border-primary rounded-md" >Login</button>
    </div>
  );
}

export default Header;