import React, { useState } from 'react';
import { MicrophoneIcon } from '@heroicons/react/24/solid';
import WaveformVisualizer from './WaveformVisualizer';

export default function MicrophoneButton({ onStartRecording, onStopRecording, isRecording }) {
  const [isHovered, setIsHovered] = useState(false);

  const handleClick = () => {
    if (isRecording) {
      onStopRecording();
    } else {
      onStartRecording();
    }
  };

  if (isRecording) {
    return (
      <div className="flex flex-col items-center space-y-4 animate-slide-up">
        <WaveformVisualizer />
        <button
          onClick={handleClick}
          className="px-8 py-3 bg-red-500 text-white rounded-lg font-semibold hover:bg-red-600 transition-colors focus-ring"
        >
          Stop Recording
        </button>
        <p className="text-sm text-gray-600 animate-pulse">Listening...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center space-y-4">
      <button
        onClick={handleClick}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className={`
          relative w-32 h-32 rounded-full bg-gradient-to-br from-nyaya-blue to-nyaya-blue-light
          flex items-center justify-center
          shadow-2xl shadow-nyaya-blue/30
          transition-all duration-300 focus-ring
          ${isHovered ? 'scale-110' : 'scale-100 animate-pulse-slow'}
        `}
        aria-label="Start voice recording"
      >
        <MicrophoneIcon className="w-12 h-12 text-white" />
        
        {/* Pulse rings */}
        <span className="absolute inset-0 rounded-full bg-nyaya-blue opacity-20 animate-ping" />
        <span className="absolute inset-0 rounded-full bg-nyaya-blue opacity-10 animate-pulse" />
      </button>

      <div className="text-center">
        <p className="text-lg font-semibold text-gray-900">Voice Triage</p>
        <p className="text-sm text-gray-600">Click to start recording</p>
      </div>
    </div>
  );
}
