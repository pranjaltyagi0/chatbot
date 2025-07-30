import { redirect } from "react-router-dom";

export function ProtectedRoutes() {
    const token = localStorage.getItem("Bearer Token");

    if (!token) {
        // If the token is not present, redirect the user to the login page
        return redirect("/login");
    }

    // If the token is present, allow access to the route
    return null; // No need to return any data
}
export default ProtectedRoutes