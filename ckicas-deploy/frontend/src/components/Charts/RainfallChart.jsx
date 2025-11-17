import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

const RainfallChart = ({ data = null }) => {
  // Sample data for demonstration (would come from API)
  const sampleData = [
    { date: '2024-08-01', rainfall: 12.5, normal: 8.2, temperature: 18.5 },
    { date: '2024-08-08', rainfall: 8.3, normal: 8.2, temperature: 19.2 },
    { date: '2024-08-15', rainfall: 15.7, normal: 8.2, temperature: 17.8 },
    { date: '2024-08-22', rainfall: 6.2, normal: 8.2, temperature: 20.1 },
    { date: '2024-08-29', rainfall: 3.8, normal: 8.2, temperature: 21.5 },
    { date: '2024-09-05', rainfall: 2.1, normal: 7.8, temperature: 22.3 },
    { date: '2024-09-12', rainfall: 1.5, normal: 7.8, temperature: 23.1 },
    { date: '2024-09-19', rainfall: 0.8, normal: 7.8, temperature: 24.2 },
    { date: '2024-09-26', rainfall: 4.2, normal: 7.8, temperature: 22.8 },
    { date: '2024-10-03', rainfall: 2.9, normal: 7.5, temperature: 21.6 },
    { date: '2024-10-10', rainfall: 1.2, normal: 7.5, temperature: 20.3 },
    { date: '2024-10-17', rainfall: 0.5, normal: 7.5, temperature: 19.7 },
    { date: '2024-10-24', rainfall: 3.1, normal: 7.5, temperature: 18.9 },
    { date: '2024-10-31', rainfall: 1.8, normal: 7.5, temperature: 17.4 },
    { date: '2024-11-07', rainfall: 0.3, normal: 7.2, temperature: 16.8 },
    { date: '2024-11-14', rainfall: 0.1, normal: 7.2, temperature: 15.9 }
  ];

  const chartData = data || sampleData;

  // Format date for display
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-NZ', { month: 'short', day: 'numeric' });
  };

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-300 rounded-lg shadow-lg">
          <p className="font-medium">{formatDate(label)}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {entry.value.toFixed(1)}
              {entry.dataKey === 'rainfall' || entry.dataKey === 'normal' ? 'mm' : '°C'}
            </p>
          ))}
          {data.rainfall < data.normal && (
            <p className="text-xs text-red-600 mt-1">
              Below normal rainfall
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  // Calculate drought periods (consecutive weeks below normal)
  const droughtPeriods = [];
  let droughtStart = null;

  chartData.forEach((item, index) => {
    if (item.rainfall < item.normal) {
      if (droughtStart === null) {
        droughtStart = index;
      }
    } else {
      if (droughtStart !== null) {
        if (index - droughtStart >= 2) { // At least 2 weeks
          droughtPeriods.push({
            start: droughtStart,
            end: index - 1,
            severity: 'moderate' // Could calculate based on deficit
          });
        }
        droughtStart = null;
      }
    }
  });

  // Handle ongoing drought
  if (droughtStart !== null && chartData.length - droughtStart >= 2) {
    droughtPeriods.push({
      start: droughtStart,
      end: chartData.length - 1,
      severity: 'severe'
    });
  }

  return (
    <div className="w-full">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">90-Day Rainfall Trend</h3>
        <p className="text-sm text-gray-600">
          Weekly rainfall accumulation compared to historical normals
        </p>
      </div>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              stroke="#6b7280"
              fontSize={12}
            />
            <YAxis
              stroke="#6b7280"
              fontSize={12}
              label={{ value: 'Rainfall (mm)', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />

            {/* Normal rainfall line */}
            <Line
              type="monotone"
              dataKey="normal"
              stroke="#6b7280"
              strokeDasharray="5 5"
              strokeWidth={2}
              name="Historical Normal"
              dot={false}
            />

            {/* Actual rainfall line */}
            <Line
              type="monotone"
              dataKey="rainfall"
              stroke="#2563eb"
              strokeWidth={3}
              name="Actual Rainfall"
              dot={{ fill: '#2563eb', strokeWidth: 2, r: 4 }}
            />

            {/* Drought period overlays */}
            {droughtPeriods.map((period, index) => (
              <ReferenceLine
                key={index}
                x={chartData[period.start].date}
                stroke="#dc2626"
                strokeWidth={0}
                label={{
                  value: "Drought Period",
                  position: "topLeft",
                  fill: "#dc2626",
                  fontSize: 10
                }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Chart Insights */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 p-3 rounded-lg">
          <div className="text-sm font-medium text-blue-900">Total Rainfall</div>
          <div className="text-lg font-bold text-blue-600">
            {chartData.reduce((sum, item) => sum + item.rainfall, 0).toFixed(0)}mm
          </div>
          <div className="text-xs text-blue-700">Last 90 days</div>
        </div>

        <div className="bg-green-50 p-3 rounded-lg">
          <div className="text-sm font-medium text-green-900">Normal Total</div>
          <div className="text-lg font-bold text-green-600">
            {chartData.reduce((sum, item) => sum + item.normal, 0).toFixed(0)}mm
          </div>
          <div className="text-xs text-green-700">Expected amount</div>
        </div>

        <div className="bg-red-50 p-3 rounded-lg">
          <div className="text-sm font-medium text-red-900">Deficit</div>
          <div className={`text-lg font-bold ${
            chartData.reduce((sum, item) => sum + item.rainfall, 0) <
            chartData.reduce((sum, item) => sum + item.normal, 0)
              ? 'text-red-600' : 'text-green-600'
          }`}>
            {Math.abs(
              chartData.reduce((sum, item) => sum + item.rainfall, 0) -
              chartData.reduce((sum, item) => sum + item.normal, 0)
            ).toFixed(0)}mm
          </div>
          <div className="text-xs text-red-700">
            {chartData.reduce((sum, item) => sum + item.rainfall, 0) <
             chartData.reduce((sum, item) => sum + item.normal, 0)
               ? 'Below normal' : 'Above normal'}
          </div>
        </div>
      </div>

      {/* Drought Alert */}
      {droughtPeriods.length > 0 && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <div className="text-red-600 mr-2">⚠️</div>
            <div>
              <div className="text-sm font-medium text-red-900">Drought Alert</div>
              <div className="text-xs text-red-700">
                {droughtPeriods.length} drought period{droughtPeriods.length > 1 ? 's' : ''} detected in the last 90 days
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RainfallChart;