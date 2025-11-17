import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Activity,
  Database,
  Zap,
  AlertTriangle,
  CheckCircle,
  XCircle,
  RefreshCw,
  Download,
  LogOut,
  TrendingUp,
  Server,
  Wifi,
  WifiOff
} from 'lucide-react';
import HealthIndicator from './HealthIndicator';
import APIStatusPanel from './APIStatusPanel';
import MetricsGraphs from './MetricsGraphs';
import ControlPanel from './ControlPanel';
import LogViewer from './LogViewer';
import Chatbot from './Chatbot';

function AdminDashboard() {
  const [health, setHealth] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [apiStatus, setApiStatus] = useState({});
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [wsConnected, setWsConnected] = useState(false);
  const [chatbotOpen, setChatbotOpen] = useState(false);
  const navigate = useNavigate();

  // Check authentication
  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      navigate('/admin/login');
      return;
    }
    loadDashboardData();
  }, [navigate]);

  // WebSocket connection for real-time updates
  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) return;

    const ws = new WebSocket(`ws://localhost:8000/api/admin/ws`);

    ws.onopen = () => {
      setWsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'health_update') {
        setHealth(data.health);
        setMetrics(data.metrics);
      }
    };

    ws.onclose = () => {
      setWsConnected(false);
    };

    ws.onerror = () => {
      setWsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, []);

  const loadDashboardData = async () => {
    try {
      const [healthRes, metricsRes, apiRes, logsRes] = await Promise.all([
        axios.get('/api/admin/health'),
        axios.get('/api/admin/metrics'),
        axios.get('/api/admin/apis'),
        axios.get('/api/admin/logs')
      ]);

      setHealth(healthRes.data);
      setMetrics(metricsRes.data);
      setApiStatus(apiRes.data);
      setLogs(logsRes.data.logs);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    navigate('/admin/login');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
      case 'operational':
        return 'text-green-600';
      case 'degraded':
        return 'text-yellow-600';
      case 'failed':
      case 'unhealthy':
        return 'text-red-600';
      default:
        return 'text-gray-600';
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto text-blue-600" />
          <p className="mt-2 text-gray-600">Loading CKICAS Admin Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Server className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">CKICAS Admin Dashboard</h1>
                <p className="text-sm text-gray-600">Constitutional AI System Monitoring</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* WebSocket Status */}
              <div className="flex items-center space-x-2">
                {wsConnected ? (
                  <Wifi className="h-5 w-5 text-green-600" />
                ) : (
                  <WifiOff className="h-5 w-5 text-red-600" />
                )}
                <span className={`text-sm ${wsConnected ? 'text-green-600' : 'text-red-600'}`}>
                  {wsConnected ? 'Live' : 'Offline'}
                </span>
              </div>

              {/* System Status */}
              {health && (
                <div className="flex items-center space-x-2">
                  {getStatusIcon(health.status)}
                  <span className={`text-sm font-medium ${getStatusColor(health.status)}`}>
                    {health.status.toUpperCase()}
                  </span>
                </div>
              )}

              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Status Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <HealthIndicator
            title="System Health"
            status={health?.status || 'unknown'}
            value={health?.response_time_seconds ? `${health.response_time_seconds}s` : 'N/A'}
            icon={<Activity className="h-6 w-6" />}
          />

          <HealthIndicator
            title="Cache Efficiency"
            status={metrics?.cache?.hit_rate > 0.7 ? 'healthy' : 'degraded'}
            value={`${((metrics?.cache?.hit_rate || 0) * 100).toFixed(1)}%`}
            icon={<Zap className="h-6 w-6" />}
          />

          <HealthIndicator
            title="Database"
            status={health?.components?.database || 'unknown'}
            value="Operational"
            icon={<Database className="h-6 w-6" />}
          />

          <HealthIndicator
            title="Active Alerts"
            status={health?.issues?.length > 0 ? 'degraded' : 'healthy'}
            value={health?.issues?.length || 0}
            icon={<AlertTriangle className="h-6 w-6" />}
          />
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            <APIStatusPanel apiStatus={apiStatus} />
            <MetricsGraphs metrics={metrics} />
            <LogViewer logs={logs} />
          </div>

          {/* Right Column */}
          <div>
            <ControlPanel onRefresh={loadDashboardData} />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500">
          <p>CKICAS Admin Dashboard - Constitutional AI System Monitoring</p>
          <p className="text-sm mt-2">
            Phase 1: Drought Early Warning • Yama Principles: Ahimsa, Satya, Asteya, Brahmacharya, Aparigraha
          </p>
        </footer>
      </main>

      {/* Chatbot */}
      <Chatbot
        isOpen={chatbotOpen}
        onToggle={() => setChatbotOpen(!chatbotOpen)}
        health={health}
        metrics={metrics}
      />
    </div>
  );
}

export default AdminDashboard;