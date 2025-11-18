'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import the map component to avoid SSR issues
const DroughtMap = dynamic(() => import('../components/Map/DroughtMap'), {
  ssr: false,
  loading: () => <div className="h-[600px] bg-gray-100 rounded-lg flex items-center justify-center">Loading map...</div>
});

interface ApiStatus {
  niwa: boolean;
  openweather: boolean;
  anthropic: boolean;
}

interface DroughtRisk {
  risk_score: number;      // Backend sends this (0-100 scale)
  risk_level?: string;     // Optional fallback
  confidence: number;
  factors: string[];
}

interface DataSource {
  provider: string;        // Backend sends this
  dataset: string;
  timestamp: string;
  freshness_hours: number;
  parameters: string[];
  note: string;
}

export default function CKICASDroughtMonitor() {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null);
  const [droughtRisk, setDroughtRisk] = useState<DroughtRisk | null>(null);
  const [dataSources, setDataSources] = useState<DataSource[]>([]);
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ckicas-drought-monitor-1.onrender.com';

  useEffect(() => {
    fetchApiStatus();
    fetchDataSources();
    fetchDroughtRisk();
  }, []);

  const fetchApiStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/apis`);
      const data = await response.json();
      setApiStatus(data);
    } catch (error) {
      console.error('Failed to fetch API status:', error);
    }
  };

  const fetchDataSources = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/public/data-sources`);
      const data = await response.json();
      setDataSources(data.sources || []);
    } catch (error) {
      console.error('Failed to fetch data sources:', error);
    }
  };

  const fetchDroughtRisk = async () => {
    try {
      // Using default coordinates for demonstration (Auckland, NZ)
      const response = await fetch(`${API_BASE_URL}/api/public/drought-risk?lat=-36.8485&lon=174.7633`);
      const data = await response.json();
      setDroughtRisk(data);
    } catch (error) {
      console.error('Failed to fetch drought risk:', error);
    }
  };

  const sendChatMessage = async () => {
    if (!chatMessage.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: chatMessage,
          context: { type: 'drought_monitoring' }
        }),
      });
      const data = await response.json();
      setChatResponse(data.response || 'No response received');
    } catch (error) {
      setChatResponse('Error: Could not connect to AI assistant');
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskLevel = (score: number): string => {
    if (score >= 80) return 'extreme';
    if (score >= 60) return 'severe';
    if (score >= 40) return 'moderate';
    if (score >= 20) return 'mild';
    return 'normal';
  };

  const getRiskColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'extreme': return 'text-red-600 bg-red-100';
      case 'severe': return 'text-orange-600 bg-orange-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'mild': return 'text-blue-600 bg-blue-100';
      case 'normal': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">CKICAS Drought Monitor</h1>
              <p className="text-gray-600 mt-1">Advanced AI-Powered Drought Monitoring System</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${apiStatus?.anthropic ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="text-sm text-gray-600">AI Assistant</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Status Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* API Status Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">API Status</h3>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">NIWA Weather</span>
                <div className={`w-2 h-2 rounded-full ${apiStatus?.niwa ? 'bg-green-500' : 'bg-red-500'}`}></div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">OpenWeather</span>
                <div className={`w-2 h-2 rounded-full ${apiStatus?.openweather ? 'bg-green-500' : 'bg-red-500'}`}></div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Claude AI</span>
                <div className={`w-2 h-2 rounded-full ${apiStatus?.anthropic ? 'bg-green-500' : 'bg-red-500'}`}></div>
              </div>
            </div>
          </div>

          {/* Current Risk Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Risk Assessment</h3>
            {droughtRisk ? (
              <div>
                <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(getRiskLevel(droughtRisk.risk_score))}`}>
                  {getRiskLevel(droughtRisk.risk_score).toUpperCase()} RISK
                </div>
                <p className="text-sm text-gray-600 mt-2">
                  Confidence: {Math.round(droughtRisk.confidence * 100)}%
                </p>
                <div className="mt-3">
                  <p className="text-xs text-gray-500 mb-1">Key Factors:</p>
                  <ul className="text-xs text-gray-600 space-y-1">
                    {(droughtRisk.factors || []).slice(0, 3).map((factor, index) => (
                      <li key={index}>• {factor || 'Unknown factor'}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <p className="text-gray-500">Loading risk assessment...</p>
            )}
          </div>

          {/* Data Sources Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Active Data Sources</h3>
            <div className="space-y-2">
              {dataSources.slice(0, 3).map((source, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">{source.provider || 'Unknown Source'}</span>
                  <div className={`w-2 h-2 rounded-full ${source.freshness_hours <= 2 ? 'bg-green-500' : source.freshness_hours <= 8 ? 'bg-yellow-500' : 'bg-red-500'}`}></div>
                </div>
              ))}
            </div>
            {dataSources.length > 3 && (
              <p className="text-xs text-gray-500 mt-2">+{dataSources.length - 3} more sources</p>
            )}
          </div>
        </div>

        {/* Drought Risk Map */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Drought Risk Map - New Zealand</h3>
          <p className="text-gray-600 mb-4">
            Interactive map showing drought risk levels across New Zealand regions. Click on regions or enter coordinates to get detailed risk assessments.
          </p>
          <DroughtMap key="single-drought-map" apiBaseUrl={API_BASE_URL} />
        </div>

        {/* AI Assistant Chat */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Drought Analysis Assistant</h3>
          <div className="space-y-4">
            <div className="flex space-x-2">
              <input
                type="text"
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                placeholder="Ask about drought conditions, weather patterns, or risk analysis..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
              />
              <button
                onClick={sendChatMessage}
                disabled={isLoading || !chatMessage.trim()}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Analyzing...' : 'Ask AI'}
              </button>
            </div>
            {chatResponse && (
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-700">{chatResponse}</p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center text-gray-500 text-sm">
          <p>CKICAS Drought Monitor - Powered by Axiom-X AI & Real-time Weather Data</p>
          <p className="mt-1">Backend: {API_BASE_URL}</p>
        </footer>
      </main>
    </div>
  );
}
