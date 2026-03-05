import React, { useState } from 'react';
import {
  ChevronDownIcon,
  ChevronUpIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
} from '@heroicons/react/24/outline';
import EmotionIndicator from '../case/EmotionIndicator';
import Badge from '../common/Badge';

export default function TriageResultsCard({ results }) {
  const [showFacts, setShowFacts] = useState(false);

  const { emotion, classification, extractedFacts, transcription } = results;

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden animate-slide-up">
      {/* Header */}
      <div className="bg-gradient-to-r from-nyaya-blue to-nyaya-blue-light p-6">
        <h3 className="text-xl font-bold text-white">Triage Results</h3>
        <p className="text-sm text-gray-200 mt-1">AI-powered legal analysis</p>
      </div>

      {/* Content */}
      <div className="p-6 space-y-6">
        {/* Emotion & Urgency */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-gray-600 mb-2 block">
              Emotional State
            </label>
            <EmotionIndicator emotion={emotion.primary} confidence={emotion.confidence} />
          </div>
          <div>
            <label className="text-sm font-medium text-gray-600 mb-2 block">
              Urgency Level
            </label>
            <Badge
              variant={
                emotion.urgency === 'high'
                  ? 'error'
                  : emotion.urgency === 'medium'
                  ? 'warning'
                  : 'success'
              }
              size="lg"
            >
              {emotion.urgency.toUpperCase()}
            </Badge>
          </div>
        </div>

        {/* Legal Category */}
        <div>
          <label className="text-sm font-medium text-gray-600 mb-2 block">
            Legal Category
          </label>
          <div className="flex items-center space-x-2">
            <Badge variant="primary" size="lg">
              {classification.category}
            </Badge>
            <span className="text-sm text-gray-500">
              {(classification.confidence * 100).toFixed(0)}% confidence
            </span>
          </div>
        </div>

        {/* Relevant Sections */}
        {classification.relevantSections && classification.relevantSections.length > 0 && (
          <div>
            <label className="text-sm font-medium text-gray-600 mb-3 block">
              Relevant Legal Sections
            </label>
            <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
              {classification.relevantSections.map((section, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <InformationCircleIcon className="w-5 h-5 text-nyaya-blue flex-shrink-0 mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      {section.section}
                    </p>
                    {section.description && (
                      <p className="text-xs text-gray-600 mt-1">
                        {section.description}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Extracted Facts (Collapsible) */}
        {extractedFacts && Object.keys(extractedFacts).length > 0 && (
          <div>
            <button
              onClick={() => setShowFacts(!showFacts)}
              className="flex items-center justify-between w-full text-left focus-ring rounded-lg p-3 hover:bg-gray-50"
            >
              <span className="text-sm font-medium text-gray-900">
                Extracted Facts
              </span>
              {showFacts ? (
                <ChevronUpIcon className="w-5 h-5 text-gray-500" />
              ) : (
                <ChevronDownIcon className="w-5 h-5 text-gray-500" />
              )}
            </button>

            {showFacts && (
              <div className="mt-3 space-y-2 pl-3 border-l-2 border-justice-gold">
                {Object.entries(extractedFacts).map(([key, value]) => (
                  <div key={key}>
                    <span className="text-xs font-semibold text-gray-600 uppercase">
                      {key}:
                    </span>
                    <p className="text-sm text-gray-900 mt-1">{value}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Transcription */}
        <div>
          <label className="text-sm font-medium text-gray-600 mb-2 block">
            Your Statement
          </label>
          <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-900 italic">"{transcription}"</p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-200">
          <button className="flex-1 px-6 py-3 bg-nyaya-blue text-white rounded-lg font-semibold hover:bg-nyaya-blue-light transition-colors focus-ring">
            Generate Petition
          </button>
          <button className="flex-1 px-6 py-3 border-2 border-nyaya-blue text-nyaya-blue rounded-lg font-semibold hover:bg-nyaya-blue hover:text-white transition-colors focus-ring">
            Save to Cases
          </button>
        </div>
      </div>
    </div>
  );
}
