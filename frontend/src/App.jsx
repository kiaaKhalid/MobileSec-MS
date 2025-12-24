import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
// AJOUT : Import de l'icône Brain pour l'IA
import { Shield, Home, Upload, FileSearch, Key, Network, FileText, Wrench, Brain } from 'lucide-react';
import './App.css';

import HomePage from './pages/HomePage';
import APKScannerPage from './pages/APKScannerPage';
import SecretHunterPage from './pages/SecretHunterPage';
import CryptoCheckPage from './pages/CryptoCheckPage';
import NetworkInspectorPage from './pages/NetworkInspectorPage';
import ReportGenPage from './pages/ReportGenPage';
import FixSuggestPage from './pages/FixSuggestPage';
// AJOUT : Import de la nouvelle page
import AIScannerPage from './pages/AIScannerPage';

// AJOUT : Import du Context
import { GlobalStateProvider } from './context/GlobalStateContext';

function App() {
  return (
    <GlobalStateProvider>
      <Router>
        <div className="app">
          <nav className="sidebar">
            <div className="logo">
              <Shield size={32} />
              <h1>MobileSec-MS</h1>
            </div>

            <ul className="nav-menu">
              <li>
                <Link to="/" className="nav-link">
                  <Home size={20} />
                  <span>Dashboard</span>
                </Link>
              </li>
              <li>
                <Link to="/apkscanner" className="nav-link">
                  <Upload size={20} />
                  <span>APK Scanner</span>
                </Link>
              </li>

              {/* --- NOUVEAU LIEN IA SCANNER --- */}
              <li>
                <Link to="/aiscanner" className="nav-link">
                  <Brain size={20} />
                  <span>AI Deep Scan</span>
                </Link>
              </li>
              {/* ------------------------------- */}

              <li>
                <Link to="/secrethunter" className="nav-link">
                  <FileSearch size={20} />
                  <span>Secret Hunter</span>
                </Link>
              </li>
              <li>
                <Link to="/cryptocheck" className="nav-link">
                  <Key size={20} />
                  <span>Crypto Check</span>
                </Link>
              </li>
              <li>
                <Link to="/networkinspector" className="nav-link">
                  <Network size={20} />
                  <span>Network Inspector</span>
                </Link>
              </li>
              <li>
                <Link to="/reportgen" className="nav-link">
                  <FileText size={20} />
                  <span>Report Generator</span>
                </Link>
              </li>
              <li>
                <Link to="/fixsuggest" className="nav-link">
                  <Wrench size={20} />
                  <span>Fix Suggestions</span>
                </Link>
              </li>
            </ul>
          </nav>

          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/apkscanner" element={<APKScannerPage />} />
              <Route path="/aiscanner" element={<AIScannerPage />} />
              <Route path="/secrethunter" element={<SecretHunterPage />} />
              <Route path="/cryptocheck" element={<CryptoCheckPage />} />
              <Route path="/networkinspector" element={<NetworkInspectorPage />} />
              <Route path="/reportgen" element={<ReportGenPage />} />
              <Route path="/fixsuggest" element={<FixSuggestPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </GlobalStateProvider>
  );
}

export default App;