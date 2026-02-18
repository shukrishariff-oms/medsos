import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import Connect from './pages/Connect';
import Compose from './pages/Compose';
import Inbox from './pages/Inbox';
import Analytics from './pages/Analytics';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/connect" element={<Connect />} />
          <Route path="/compose" element={<Compose />} />
          <Route path="/inbox" element={<Inbox />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/" element={<Navigate to="/compose" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
