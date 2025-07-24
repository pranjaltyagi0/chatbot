import { Link } from 'react-router-dom';

const NotFound = () => {
    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center">
            <h1 className="text-4xl font-bold">404</h1>
            <p className="mb-4">Page Not Found</p>
            <Link to="/login" className="text-blue-400 hover:underline">
                Go to Login
            </Link>
        </div>
    );
};

export default NotFound;