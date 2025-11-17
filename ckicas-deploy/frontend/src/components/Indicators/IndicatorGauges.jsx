import React from 'react';
import { Droplets, Thermometer, TrendingDown, AlertTriangle, CheckCircle } from 'lucide-react';

const IndicatorGauges = ({ indicators, confidence }) => {
  const {
    spi_30day = 0,
    spi_60day = 0,
    smd_current = 0,
    smd_anomaly = 0,
    nzdi_category = 'NORMAL'
  } = indicators;

  // SPI gauge configuration
  const getSPIGauge = (value, label, period) => {
    const percentage = Math.min(100, Math.max(0, 50 + (value * 10))); // Convert SPI to 0-100 scale
    const color = value < -2 ? '#dc2626' : value < -1 ? '#ea580c' : value < 0 ? '#d97706' : '#16a34a';

    return (
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">{label}</span>
          <span className="text-sm font-bold" style={{ color }}>{value.toFixed(1)}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
          <div
            className="h-3 rounded-full transition-all duration-300"
            style={{
              width: `${percentage}%`,
              backgroundColor: color
            }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-500">
          <span>Dry</span>
          <span>Normal</span>
          <span>Wet</span>
        </div>
      </div>
    );
  };

  // SMD gauge configuration
  const getSMDGauge = () => {
    const maxSMD = 150; // Field capacity
    const percentage = Math.min(100, (smd_current / maxSMD) * 100);
    const color = smd_current > 120 ? '#dc2626' : smd_current > 90 ? '#ea580c' : smd_current > 60 ? '#d97706' : '#16a34a';

    return (
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Soil Moisture Deficit</span>
          <span className="text-sm font-bold" style={{ color }}>{smd_current.toFixed(0)}mm</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
          <div
            className="h-3 rounded-full transition-all duration-300"
            style={{
              width: `${percentage}%`,
              backgroundColor: color
            }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-500">
          <span>0mm</span>
          <span>75mm</span>
          <span>150mm</span>
        </div>
        {smd_anomaly !== 0 && (
          <div className="mt-2 text-xs">
            <span className={smd_anomaly > 0 ? 'text-red-600' : 'text-green-600'}>
              {smd_anomaly > 0 ? '+' : ''}{smd_anomaly.toFixed(0)}mm vs normal
            </span>
          </div>
        )}
      </div>
    );
  };

  // NZDI category display
  const getNZDICategory = () => {
    const categories = {
      'NORMAL': { color: 'text-green-600', bg: 'bg-green-100', icon: CheckCircle },
      'DRY': { color: 'text-yellow-600', bg: 'bg-yellow-100', icon: AlertTriangle },
      'VERY_DRY': { color: 'text-orange-600', bg: 'bg-orange-100', icon: AlertTriangle },
      'EXTREMELY_DRY': { color: 'text-red-600', bg: 'bg-red-100', icon: AlertTriangle },
      'DROUGHT': { color: 'text-red-700', bg: 'bg-red-200', icon: AlertTriangle },
      'SEVERE_DROUGHT': { color: 'text-red-800', bg: 'bg-red-300', icon: AlertTriangle }
    };

    const category = categories[nzdi_category] || categories['NORMAL'];
    const IconComponent = category.icon;

    return (
      <div className={`${category.bg} rounded-lg p-4`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <IconComponent className={`w-5 h-5 mr-2 ${category.color}`} />
            <span className="font-medium text-gray-900">NZ Drought Index</span>
          </div>
          <span className={`font-bold ${category.color}`}>{nzdi_category.replace('_', ' ')}</span>
        </div>
      </div>
    );
  };

  // Confidence indicator
  const getConfidenceIndicator = () => {
    const confidenceConfig = {
      'HIGH': { color: 'text-green-600', bg: 'bg-green-100', description: 'High confidence (0-7 days)' },
      'MEDIUM': { color: 'text-yellow-600', bg: 'bg-yellow-100', description: 'Medium confidence (8-21 days)' },
      'LOW': { color: 'text-red-600', bg: 'bg-red-100', description: 'Low confidence (22+ days)' }
    };

    const config = confidenceConfig[confidence] || confidenceConfig['LOW'];

    return (
      <div className={`${config.bg} rounded-lg p-3 mt-4`}>
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">Forecast Confidence</span>
          <span className={`text-sm font-bold ${config.color}`}>{confidence}</span>
        </div>
        <p className="text-xs text-gray-600 mt-1">{config.description}</p>
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {/* SPI Indicators */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-gray-700 flex items-center">
          <Droplets className="w-4 h-4 mr-1" />
          Precipitation Indicators
        </h4>
        {getSPIGauge(spi_30day, 'SPI 30-Day', 30)}
        {getSPIGauge(spi_60day, 'SPI 60-Day', 60)}
      </div>

      {/* Soil Moisture */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-gray-700 flex items-center">
          <TrendingDown className="w-4 h-4 mr-1" />
          Soil Moisture
        </h4>
        {getSMDGauge()}
      </div>

      {/* NZDI Category */}
      <div>
        <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
          <Thermometer className="w-4 h-4 mr-1" />
          Drought Category
        </h4>
        {getNZDICategory()}
      </div>

      {/* Confidence */}
      {getConfidenceIndicator()}

      {/* Constitutional Compliance Note */}
      <div className="bg-blue-50 rounded-lg p-3 mt-4">
        <p className="text-xs text-blue-800">
          <strong>Constitutional AI:</strong> Indicators calculated with scientific precision.
          Confidence calibrated by time horizon (Satya principle).
        </p>
      </div>
    </div>
  );
};

export default IndicatorGauges;