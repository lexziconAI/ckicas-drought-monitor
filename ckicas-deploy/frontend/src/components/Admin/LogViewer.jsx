import React, { useState } from 'react';
import { FileText, AlertCircle, Info, XCircle, Clock, Filter } from 'lucide-react';

function LogViewer({ logs }) {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const getLogIcon = (level) => {
    switch (level.toLowerCase()) {
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />;
      case 'warning':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      default:
        return <Info className="h-4 w-4 text-blue-500" />;
    }
  };

  const getLogColor = (level) => {
    switch (level.toLowerCase()) {
      case 'error':
        return 'border-red-200 bg-red-50';
      case 'warning':
        return 'border-yellow-200 bg-yellow-50';
      default:
        return 'border-gray-200 bg-gray-50';
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const filteredLogs = logs.filter(log => {
    const matchesFilter = filter === 'all' || log.level.toLowerCase() === filter;
    const matchesSearch = searchTerm === '' ||
      log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.source.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const logStats = {
    total: logs.length,
    errors: logs.filter(log => log.level === 'ERROR').length,
    warnings: logs.filter(log => log.level === 'WARNING').length,
    info: logs.filter(log => log.level === 'INFO').length
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <FileText className="h-5 w-5 text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">System Logs</h2>
        </div>
        <div className="flex items-center space-x-4 text-sm text-gray-600">
          <span>Total: {logStats.total}</span>
          <span className="text-red-600">Errors: {logStats.errors}</span>
          <span className="text-yellow-600">Warnings: {logStats.warnings}</span>
          <span className="text-blue-600">Info: {logStats.info}</span>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="flex-1">
          <div className="relative">
            <Filter className="h-4 w-4 absolute left-3 top-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search logs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <div className="flex space-x-2">
          {['all', 'error', 'warning', 'info'].map((level) => (
            <button
              key={level}
              onClick={() => setFilter(level)}
              className={`px-3 py-2 text-sm font-medium rounded-md ${
                filter === level
                  ? 'bg-blue-100 text-blue-800 border-blue-300'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              } border`}
            >
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Log Entries */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {filteredLogs.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No logs found matching your criteria</p>
          </div>
        ) : (
          filteredLogs.map((log, index) => (
            <div
              key={index}
              className={`p-3 rounded-lg border ${getLogColor(log.level)}`}
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 mt-0.5">
                  {getLogIcon(log.level)}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-900">
                      {log.message}
                    </p>
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <Clock className="h-3 w-3" />
                      <span>{formatTimestamp(log.timestamp)}</span>
                    </div>
                  </div>

                  <div className="mt-1 flex items-center space-x-4 text-xs text-gray-600">
                    <span className="font-medium">{log.source}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      log.level === 'ERROR' ? 'bg-red-100 text-red-800' :
                      log.level === 'WARNING' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {log.level}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Log Summary */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-sm font-medium text-gray-900 mb-2">Log Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Total Entries:</span>
            <span className="ml-2 font-medium">{logStats.total}</span>
          </div>
          <div>
            <span className="text-gray-600">Errors:</span>
            <span className="ml-2 font-medium text-red-600">{logStats.errors}</span>
          </div>
          <div>
            <span className="text-gray-600">Warnings:</span>
            <span className="ml-2 font-medium text-yellow-600">{logStats.warnings}</span>
          </div>
          <div>
            <span className="text-gray-600">Info:</span>
            <span className="ml-2 font-medium text-blue-600">{logStats.info}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LogViewer;