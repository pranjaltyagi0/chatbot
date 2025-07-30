import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router";
import './index.css'
import App from './App.tsx'
import Signup from './components/Signup.tsx';
import Login from './components/Login.tsx';
import Chat from './components/chat.tsx';
import ProtectedRoutes from './components/ProtectedRoutes.tsx';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/signup",
    element: <Signup />
  },
  {
    path: "/chat",
    element: <Chat />,
    loader: ProtectedRoutes
  }

]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />,
  </StrictMode>,
)
