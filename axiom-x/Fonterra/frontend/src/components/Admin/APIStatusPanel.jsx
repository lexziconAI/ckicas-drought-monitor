import React from 'react';
import { Wifi, WifiOff, Clock, Zap } from 'lucide-react';

function APIStatusPanel({ apiStatus }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'operational':
        return 'text-green-600 bg-green-50';
      case 'degraded':
        return 'text-yellow-600 bg-yellow-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'operational':
        return <Wifi className="h-4 w-4" />;
      case 'degraded':
        return <Wifi className="h-4 w-4" />;
      case 'failed':
        return <WifiOff className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const formatLastCheck = (timestamp) => {
    if (!timestamp) return 'Never';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMinutes = Math.floor((now - date) / (1000 * 60));

    if (diffMinutes < 1) return 'Just now';
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    const diffHours = Math.floor(diffMinutes / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">API Availability Status</h2>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <Zap className="h-4 w-4" />
          <span>Real-time monitoring</span>
        </div>
      </div>

      <div className="space-y-4">
        {Object.entries(apiStatus).map(([apiName, status]) => (
          <div key={apiName} className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-full ${getStatusColor(status.status)}`}>
                {getStatusIcon(status.status)}
              </div>
              <div>
                <p className="font-medium text-gray-900 capitalize">
                  {apiName.replace('_', ' ')}
                </p>
                <p className="text-sm text-gray-600">
                  Last checked: {formatLastCheck(status.last_check)}
                </p>
                {status.error && (
                  <p className="text-xs text-red-600 mt-1">{status.error}</p>
                )}
              </div>
            </div>

            <div className="text-right">
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(status.status)}`}>
                {status.status}
              </span>
              {status.response_time && (
                <p className="text-xs text-gray-500 mt-1">
                  {status.response_time}s response
                </p>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <div className="flex items-center space-x-2">
          <Clock className="h-4 w-4 text-blue-600" />
          <span className="text-sm text-blue-800">
            Status updates automatically every 30 seconds via WebSocket
          </span>
        </div>
      </div>
    </div>
  );
}

export default APIStatusPanel;