import React from 'react';
import {
  Bars3Icon,
  SunIcon,
  MoonIcon,
  LanguageIcon,
  UserCircleIcon,
} from '@heroicons/react/24/outline';
import LanguageToggle from '../accessibility/LanguageToggle';
import ContrastToggle from '../accessibility/ContrastToggle';

export default function Header({ onMenuClick, title = 'Dashboard' }) {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-gray-200 shadow-sm">
      <div className="flex items-center justify-between h-16 px-4 lg:px-8">
        {/* Left: Menu button (mobile) + Title */}
        <div className="flex items-center space-x-4">
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100 focus-ring"
            aria-label="Open menu"
          >
            <Bars3Icon className="w-6 h-6 text-gray-600" />
          </button>
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center space-x-2">
          {/* Language Toggle */}
          <LanguageToggle />

          {/* Contrast Toggle */}
          <ContrastToggle />

          {/* User Profile */}
          <button
            className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100 focus-ring"
            aria-label="User profile"
          >
            <UserCircleIcon className="w-8 h-8 text-gray-600" />
            <span className="hidden md:block text-sm font-medium text-gray-700">
              User
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}
