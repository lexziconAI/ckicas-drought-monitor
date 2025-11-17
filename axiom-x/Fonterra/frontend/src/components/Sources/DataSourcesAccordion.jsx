import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Clock, Database, ExternalLink } from 'lucide-react';

const DataSourcesAccordion = ({ sources = [] }) => {
  const [expandedItems, setExpandedItems] = useState(new Set());

  const toggleItem = (index) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedItems(newExpanded);
  };

  const getFreshnessColor = (hours) => {
    if (hours <= 6) return 'text-green-600';
    if (hours <= 24) return 'text-yellow-600';
    if (hours <= 72) return 'text-orange-600';
    return 'text-red-600';
  };

  const getFreshnessLabel = (hours) => {
    if (hours <= 1) return 'Just now';
    if (hours <= 24) return `${hours}h ago`;
    if (hours <= 168) return `${Math.floor(hours / 24)}d ago`;
    return `${Math.floor(hours / 168)}w ago`;
  };

  const formatTimestamp = (timestamp) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch {
      return timestamp;
    }
  };

  if (!sources || sources.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <Database className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p>No data sources available</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-semibold text-gray-700">Data Sources (Asteya)</h4>
        <span className="text-xs text-gray-500">{sources.length} sources</span>
      </div>

      {sources.map((source, index) => {
        const isExpanded = expandedItems.has(index);
        const freshnessHours = source.freshness_hours || 0;

        return (
          <div key={index} className="border border-gray-200 rounded-lg overflow-hidden">
            {/* Header */}
            <button
              onClick={() => toggleItem(index)}
              className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <Database className="w-4 h-4 text-gray-600" />
                <div className="text-left">
                  <div className="font-medium text-sm text-gray-900">
                    {source.provider || 'Unknown Provider'}
                  </div>
                  <div className="text-xs text-gray-600">
                    {source.dataset || 'Unknown Dataset'}
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <div className={`text-xs ${getFreshnessColor(freshnessHours)}`}>
                  {getFreshnessLabel(freshnessHours)}
                </div>
                {isExpanded ? (
                  <ChevronDown className="w-4 h-4 text-gray-500" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-gray-500" />
                )}
              </div>
            </button>

            {/* Expanded Content */}
            {isExpanded && (
              <div className="px-3 pb-3 bg-white">
                <div className="border-t border-gray-100 pt-3 mt-3 space-y-2">
                  {/* Timestamp */}
                  <div className="flex items-center space-x-2">
                    <Clock className="w-3 h-3 text-gray-500" />
                    <span className="text-xs text-gray-600">
                      Last updated: {formatTimestamp(source.timestamp)}
                    </span>
                  </div>

                  {/* Parameters */}
                  {source.parameters && source.parameters.length > 0 && (
                    <div>
                      <div className="text-xs font-medium text-gray-700 mb-1">Parameters:</div>
                      <div className="flex flex-wrap gap-1">
                        {source.parameters.map((param, paramIndex) => (
                          <span
                            key={paramIndex}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                          >
                            {param}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Additional metadata */}
                  {source.note && (
                    <div className="text-xs text-gray-600 bg-yellow-50 p-2 rounded">
                      <strong>Note:</strong> {source.note}
                    </div>
                  )}

                  {/* External link if available */}
                  {source.url && (
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-xs text-blue-600 hover:text-blue-800"
                    >
                      View source <ExternalLink className="w-3 h-3 ml-1" />
                    </a>
                  )}
                </div>
              </div>
            )}
          </div>
        );
      })}

      {/* Constitutional Compliance Note */}
      <div className="mt-4 p-3 bg-green-50 rounded-lg">
        <p className="text-xs text-green-800">
          <strong>Asteya Principle:</strong> All data sources are properly cited with timestamps and freshness indicators.
          No hidden or unattributed data is used in calculations.
        </p>
      </div>
    </div>
  );
};

export default DataSourcesAccordion;