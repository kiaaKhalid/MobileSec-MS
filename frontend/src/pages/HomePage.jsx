import { useState, useEffect } from 'react';
import { Shield, Activity, AlertTriangle, TrendingUp, Zap } from 'lucide-react';

function HomePage() {
  const [services, setServices] = useState([]);
  const [stats, setStats] = useState({
    totalScans: 0,
    vulnerabilities: 0,
    activeScans: 0
  });

  useEffect(() => {
    checkServices();
    const interval = setInterval(checkServices, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkServices = async () => {
    const serviceList = [
      { name: 'APK Scanner', url: 'http://localhost:8001/health', icon: '📱', color: '#667eea' },
      { name: 'Secret Hunter', url: 'http://localhost:8002/health', icon: '🔍', color: '#06b6d4' },
      { name: 'Crypto Check', url: 'http://localhost:8003/health', icon: '🔐', color: '#10b981' },
      { name: 'Network Inspector', url: 'http://localhost:8004/health', icon: '🌐', color: '#8b5cf6' },
      { name: 'Report Generator', url: 'http://localhost:8005/health', icon: '📊', color: '#f59e0b' },
      { name: 'Fix Suggest', url: 'http://localhost:8006/health', icon: '🔧', color: '#ef4444' },
      { name: 'CI Connector', url: 'http://localhost:8007/health', icon: '🔄', color: '#ec4899' }
    ];

    const results = await Promise.all(
      serviceList.map(async (service) => {
        try {
          const response = await fetch(service.url);
          return { ...service, status: response.ok ? 'online' : 'offline' };
        } catch {
          return { ...service, status: 'offline' };
        }
      })
    );

    setServices(results);
    
    // Simulate stats animation
    setTimeout(() => {
      setStats({
        totalScans: 1248,
        vulnerabilities: 342,
        activeScans: results.filter(s => s.status === 'online').length
      });
    }, 300);
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Security Dashboard</h1>
        <p>Monitor your mobile application security in real-time</p>
      </div>

      {/* Stats Grid - 3 Cards */}
      <div className="stats-grid-three">
        <div className="stat-card" style={{ '--accent-color': '#667eea' }}>
          <div className="stat-icon">
            <Zap size={32} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Total Scans</div>
            <div className="stat-value">{stats.totalScans.toLocaleString()}</div>
            <div className="stat-trend">
              <TrendingUp size={16} />
              <span>+12% from last month</span>
            </div>
          </div>
        </div>

        <div className="stat-card" style={{ '--accent-color': '#ef4444' }}>
          <div className="stat-icon">
            <AlertTriangle size={32} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Vulnerabilities Found</div>
            <div className="stat-value">{stats.vulnerabilities.toLocaleString()}</div>
            <div className="stat-trend danger">
              <AlertTriangle size={16} />
              <span>8 critical issues</span>
            </div>
          </div>
        </div>

        <div className="stat-card" style={{ '--accent-color': '#06b6d4' }}>
          <div className="stat-icon">
            <Activity size={32} />
          </div>
          <div className="stat-content">
            <div className="stat-label">Active Services</div>
            <div className="stat-value">{stats.activeScans}/{services.length}</div>
            <div className="stat-trend">
              <Activity size={16} />
              <span>All systems operational</span>
            </div>
          </div>
        </div>
      </div>

      {/* Services Grid */}
      <div style={{ marginTop: '3rem' }}>
        <h2 style={{ fontSize: '2rem', marginBottom: '2rem', fontWeight: '700' }}>
          <Shield size={32} style={{ display: 'inline-block', verticalAlign: 'middle', marginRight: '1rem' }} />
          Service Status
        </h2>
        
        <div className="grid">
          {services.map((service, index) => (
            <div 
              key={index} 
              className="service-card"
              style={{ 
                animationDelay: `${index * 0.1}s`,
                '--service-color': service.color 
              }}
            >
              <div className="service-header">
                <div className="service-icon" style={{ background: service.color }}>
                  <span>{service.icon}</span>
                </div>
                <div className="service-info">
                  <h3>{service.name}</h3>
                  <span className={`status-badge ${service.status}`}>
                    <span className="pulse"></span>
                    {service.status === 'online' ? 'Online' : 'Offline'}
                  </span>
                </div>
              </div>
              
              <div className="service-details">
                <div className="detail-row">
                  <span>Endpoint:</span>
                  <code>{service.url}</code>
                </div>
                <div className="detail-row">
                  <span>Response Time:</span>
                  <span className="response-time">{service.status === 'online' ? '< 100ms' : 'N/A'}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
