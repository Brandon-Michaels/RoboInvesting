
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './Pages/homepage';
import Chatbot from './Pages/chatbot';
// import Account from './pages/Account';
import Login from './Pages/login';

const App = () => (
  <Router>
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-blue-500 p-4">
        <ul className="flex space-x-4">
          <li>
            <Link to="/" className="text-white">Home</Link>
          </li>
          <li>
            <Link to="/chatbot" className="text-white">Chatbot</Link>
          </li>
          <li>
            <Link to="/account" className="text-white">Account</Link>
          </li>
          <li>
            <Link to="/login" className="text-white">Login</Link>
          </li>
        </ul>
      </nav>

      {/* Main Content */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  </Router>
);

export default App;
