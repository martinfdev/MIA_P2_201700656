import { useNavigate } from "react-router-dom"
// import {AiOutlineEye} from 'react-icons/ai'


function Login() {
    const navigate = useNavigate();
    
    const handleReports = () => {
        navigate('/reports')
    }

    return (
        <div className="flex h-screen justify-center items-center">
            <div className="flex flex-col items-center justify-center gap-14 rounded-md bg-slate-600 w-auto h-auto p-10">
                <h1 className="text-3xl text-slate-200 font-semibold">Login</h1>
                <div className="flex flex-col gap-4 w-full">
                    <input
                        type="text"
                        placeholder="ID Particion"
                        className="p-2 rounded-md bg-slate-200 w-full hover:bg-blue-200 border-2 hover:border-primary hover:shadow-md" />
                    <input
                        type="text"
                        placeholder="Username"
                        className="p-2 rounded-md bg-slate-200 w-full hover:bg-blue-200 border-2 hover:border-primary hover:shadow-md" />
                    <input
                        type="password"
                        placeholder="Password"
                        className="p-2 rounded-md bg-slate-200 w-full hover:bg-blue-200 border-2 hover:border-primary hover:shadow-md" />
                    {/* <AiOutlineEye className="text-2xl text-slate-200" /> */}
                </div>
                <button className="p-3 rounded-md text-slate-900 font-bold bg-slate-200 border-4 hover:border-primary  w-full"
                onClick={handleReports}
                >Ingresar</button>
            </div>
        </div>
    )
}

export default Login;