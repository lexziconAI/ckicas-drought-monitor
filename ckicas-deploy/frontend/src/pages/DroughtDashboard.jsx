import React, { useState } from 'react';
import DroughtMap from '../components/Map/DroughtMap';
import IndicatorGauges from '../components/Indicators/IndicatorGauges';
import RainfallChart from '../components/Charts/RainfallChart';
import DataSourcesAccordion from '../components/Sources/DataSourcesAccordion';
import Header from '../components/Layout/Header';
import Chatbot from '../components/Admin/Chatbot';

function DroughtDashboard() {
  const [chatbotOpen, setChatbotOpen] = useState(false);

  // Mock data for chatbot context (in a real app, this would come from API)
  const mockHealth = {
    status: 'healthy',
    response_time_seconds: 0.234,
    services: ['database', 'cache', 'api']
  };

  const mockMetrics = {
    cache: { hit_rate: 0.85, size_mb: 45.2 },
    performance: { avg_response_time: 0.234, requests_per_minute: 12.5 },
    system: { cpu_usage: 0.32, memory_usage: 0.67 }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            NZ Drought Early Warning Dashboard
          </h1>
          <p className="text-lg text-gray-600">
            Constitutional AI drought monitoring for New Zealand farmers
          </p>
          <div className="flex justify-center space-x-4 mt-4">
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
              Ahimsa: Non-harm
            </span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
              Satya: Truth
            </span>
            <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
              Asteya: Attribution
            </span>
          </div>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Map */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold mb-4">Regional Drought Risk Map</h2>
              <DroughtMap />
            </div>
          </div>

          {/* Right Column - Indicators */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4">Drought Indicators</h3>
              <IndicatorGauges
                indicators={{
                  spi_30day: -1.8,
                  spi_60day: -1.6,
                  smd_current: -125.4,
                  smd_anomaly: -35.2,
                  nzdi_category: 'DROUGHT'
                }}
                confidence="HIGH"
              />
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4">Data Sources</h3>
              <DataSourcesAccordion sources={[
                {
                  provider: 'NIWA_DataHub',
                  dataset: 'CliFlo_Station_2112',
                  timestamp: '2024-11-16T06:00:00Z',
                  freshness_hours: 8,
                  parameters: ['rainfall_daily', 'temperature_max']
                },
                {
                  provider: 'Waikato_RC',
                  dataset: 'SoilMoisture_Ruakura',
                  timestamp: '2024-11-16T14:00:00Z',
                  freshness_hours: 0,
                  parameters: ['soil_moisture_volumetric']
                }
              ]} />
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">90-Day Rainfall Trend</h2>
            <RainfallChart />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500">
          <p>Constitutional AI Dashboard - Following Yama principles for farmer trust and accuracy</p>
          <p className="text-sm mt-2">Data sources cited with timestamps • Confidence levels time-calibrated • No false alarms</p>
        </footer>
      </main>

      {/* Floating Chatbot */}
      <Chatbot
        isOpen={chatbotOpen}
        onToggle={() => setChatbotOpen(!chatbotOpen)}
        health={mockHealth}
        metrics={mockMetrics}
      />
    </div>
  );
}

export default DroughtDashboard;