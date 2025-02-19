// src/pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
  <div className="min-h-screen bg-gray-100 p-6">
      <div className = "flex justify-end">
          <Link to = "/chatbot">
            <button className = "px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600">
                Open Chatbot
            </button>
          </Link>
      </div>

      <h1 className = "text-2xl font-bold mb-4">Financial Overview</h1>
      <div className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className = "bg-white p-6 rounded-2xl shadow-md">
              <h2 className = "text-lg font-semibold">Net Worth</h2>
              <p className = "text-2xl font-bold text-green-500">$150,000</p>
          </div>

          <div className = "bg-white p-6 rounded-2xl shadow-md">
              <h2 className="text-lg font-semibold">Assets</h2>
              <p className="text-2xl font-bold">$200,000</p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-md">
              <h2 className="text-lg font-semibold">Monthly Gain</h2>
              <p className="text-2xl font-bold text-green-500">+3.5%</p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-md">
              <h2 className="text-lg font-semibold">Goals</h2>
              <p className="text-md text-gray-600">Save $10,000 for investment</p>
          </div>
      </div>
      </div>
    );
}
export default Home;
