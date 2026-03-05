import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  DocumentTextIcon,
  MicrophoneIcon,
  FolderIcon,
  BookOpenIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'New Petition', href: '/petition/new', icon: DocumentTextIcon },
  { name: 'Voice Triage', href: '/voice-triage', icon: MicrophoneIcon },
  { name: 'Case Memory', href: '/cases', icon: FolderIcon },
  { name: 'Legal Library', href: '/library', icon: BookOpenIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
];

export default function Sidebar({ isOpen, onClose }) {
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 z-50 h-full w-72 bg-nyaya-blue text-white
          transform transition-transform duration-300 ease-in-out
          lg:translate-x-0
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        `}
      >
        {/* Logo */}
        <div className="flex items-center justify-between h-16 px-6 border-b border-nyaya-blue-light">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-justice-gold rounded-lg flex items-center justify-center">
              <span className="text-nyaya-blue font-bold text-xl">न्या</span>
            </div>
            <div>
              <h1 className="text-lg font-bold">Nyaya-Dwarpal</h1>
              <p className="text-xs text-gray-300">Justice Guardian</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="mt-6 px-3">
          <ul className="space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`
                      flex items-center space-x-3 px-4 py-3 rounded-lg
                      transition-all duration-200 focus-ring
                      ${
                        isActive
                          ? 'bg-nyaya-blue-light text-white shadow-lg'
                          : 'text-gray-300 hover:bg-nyaya-blue-light/50 hover:text-white'
                      }
                    `}
                  >
                    <item.icon className="w-6 h-6" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-nyaya-blue-light">
          <div className="text-xs text-gray-400">
            <p>AI for Bharat Competition</p>
            <p className="mt-1">Powered by AWS Bedrock</p>
          </div>
        </div>
      </aside>
    </>
  );
}
