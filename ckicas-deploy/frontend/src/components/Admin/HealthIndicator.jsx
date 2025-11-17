import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Activity } from 'lucide-react';

function HealthIndicator({ title, status, value, icon }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
      case 'operational':
        return 'bg-green-50 border-green-200 text-green-800';
      case 'degraded':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'failed':
      case 'unhealthy':
        return 'bg-red-50 border-red-200 text-red-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
      case 'operational':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'degraded':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />;
      case 'failed':
      case 'unhealthy':
        return <XCircle className="h-5 w-5 text-red-600" />;
      default:
        return <Activity className="h-5 w-5 text-gray-600" />;
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${getStatusColor(status)}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="text-gray-600">
            {icon}
          </div>
          <div>
            <p className="text-sm font-medium text-gray-900">{title}</p>
            <p className="text-lg font-semibold">{value}</p>
          </div>
        </div>
        {getStatusIcon(status)}
      </div>
    </div>
  );
}

export default HealthIndicator;