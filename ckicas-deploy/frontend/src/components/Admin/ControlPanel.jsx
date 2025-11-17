import React, { useState } from 'react';
import axios from 'axios';
import {
  RefreshCw,
  Trash2,
  TestTube,
  Download,
  Play,
  CheckCircle,
  XCircle,
  Loader
} from 'lucide-react';

function ControlPanel({ onRefresh }) {
  const [loading, setLoading] = useState({});
  const [results, setResults] = useState({});

  const handleAction = async (action, endpoint) => {
    setLoading(prev => ({ ...prev, [action]: true }));
    setResults(prev => ({ ...prev, [action]: null }));

    try {
      const response = await axios.post(`/api/admin/${endpoint}`);
      setResults(prev => ({ ...prev, [action]: { success: true, data: response.data } }));
      if (action === 'refresh') {
        onRefresh(); // Refresh dashboard data
      }
    } catch (error) {
      setResults(prev => ({
        ...prev,
        [action]: {
          success: false,
          error: error.response?.data?.detail || error.message
        }
      }));
    } finally {
      setLoading(prev => ({ ...prev, [action]: false }));
    }
  };

  const handleExport = async (format) => {
    const action = `export_${format}`;
    setLoading(prev => ({ ...prev, [action]: true }));

    try {
      const response = await axios.get(`/api/admin/export?format=${format}`);

      // Create download link
      const blob = new Blob([JSON.stringify(response.data, null, 2)], {
        type: format === 'json' ? 'application/json' : 'text/csv'
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ckicas_export_${new Date().toISOString().split('T')[0]}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setResults(prev => ({ ...prev, [action]: { success: true, message: 'Export completed' } }));
    } catch (error) {
      setResults(prev => ({
        ...prev,
        [action]: {
          success: false,
          error: error.response?.data?.detail || error.message
        }
      }));
    } finally {
      setLoading(prev => ({ ...prev, [action]: false }));
    }
  };

  const controls = [
    {
      id: 'refresh',
      title: 'Force Data Refresh',
      description: 'Manually trigger data collection from all sources',
      icon: <RefreshCw className="h-5 w-5" />,
      endpoint: 'refresh',
      variant: 'primary'
    },
    {
      id: 'clear_cache',
      title: 'Clear Brahmacharya Cache',
      description: 'Reset intelligent caching system',
      icon: <Trash2 className="h-5 w-5" />,
      endpoint: 'clear-cache',
      variant: 'warning'
    },
    {
      id: 'test_constitutional',
      title: 'Test Constitutional Compliance',
      description: 'Run Yama principles validation tests',
      icon: <TestTube className="h-5 w-5" />,
      endpoint: 'test-constitutional',
      variant: 'secondary'
    }
  ];

  const getButtonClasses = (variant, isLoading) => {
    const baseClasses = "w-full flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

    if (isLoading) {
      return `${baseClasses} bg-gray-100 text-gray-400 cursor-not-allowed`;
    }

    switch (variant) {
      case 'primary':
        return `${baseClasses} bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500`;
      case 'warning':
        return `${baseClasses} bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500`;
      case 'secondary':
        return `${baseClasses} bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500`;
      default:
        return `${baseClasses} bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500`;
    }
  };

  return (
    <div className="space-y-6">
      {/* Manual Controls */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center space-x-2 mb-6">
          <Play className="h-5 w-5 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">Manual Controls</h2>
        </div>

        <div className="space-y-4">
          {controls.map((control) => (
            <div key={control.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <div className="text-gray-600 mt-0.5">
                    {control.icon}
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">{control.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">{control.description}</p>
                  </div>
                </div>
              </div>

              <div className="mt-4">
                <button
                  onClick={() => handleAction(control.id, control.endpoint)}
                  disabled={loading[control.id]}
                  className={getButtonClasses(control.variant, loading[control.id])}
                >
                  {loading[control.id] ? (
                    <>
                      <Loader className="h-4 w-4 animate-spin mr-2" />
                      Processing...
                    </>
                  ) : (
                    <>
                      {control.icon}
                      <span className="ml-2">Execute</span>
                    </>
                  )}
                </button>
              </div>

              {results[control.id] && (
                <div className={`mt-3 p-3 rounded-md ${
                  results[control.id].success
                    ? 'bg-green-50 border border-green-200'
                    : 'bg-red-50 border border-red-200'
                }`}>
                  <div className="flex items-center space-x-2">
                    {results[control.id].success ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <XCircle className="h-4 w-4 text-red-600" />
                    )}
                    <span className={`text-sm font-medium ${
                      results[control.id].success ? 'text-green-800' : 'text-red-800'
                    }`}>
                      {results[control.id].success ? 'Success' : 'Error'}
                    </span>
                  </div>
                  <div className="mt-1 text-sm text-gray-700">
                    {results[control.id].data?.message ||
                     results[control.id].error ||
                     JSON.stringify(results[control.id].data, null, 2)}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Data Export */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center space-x-2 mb-6">
          <Download className="h-5 w-5 text-green-600" />
          <h2 className="text-xl font-semibold text-gray-900">Data Export</h2>
        </div>

        <div className="space-y-4">
          <div className="border border-gray-200 rounded-lg p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Export System Data</h3>
            <p className="text-sm text-gray-600 mb-4">
              Download current system state, metrics, and configuration
            </p>

            <div className="flex space-x-3">
              <button
                onClick={() => handleExport('json')}
                disabled={loading.export_json}
                className="flex-1 flex items-center justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading.export_json ? (
                  <Loader className="h-4 w-4 animate-spin mr-2" />
                ) : (
                  <Download className="h-4 w-4 mr-2" />
                )}
                JSON Export
              </button>

              <button
                onClick={() => handleExport('csv')}
                disabled={loading.export_csv}
                className="flex-1 flex items-center justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading.export_csv ? (
                  <Loader className="h-4 w-4 animate-spin mr-2" />
                ) : (
                  <Download className="h-4 w-4 mr-2" />
                )}
                CSV Export
              </button>
            </div>

            {(results.export_json || results.export_csv) && (
              <div className="mt-3 p-3 rounded-md bg-green-50 border border-green-200">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <span className="text-sm font-medium text-green-800">Export completed</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Brahmacharya Status */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Brahmacharya Status</h2>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Cache Efficiency Target</span>
            <span className="text-sm font-medium text-green-600">&gt;80%</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">API Call Prevention</span>
            <span className="text-sm font-medium text-blue-600">Active</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Resource Waste Prevention</span>
            <span className="text-sm font-medium text-green-600">Enforced</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ControlPanel;