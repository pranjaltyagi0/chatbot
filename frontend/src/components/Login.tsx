// import axios from "axios";
// import { useState } from "react";
// import { useNavigate } from "react-router";
// function Login() {
//     const [email, setEmail] = useState("")
//     const [password, setPassword] = useState("")
//     const navigate = useNavigate()

//     async function onLogin() {
//         try {
//             const url = "http://127.0.0.1:3000/auth/login"
//             const payload = {
//                 "user_email_id": email,
//                 "password": password
//             }
//             const response = await axios.post(url, payload, {
//                 headers: {
//                     Accept: "application/json",
//                     "Content-Type": "application/json;charset=UTF-8",
//                 }
//             })
//             console.log(response)
//             if (response.data.successful && response.data.access_token != null) {
//                 localStorage.setItem("user_email_id", response.data.user_email_id)
//                 localStorage.setItem("Bearer Token", response.data.access_token)
//                 navigate("/chat")
//             }

//         }
//         catch {
//             console.log("Logging error ")
//         }
//         finally {

//         }
//     }

//     return (
//         <div className=" flex justify-center items-center border-2 h-screen w-screen">
//             <form className="flex flex-col border-2 h-3/6 justify-center items-center w-96 gap-2" onSubmit={(e) => {
//                 e.preventDefault()
//                 onLogin()
//             }}>
//                 <input className="border-2 rounded-4xl w-48" type="email" required placeholder="Email" onChange={(e) => setEmail(e.target.value)}></input>
//                 <input className="border-2 rounded-4xl w-48 " type="password" required placeholder="Password" onChange={(e) => setPassword(e.target.value)}></input>
//                 <button className="border-2 rounded-4xl w-36" type="submit">Log In</button>
//             </form>
//         </div>
//     )
// }
// export default Login
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate(); 
    useEffect(() => {
        const token = localStorage.getItem("Bearer Token");
        if (token) {
            navigate("/chat");
        }
    }, []);
    async function onLogin() {
        try {
            setLoading(true);
            setErrorMsg("");

            const url = "http://127.0.0.1:3000/auth/login";
            const payload = {
                "user_email_id": email,
                "password": password,
            };

            const response = await axios.post(url, payload, {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=UTF-8",
                },
            });
            console.log(response)
            const data = response.data;
            if (data.successful && data.access_token) {
                localStorage.setItem("user_email_id", data.user_email_id);
                localStorage.setItem("Bearer Token", data.access_token);
                navigate("/chat");
            } else {
                setErrorMsg("Invalid email or password.");
            }
        } catch (error) {
            console.error("Login error", error);
            setErrorMsg("Invalid email or password.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="flex justify-center items-center h-screen bg-gray-900">
            <form
                className="flex flex-col bg-white rounded-xl shadow-md px-10 py-8 w-96 space-y-4"
                onSubmit={(e) => {
                    e.preventDefault();
                    onLogin();
                }}
            >
                <h2 className="text-2xl font-bold text-center text-gray-800">Login</h2>

                <input
                    type="email"
                    required
                    placeholder="Email"
                    className="p-2 border border-gray-300 rounded-b-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => setEmail(e.target.value)}
                />

                <input
                    type="password"
                    required
                    placeholder="Password"
                    className="p-2 border border-gray-300 rounded-b-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => setPassword(e.target.value)}
                />

                {errorMsg && (
                    <p className="text-sm text-red-600 text-center">{errorMsg}</p>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="bg-blue-600 text-white py-2 rounded-b-lg hover:bg-blue-700 transition duration-200 disabled:opacity-50"
                >
                    {loading ? "Logging in..." : "Log In"}
                </button>

                <button
                    type="button"
                    onClick={() => navigate("/signup")}
                    className="bg-gray-100 text-blue-600 border border-blue-500 py-2 rounded-b-lg hover:bg-blue-50 transition duration-200"
                >
                    Sign Up
                </button>
            </form>
        </div>
    );
}

export default Login;
