import React from 'react';
import { Shield, Droplets, Users, Heart, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';

const Header = () => {
  const isAdmin = localStorage.getItem('admin_token');

  return (
    <header className="bg-white shadow-lg border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-4">
            <Link to="/" className="flex items-center space-x-2">
              <Droplets className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">NZ Drought Monitor</h1>
                <p className="text-sm text-gray-600">Constitutional AI for Farmers</p>
              </div>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">
              Dashboard
            </Link>
            <a href="#regions" className="text-gray-700 hover:text-blue-600 font-medium">
              Regions
            </a>
            <a href="#forecasts" className="text-gray-700 hover:text-blue-600 font-medium">
              Forecasts
            </a>
            <a href="#about" className="text-gray-700 hover:text-blue-600 font-medium">
              About
            </a>
            {isAdmin && (
              <Link to="/admin" className="flex items-center space-x-1 text-orange-600 hover:text-orange-700 font-medium">
                <Settings className="w-4 h-4" />
                <span>Admin</span>
              </Link>
            )}
          </nav>

          {/* Constitutional Principles */}
          <div className="hidden lg:flex items-center space-x-4">
            <div className="flex items-center space-x-1 text-xs">
              <Shield className="w-3 h-3 text-green-600" />
              <span className="text-gray-600">Ahimsa</span>
            </div>
            <div className="flex items-center space-x-1 text-xs">
              <Users className="w-3 h-3 text-blue-600" />
              <span className="text-gray-600">Satya</span>
            </div>
            <div className="flex items-center space-x-1 text-xs">
              <Heart className="w-3 h-3 text-purple-600" />
              <span className="text-gray-600">Asteya</span>
            </div>
          </div>

          {/* Status Indicator */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600 hidden sm:inline">Live Data</span>
            </div>
          </div>
        </div>

        {/* Constitutional Principles Explanation (Mobile) */}
        <div className="lg:hidden mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="flex flex-col items-center">
              <Shield className="w-5 h-5 text-green-600 mb-1" />
              <span className="text-xs font-medium text-gray-900">Ahimsa</span>
              <span className="text-xs text-gray-600">No False Alarms</span>
            </div>
            <div className="flex flex-col items-center">
              <Users className="w-5 h-5 text-blue-600 mb-1" />
              <span className="text-xs font-medium text-gray-900">Satya</span>
              <span className="text-xs text-gray-600">Truthful Confidence</span>
            </div>
            <div className="flex flex-col items-center">
              <Heart className="w-5 h-5 text-purple-600 mb-1" />
              <span className="text-xs font-medium text-gray-900">Asteya</span>
              <span className="text-xs text-gray-600">Proper Attribution</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;