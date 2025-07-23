import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { login } from '../store/slices/authSlice';

const Signup = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [user_email_id, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:3000/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, user_email_id, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Signup failed');
            }

            dispatch(login({ token: data.token, user: user_email_id }));
            navigate('/chat');
        } catch (err: any) {
            setError(err.message);
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center p-4">
            <h2 className="text-2xl mb-4 font-bold">Sign Up</h2>

            {error && <p className="mb-4 text-red-400 text-sm">{error}</p>}

            <form onSubmit={handleSignup} className="space-y-4 w-full max-w-sm">
                <div>
                    <input
                        type="text"
                        placeholder="Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        className="w-full p-2 bg-gray-800 border border-gray-600 rounded"
                    />
                </div>
                <input
                    type="email"
                    placeholder="Email"
                    value={user_email_id}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full p-2 bg-gray-800 border border-gray-600 rounded"
                />
                <div className="relative">
                    <input
                        type={showPassword ? 'text' : 'password'}
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full p-2 bg-gray-800 border border-gray-600 rounded"
                    />
                    <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-2 top-1/2 -translate-y-1/2 text-sm text-gray-400"
                    >
                        {showPassword ? 'Hide' : 'Show'}
                    </button>
                </div>
                <button type="submit" className="w-full bg-green-600 hover:bg-green-700 py-2 rounded">
                    Sign Up
                </button>
            </form>
        </div>
    );
};

export default Signup;
