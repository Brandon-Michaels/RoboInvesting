import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => (
  <nav className="bg-gray-800 p-4 text-white">
    <Link to="/" className="mx-4 hover:underline">Home</Link>
    <Link to="/chatbot" className="mx-4 hover:underline">Chatbot</Link>
    <Link to="/account" className="mx-4 hover:underline">Account</Link>
    <Link to="/login" className="mx-4 hover:underline">Login</Link>
  </nav>
);

export default Navbar;