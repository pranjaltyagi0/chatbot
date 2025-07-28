import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import axios from "axios";

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
    const [isValid, setIsValid] = useState<boolean | null>(null);

    useEffect(() => {
        const token = localStorage.getItem("Bearer Token");

        if (!token) {
            setIsValid(false);
            return;
        }

        axios
            .post(
                "http://localhost:3000/auth/verify-token",
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            )
            .then((res) => {
                if (res.data.valid) {
                    setIsValid(true);
                } else {
                    setIsValid(false);
                }
            })
            .catch((err) => {
                console.error("Token validation error:", err);
                setIsValid(false);
            });
    }, []);

    if (isValid === null) {
        return <div className="text-center text-white mt-10">Checking authentication...</div>;
    }

    if (!isValid) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

export default ProtectedRoute;
