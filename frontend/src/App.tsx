import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Chat from './pages/Chat';
import NotFound from './pages/NotFound';
import { useSelector } from 'react-redux';
import type { RootState } from './store';

const App = () => {
  const isAuthenticated = useSelector((state: RootState) => !!state.auth.token);

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route
        path="/chat"
        element={isAuthenticated ? <Chat /> : <Login />}
      />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;
