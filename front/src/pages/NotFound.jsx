import { useNavigate } from 'react-router-dom';


function NotFound() {
  const navigate = useNavigate();
  const handleHome = () => {
    navigate('/home');
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-6">
      <h1 className="text-white text-8xl">404</h1>
      <p className="text-white text-4xl">Page not found</p>
      <button
        className="p-3 rounded-md text-slate-900 font-bold bg-slate-200 border-4 hover:border-primary"
        onClick={handleHome}
      >Go Home</button>
    </div>
  );
}

export default NotFound;