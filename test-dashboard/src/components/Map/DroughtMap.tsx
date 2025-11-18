'use client';

import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
import L from 'leaflet';
if (typeof window !== 'undefined') {
  delete (L.Icon.Default.prototype as any)._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  });
}

interface DroughtMapProps {
  apiBaseUrl: string;
}

const DroughtMap: React.FC<DroughtMapProps> = ({ apiBaseUrl }) => {
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number; lon: number } | null>(null);
  const [mapCenter, setMapCenter] = useState([-40.9, 174.9]); // Better NZ center coordinates
  const [mapZoom, setMapZoom] = useState(5); // Better zoom for NZ view
  const [droughtData, setDroughtData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [regionalData, setRegionalData] = useState<any[]>([]);
  const [regionalLoading, setRegionalLoading] = useState(true);

  // NZ regions with coordinates (no hardcoded risk scores)
  const nzRegions = [
    { name: 'Northland', lat: -35.7, lon: 174.3 },
    { name: 'Auckland', lat: -36.8, lon: 174.7 },
    { name: 'Waikato', lat: -37.7, lon: 175.2 },
    { name: 'Bay of Plenty', lat: -37.7, lon: 176.2 },
    { name: 'Gisborne', lat: -38.6, lon: 178.0 },
    { name: 'Hawke\'s Bay', lat: -39.5, lon: 176.8 },
    { name: 'Taranaki', lat: -39.1, lon: 174.1 },
    { name: 'Manawatu-Wanganui', lat: -40.0, lon: 175.7 },
    { name: 'Wellington', lat: -41.3, lon: 174.8 },
    { name: 'Tasman', lat: -41.3, lon: 173.0 },
    { name: 'Nelson', lat: -41.3, lon: 173.3 },
    { name: 'Marlborough', lat: -41.5, lon: 173.9 },
    { name: 'West Coast', lat: -42.4, lon: 171.2 },
    { name: 'Canterbury', lat: -43.5, lon: 171.2 },
    { name: 'Otago', lat: -45.0, lon: 170.5 },
    { name: 'Southland', lat: -46.4, lon: 168.4 }
  ];

  // Fetch regional drought data on component mount
  useEffect(() => {
    fetchRegionalDroughtData();
  }, []);

  // Fetch drought risk data when location is selected
  useEffect(() => {
    if (selectedLocation) {
      fetchDroughtData(selectedLocation.lat, selectedLocation.lon);
    }
  }, [selectedLocation]);

  const fetchRegionalDroughtData = async () => {
    setRegionalLoading(true);
    try {
      const regionalPromises = nzRegions.map(async (region) => {
        try {
          const response = await fetch(`${apiBaseUrl}/api/public/drought-risk?lat=${region.lat}&lon=${region.lon}&forecast_days=7`);
          if (!response.ok) {
            throw new Error(`Failed to fetch data for ${region.name}`);
          }
          const data = await response.json();
          return {
            ...region,
            risk: data.risk_score || 50, // Default to 50 if no risk_score
            confidence: data.confidence || 0,
            factors: data.factors || [],
            lastUpdated: new Date().toISOString()
          };
        } catch (error) {
          console.error(`Error fetching data for ${region.name}:`, error);
          // Return region with default data if API fails
          return {
            ...region,
            risk: 50, // Default moderate risk
            confidence: 0.2,
            factors: ['api_error'],
            lastUpdated: new Date().toISOString(),
            error: true
          };
        }
      });

      const regionalResults = await Promise.all(regionalPromises);
      setRegionalData(regionalResults);
      console.log('Fetched real regional drought data:', regionalResults);
    } catch (error) {
      console.error('Error fetching regional data:', error);
      setError('Failed to load regional drought data');
    } finally {
      setRegionalLoading(false);
    }
  };

  const fetchDroughtData = async (lat: number, lon: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/public/drought-risk?lat=${lat}&lon=${lon}&forecast_days=14`);
      if (!response.ok) {
        throw new Error('Failed to fetch drought data');
      }
      const data = await response.json();
      setDroughtData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  // Get risk color based on drought risk score
  const getRiskColor = (risk: number) => {
    if (risk >= 80) return '#dc2626'; // Red - Extreme drought
    if (risk >= 60) return '#ea580c'; // Orange - Severe drought
    if (risk >= 40) return '#d97706'; // Amber - Moderate drought
    if (risk >= 20) return '#65a30d'; // Yellow-green - Mild drought
    return '#16a34a'; // Green - Normal
  };

  // Get risk category
  const getRiskCategory = (risk: number) => {
    if (risk >= 80) return 'Extreme Drought';
    if (risk >= 60) return 'Severe Drought';
    if (risk >= 40) return 'Moderate Drought';
    if (risk >= 20) return 'Mild Drought';
    return 'Normal Conditions';
  };

  const handleMapClick = (e: any) => {
    const { lat, lng } = e.latlng;
    setSelectedLocation({ lat, lon: lng });
    setMapCenter([lat, lng]);
  };

  // Only render map on client side
  if (typeof window === 'undefined') {
    return <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center">Loading map...</div>;
  }

  return (
    <div className="relative w-full h-[600px] rounded-lg overflow-hidden border border-gray-200">
      <div className="w-full h-full">
        <MapContainer
          key="drought-map" // Prevent React re-mounting
          center={mapCenter as [number, number]}
          zoom={mapZoom}
          style={{ height: '100%', width: '100%' }}
          maxBounds={[[-48, 165], [-34, 180]]} // Restrict panning to NZ region
          maxBoundsViscosity={1.0} // Prevent dragging outside bounds
          scrollWheelZoom={false} // Prevent scroll hijacking
          // @ts-ignore - react-leaflet types issue
          onClick={handleMapClick}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {/* NZ Region Circles */}
          {regionalData.map((region, index) => (
            <Circle
              key={index}
              center={[region.lat, region.lon]}
              radius={50000} // 50km radius
              pathOptions={{
                color: getRiskColor(region.risk),
                fillColor: getRiskColor(region.risk),
                fillOpacity: 0.6,
                weight: 2
              }}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-semibold text-lg">{region.name}</h3>
                  <p className="text-sm text-gray-600">
                    Risk Score: <span className="font-medium">{region.risk}/100</span>
                  </p>
                  <p className="text-sm text-gray-500">
                    Confidence: <span className="font-medium">{Math.round((region.confidence || 0) * 100)}%</span>
                  </p>
                  {region.error && (
                    <p className="text-sm text-red-500">⚠️ Using fallback data</p>
                  )}
                  <p className="text-sm">
                    Category: <span
                      className="font-medium"
                      style={{ color: getRiskColor(region.risk) }}
                    >
                      {getRiskCategory(region.risk)}
                    </span>
                  </p>
                  <button
                    className="mt-2 px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
                    onClick={() => setSelectedLocation({ lat: region.lat, lon: region.lon })}
                  >
                    Get Details
                  </button>
                </div>
              </Popup>
            </Circle>
          ))}

          {/* Selected location marker */}
          {selectedLocation && (
            <Marker position={[selectedLocation.lat, selectedLocation.lon]}>
              <Popup>
                <div className="p-2">
                  <h3 className="font-semibold">Selected Location</h3>
                  <p className="text-sm text-gray-600">
                    {selectedLocation.lat.toFixed(4)}, {selectedLocation.lon.toFixed(4)}
                  </p>
                  {droughtData && (
                    <div className="mt-2">
                      <p className="text-sm">
                        Risk Score: <span className="font-medium">{droughtData.risk_score || droughtData.risk_level}/100</span>
                      </p>
                      <p className="text-sm">
                        Confidence: <span className="font-medium">{Math.round((droughtData.confidence || 0) * 100)}%</span>
                      </p>
                    </div>
                  )}
                  {isLoading && <p className="text-sm text-gray-500">Loading...</p>}
                  {error && <p className="text-sm text-red-500">Error: {error}</p>}
                </div>
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </div>

      {/* Map Controls */}
      <div className="absolute top-4 right-4 bg-white p-4 rounded-lg shadow-lg z-[1000] max-w-xs">
        <div className="flex items-center justify-between mb-2">
          <h4 className="font-semibold">Drought Risk Legend</h4>
          <button
            onClick={fetchRegionalDroughtData}
            disabled={regionalLoading}
            className="px-2 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 disabled:bg-gray-400"
            title="Refresh regional data"
          >
            {regionalLoading ? '⟳' : '↻'}
          </button>
        </div>
        {regionalLoading && (
          <p className="text-xs text-blue-600 mb-2">Loading regional data...</p>
        )}
        <div className="space-y-1 text-sm">
          <div className="flex items-center">
            <div className="w-4 h-4 rounded mr-2" style={{ backgroundColor: '#dc2626' }}></div>
            <span>Extreme Drought (80-100)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded mr-2" style={{ backgroundColor: '#ea580c' }}></div>
            <span>Severe Drought (60-79)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded mr-2" style={{ backgroundColor: '#d97706' }}></div>
            <span>Moderate Drought (40-59)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded mr-2" style={{ backgroundColor: '#65a30d' }}></div>
            <span>Mild Drought (20-39)</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded mr-2" style={{ backgroundColor: '#16a34a' }}></div>
            <span>Normal (0-19)</span>
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Data updated: {regionalData.length > 0 ? new Date(regionalData[0]?.lastUpdated || Date.now()).toLocaleTimeString() : 'Loading...'}
        </p>
      </div>

      {/* Location Input */}
      <div className="mt-4 flex space-x-4">
        <input
          type="number"
          step="0.0001"
          placeholder="Latitude"
          value={selectedLocation?.lat || ''}
          onChange={(e) => setSelectedLocation(prev => ({
            lat: parseFloat(e.target.value) || prev?.lat || 0,
            lon: prev?.lon || 174.0
          }))}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="number"
          step="0.0001"
          placeholder="Longitude"
          value={selectedLocation?.lon || ''}
          onChange={(e) => setSelectedLocation(prev => ({
            lat: prev?.lat || -41.0,
            lon: parseFloat(e.target.value) || prev?.lon || 0
          }))}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={() => selectedLocation && setMapCenter([selectedLocation.lat, selectedLocation.lon])}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Center Map
        </button>
      </div>
    </div>
  );
};

export default DroughtMap;